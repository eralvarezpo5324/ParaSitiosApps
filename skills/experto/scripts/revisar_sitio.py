#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
revisar_sitio.py - Revisión de seguridad externa de un sitio ya publicado.

SOLO para sitios propios o con autorización escrita del dueño. Revisar un sitio
ajeno sin permiso puede ser ilegal. Por eso el script exige --sitio-autorizado.

Qué revisa (desde fuera, sin iniciar sesión y sin modificar nada):
  - Que HTTP redirija a HTTPS y que el certificado sea válido y no esté por vencer.
  - Cabeceras de seguridad (HSTS, CSP, anti-clickjacking, nosniff, etc.).
  - Banderas de las cookies (Secure, HttpOnly, SameSite).
  - Archivos sensibles expuestos (.env, .git, respaldos, registros, phpinfo...).
  - Listado de carpetas abierto.
  - Contenido mixto, formularios inseguros y scripts externos sin integridad.
  - Configuración CORS peligrosa.

Es una revisión superficial. No sustituye la auditoría del código.

Uso:
  python3 revisar_sitio.py https://ejemplo.com --sitio-autorizado
  python3 revisar_sitio.py https://ejemplo.com --sitio-autorizado --md reporte.md

Solo usa la biblioteca estándar de Python 3.
Códigos de salida: 0 = sin hallazgos de gravedad alta, 1 = hay al menos uno,
2 = error de uso o sitio inalcanzable.
"""

import argparse
import json
import re
import secrets
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

AGENTE = "revisar-sitio/1.0 (revision de seguridad autorizada)"
PAUSA = 0.15          # segundos entre peticiones, para no saturar un hosting compartido
TIEMPO_LIMITE = 12
LECTURA_MAXIMA = 300_000

FIRMA_ENV = rb"(?m)^\s*[A-Z][A-Z0-9_]{2,}\s*=\s*\S"
FIRMA_SQL = rb"(?i)(CREATE TABLE|INSERT INTO|DROP TABLE)"
FIRMA_PHPINFO = rb"(?i)(<title>phpinfo\(\)|PHP Version\s*</?[a-z])"
FIRMA_ZIP = rb"^(PK\x03\x04|\x1f\x8b|7z\xbc\xaf)"
FIRMA_LOG_PHP = rb"PHP (Notice|Warning|Fatal error|Parse error|Deprecated)"

# (ruta, firma del contenido, gravedad, qué es)
RUTAS_SENSIBLES = [
    ("/.env", FIRMA_ENV, "ALTA", "archivo de variables de entorno con contraseñas"),
    ("/.env.local", FIRMA_ENV, "ALTA", "archivo de variables de entorno"),
    ("/.env.production", FIRMA_ENV, "ALTA", "archivo de variables de entorno"),
    ("/.env.bak", FIRMA_ENV, "ALTA", "copia del archivo de variables de entorno"),
    ("/.git/config", rb"\[core\]", "ALTA", "repositorio git completo descargable"),
    ("/.git/HEAD", rb"^ref:\s*refs/", "ALTA", "repositorio git completo descargable"),
    ("/.htpasswd", rb"(?m)^[^:\s<]+:\$?[A-Za-z0-9./$]{10,}", "ALTA", "contraseñas del servidor"),
    ("/.aws/credentials", rb"aws_access_key_id", "ALTA", "credenciales de AWS"),
    ("/id_rsa", rb"PRIVATE KEY", "ALTA", "llave privada de SSH"),
    ("/wp-config.php.bak", rb"DB_PASSWORD", "ALTA", "copia de la configuración de WordPress"),
    ("/wp-config.php~", rb"DB_PASSWORD", "ALTA", "copia de la configuración de WordPress"),
    ("/wp-config.php.old", rb"DB_PASSWORD", "ALTA", "copia de la configuración de WordPress"),
    ("/wp-config.php.save", rb"DB_PASSWORD", "ALTA", "copia de la configuración de WordPress"),
    ("/wp-config.txt", rb"DB_PASSWORD", "ALTA", "copia de la configuración de WordPress"),
    ("/config.php.bak", rb"<\?php", "ALTA", "copia de un archivo de configuración"),
    ("/config.php~", rb"<\?php", "ALTA", "copia de un archivo de configuración"),
    ("/backup.sql", FIRMA_SQL, "ALTA", "respaldo de la base de datos"),
    ("/db.sql", FIRMA_SQL, "ALTA", "respaldo de la base de datos"),
    ("/database.sql", FIRMA_SQL, "ALTA", "respaldo de la base de datos"),
    ("/dump.sql", FIRMA_SQL, "ALTA", "respaldo de la base de datos"),
    ("/backup.zip", FIRMA_ZIP, "ALTA", "respaldo comprimido del sitio"),
    ("/site.zip", FIRMA_ZIP, "ALTA", "respaldo comprimido del sitio"),
    ("/public_html.zip", FIRMA_ZIP, "ALTA", "respaldo comprimido del sitio"),
    ("/www.zip", FIRMA_ZIP, "ALTA", "respaldo comprimido del sitio"),
    ("/backup.tar.gz", FIRMA_ZIP, "ALTA", "respaldo comprimido del sitio"),
    ("/sftp-config.json", rb'"(password|host)"', "ALTA", "configuración de SFTP con contraseña"),
    ("/.vscode/sftp.json", rb'"(password|host)"', "ALTA", "configuración de SFTP con contraseña"),
    ("/.ftpconfig", rb'"(pass|host)"', "ALTA", "configuración de FTP con contraseña"),
    ("/storage/logs/laravel.log", rb"\[\d{4}-\d{2}-\d{2}", "ALTA", "registro de errores de Laravel"),
    ("/wp-content/debug.log", FIRMA_LOG_PHP, "ALTA", "registro de errores de WordPress"),
    ("/error_log", FIRMA_LOG_PHP, "ALTA", "registro de errores de PHP"),
    ("/debug.log", rb"(?i)(error|warning|exception|notice)", "MEDIA", "registro de depuración"),
    ("/docs/proyecto/reporte-seguridad.md", rb"(?i)seguridad", "ALTA",
     "reporte interno de seguridad del proyecto"),
    ("/docs/proyecto/ESTADO.md", rb"(?i)(fase|estado|proyecto)", "MEDIA",
     "documentos internos del proyecto"),
    ("/CLAUDE.md", rb"(?m)^#", "MEDIA", "documentos internos del proyecto"),
    ("/phpinfo.php", FIRMA_PHPINFO, "MEDIA", "página phpinfo con la configuración del servidor"),
    ("/info.php", FIRMA_PHPINFO, "MEDIA", "página phpinfo con la configuración del servidor"),
    ("/test.php", FIRMA_PHPINFO, "MEDIA", "página phpinfo con la configuración del servidor"),
    ("/adminer.php", rb"(?i)adminer", "MEDIA", "administrador de base de datos Adminer"),
    ("/server-status", rb"Apache Server Status", "MEDIA", "estado interno del servidor Apache"),
    ("/.DS_Store", rb"^\x00\x00\x00\x01Bud1", "MEDIA", "índice de archivos de macOS"),
    ("/phpmyadmin/", rb"(?i)phpmyadmin", "BAJA", "phpMyAdmin accesible desde internet"),
    ("/composer.json", rb'"require"', "BAJA", "lista de dependencias de PHP"),
    ("/composer.lock", rb'"packages"', "BAJA", "versiones exactas de dependencias de PHP"),
    ("/package.json", rb'"(dependencies|devDependencies|scripts)"', "BAJA",
     "lista de dependencias de JavaScript"),
    ("/package-lock.json", rb'"lockfileVersion"', "BAJA",
     "versiones exactas de dependencias de JavaScript"),
    ("/.gitignore", rb"(?m)^(node_modules|vendor|\.env|/?dist)", "BAJA",
     "archivo .gitignore, revela la estructura del proyecto"),
    ("/README.md", rb"(?m)^#", "BAJA", "README del proyecto"),
]
CARPETAS = [
    "/uploads/", "/images/", "/img/", "/assets/", "/css/", "/js/", "/files/",
    "/backup/", "/backups/", "/storage/", "/includes/", "/wp-content/uploads/",
]
FIRMA_LISTADO = re.compile(rb"(?i)(<title>Index of /|Directory listing for|>Parent Directory<)")
COOKIE_DE_SESION = re.compile(
    r"(?i)(sess|sid|auth|token|login|jwt|remember|laravel|wordpress_logged_in|secure)"
)
SOLUCION_ARCHIVO = (
    "Bórralo del servidor o muévelo fuera de la carpeta pública. Si contenía "
    "contraseñas o llaves, cámbialas todas: hay que asumir que ya fueron copiadas."
)


class SinRedireccion(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


ABRIDOR = urllib.request.build_opener(SinRedireccion)


class Respuesta:
    def __init__(self, estado, cabeceras, cuerpo, error=None):
        self.estado = estado
        self.cabeceras = cabeceras  # lista de (nombre en minúsculas, valor)
        self.cuerpo = cuerpo
        self.error = error

    def cabecera(self, nombre):
        for n, v in self.cabeceras:
            if n == nombre:
                return v
        return None

    def todas(self, nombre):
        return [v for n, v in self.cabeceras if n == nombre]


def pedir(url, cabeceras_extra=None):
    """Hace una petición GET sin seguir redirecciones. Nunca lanza excepción."""
    time.sleep(PAUSA)
    cabeceras = {"User-Agent": AGENTE, "Accept": "*/*"}
    cabeceras.update(cabeceras_extra or {})
    peticion = urllib.request.Request(url, headers=cabeceras, method="GET")
    try:
        with ABRIDOR.open(peticion, timeout=TIEMPO_LIMITE) as r:
            return Respuesta(r.status, [(k.lower(), v) for k, v in r.headers.items()],
                             r.read(LECTURA_MAXIMA))
    except urllib.error.HTTPError as e:
        try:
            cuerpo = e.read(LECTURA_MAXIMA)
        except Exception:
            cuerpo = b""
        return Respuesta(e.code, [(k.lower(), v) for k, v in e.headers.items()], cuerpo)
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, ConnectionError, OSError) as e:
        return Respuesta(0, [], b"", error=e)


class Revision:
    def __init__(self, url):
        partes = urllib.parse.urlsplit(url)
        if partes.scheme not in ("http", "https") or not partes.hostname:
            raise ValueError("La dirección debe empezar con https:// o http://")
        self.esquema = partes.scheme
        self.host = partes.hostname
        self.puerto = partes.port
        self.base = f"{partes.scheme}://{partes.netloc}"
        self.inicio = self.base + (partes.path or "/")
        self.local = self.host in ("localhost", "127.0.0.1", "::1")
        self.hallazgos = []
        self.correctos = []
        self.no_verificado = []

    def hallazgo(self, gravedad, titulo, detalle, solucion):
        self.hallazgos.append({"gravedad": gravedad, "titulo": titulo,
                               "detalle": detalle, "solucion": solucion})

    # -- HTTPS y certificado -------------------------------------------------

    def revisar_https(self):
        if self.esquema == "http":
            if self.local:
                self.no_verificado.append("HTTPS y certificado (sitio local de pruebas)")
            else:
                self.hallazgo("ALTA", "El sitio se revisó por HTTP, sin cifrado",
                              "La dirección indicada no usa HTTPS.",
                              "Activa el certificado SSL en el hosting y publica el sitio en https://.")
            return

        r = pedir(f"http://{self.host}/")
        destino = r.cabecera("location") or ""
        if r.estado in (301, 302, 303, 307, 308) and destino.lower().startswith("https://"):
            self.correctos.append("HTTP redirige a HTTPS")
            if r.estado in (302, 303, 307):
                self.hallazgo("BAJA", "La redirección a HTTPS es temporal",
                              f"Responde {r.estado} en lugar de 301.",
                              "Usa una redirección permanente (301) de HTTP a HTTPS.")
        elif r.estado == 200:
            self.hallazgo("ALTA", "El sitio también responde por HTTP sin cifrado",
                          "http:// entrega la página en lugar de redirigir a https://.",
                          "Fuerza HTTPS: en cPanel activa 'Forzar HTTPS' o añade la regla "
                          "de redirección en .htaccess.")
        elif r.estado == 0:
            self.no_verificado.append("Redirección de HTTP a HTTPS (el puerto 80 no respondió)")
        else:
            self.hallazgo("MEDIA", "HTTP no redirige claramente a HTTPS",
                          f"http:// responde {r.estado} con destino '{destino or 'ninguno'}'.",
                          "Configura una redirección 301 de todo HTTP a HTTPS.")

        try:
            contexto = ssl.create_default_context()
            with socket.create_connection((self.host, self.puerto or 443), timeout=8) as crudo:
                with contexto.wrap_socket(crudo, server_hostname=self.host) as seguro:
                    version = seguro.version() or ""
                    certificado = seguro.getpeercert()
            dias = int((ssl.cert_time_to_seconds(certificado["notAfter"]) - time.time()) / 86400)
            if version in ("TLSv1", "TLSv1.1", "SSLv3"):
                self.hallazgo("ALTA", f"El servidor negocia {version}, un cifrado obsoleto",
                              "Las versiones anteriores a TLS 1.2 tienen fallas conocidas.",
                              "Pide al hosting desactivar TLS 1.0 y 1.1.")
            else:
                self.correctos.append(f"Cifrado {version}")
            if dias < 15:
                self.hallazgo("MEDIA", f"El certificado vence en {dias} días",
                              "Si vence, los navegadores bloquearán el sitio.",
                              "Revisa que la renovación automática (AutoSSL o Let's Encrypt) funcione.")
            else:
                self.correctos.append(f"Certificado válido, vence en {dias} días")
        except ssl.SSLCertVerificationError as e:
            self.hallazgo("ALTA", "El certificado no es válido",
                          str(e), "Instala un certificado válido para este dominio.")
        except Exception:
            self.no_verificado.append(
                "Versión de TLS y vencimiento del certificado (sin conexión directa al servidor)"
            )

    # -- Cabeceras -----------------------------------------------------------

    def revisar_cabeceras(self, r):
        csp = r.cabecera("content-security-policy") or ""
        csp_reporte = r.cabecera("content-security-policy-report-only")

        if self.esquema == "https":
            hsts = r.cabecera("strict-transport-security")
            if not hsts:
                self.hallazgo("MEDIA", "Falta la cabecera HSTS",
                              "Sin Strict-Transport-Security el navegador puede volver a HTTP.",
                              "Añade: Strict-Transport-Security: max-age=31536000; includeSubDomains")
            else:
                m = re.search(r"max-age\s*=\s*(\d+)", hsts)
                if not m or int(m.group(1)) < 15552000:
                    self.hallazgo("BAJA", "HSTS con duración corta", f"Valor actual: {hsts}",
                                  "Usa max-age=31536000 (un año).")
                else:
                    self.correctos.append("HSTS activo")

        if not csp:
            detalle = ("Solo existe en modo reporte, que no bloquea nada." if csp_reporte
                       else "No hay Content-Security-Policy.")
            self.hallazgo("MEDIA", "Falta la política de seguridad de contenido (CSP)", detalle,
                          "Define una CSP que solo permita scripts y recursos de orígenes "
                          "conocidos. Reduce mucho el daño de una inyección de código.")
        else:
            directivas = {}
            for parte in csp.split(";"):
                trozos = parte.strip().split()
                if trozos:
                    directivas[trozos[0].lower()] = [t.lower() for t in trozos[1:]]
            scripts = directivas.get("script-src", directivas.get("default-src", []))
            debiles = [v for v in ("'unsafe-inline'", "'unsafe-eval'", "*") if v in scripts]
            con_nonce = any(v.startswith("'nonce-") or v.startswith("'sha") or
                            v == "'strict-dynamic'" for v in scripts)
            if debiles and not con_nonce:
                self.hallazgo("BAJA", "La CSP permite scripts de forma demasiado amplia",
                              f"script-src incluye: {', '.join(debiles)}",
                              "Sustituye 'unsafe-inline' por nonces o hashes y evita 'unsafe-eval' y '*'.")
            else:
                self.correctos.append("CSP presente")

        marco = (r.cabecera("x-frame-options") or "").upper()
        if not (marco in ("DENY", "SAMEORIGIN") or "frame-ancestors" in csp.lower()):
            self.hallazgo("MEDIA", "El sitio puede incrustarse en páginas ajenas (clickjacking)",
                          "No hay X-Frame-Options ni frame-ancestors en la CSP.",
                          "Añade frame-ancestors 'self' a la CSP, o X-Frame-Options: SAMEORIGIN.")
        else:
            self.correctos.append("Protección contra clickjacking")

        if (r.cabecera("x-content-type-options") or "").lower() != "nosniff":
            self.hallazgo("BAJA", "Falta X-Content-Type-Options: nosniff",
                          "El navegador puede interpretar un archivo como otro tipo.",
                          "Añade: X-Content-Type-Options: nosniff")
        else:
            self.correctos.append("nosniff activo")

        referente = (r.cabecera("referrer-policy") or "").lower()
        if not referente:
            self.hallazgo("BAJA", "Falta Referrer-Policy",
                          "Las direcciones internas pueden filtrarse a otros sitios.",
                          "Añade: Referrer-Policy: strict-origin-when-cross-origin")
        elif "unsafe-url" in referente or referente == "no-referrer-when-downgrade":
            self.hallazgo("BAJA", "Referrer-Policy demasiado permisiva", f"Valor actual: {referente}",
                          "Usa strict-origin-when-cross-origin.")
        else:
            self.correctos.append("Referrer-Policy correcta")

        if not r.cabecera("permissions-policy"):
            self.hallazgo("INFO", "Falta Permissions-Policy",
                          "Sin ella, el sitio no declara qué funciones del dispositivo usa.",
                          "Añade, por ejemplo: Permissions-Policy: camera=(), microphone=(), geolocation=()")

        servidor = r.cabecera("server") or ""
        if re.search(r"\d+\.\d+", servidor):
            self.hallazgo("BAJA", "El servidor revela su versión", f"Server: {servidor}",
                          "Oculta la versión (ServerTokens Prod en Apache, server_tokens off en Nginx).")
        potencia = r.cabecera("x-powered-by")
        if potencia:
            self.hallazgo("BAJA", "El servidor revela la tecnología usada", f"X-Powered-By: {potencia}",
                          "Quita la cabecera (expose_php = Off en PHP; app.disable('x-powered-by') en Express).")

    def revisar_cookies(self, r):
        for cruda in r.todas("set-cookie"):
            nombre = cruda.split("=", 1)[0].strip()
            banderas = cruda.lower()
            sesion = bool(COOKIE_DE_SESION.search(nombre))
            faltan = []
            if self.esquema == "https" and not re.search(r";\s*secure", banderas):
                faltan.append("Secure")
            if not re.search(r";\s*httponly", banderas):
                faltan.append("HttpOnly")
            if not re.search(r";\s*samesite\s*=", banderas):
                faltan.append("SameSite")
            if not faltan:
                self.correctos.append(f"Cookie {nombre} bien protegida")
                continue
            grave = sesion and ("Secure" in faltan or "HttpOnly" in faltan)
            self.hallazgo(
                "MEDIA" if grave else "BAJA",
                f"La cookie {nombre} no tiene {', '.join(faltan)}",
                "Parece una cookie de sesión." if sesion else "Cookie sin todas las protecciones.",
                "Las cookies de sesión deben llevar Secure, HttpOnly y SameSite=Lax (o Strict).",
            )

    def revisar_cors(self):
        origen_falso = "https://origen-de-prueba.invalid"
        r = pedir(self.inicio, {"Origin": origen_falso})
        permitido = r.cabecera("access-control-allow-origin")
        credenciales = (r.cabecera("access-control-allow-credentials") or "").lower() == "true"
        if permitido == origen_falso and credenciales:
            self.hallazgo("ALTA", "CORS acepta cualquier origen con credenciales",
                          "El servidor refleja el origen que se le envía y permite cookies.",
                          "Usa una lista fija de orígenes permitidos; nunca reflejes el origen recibido.")
        elif permitido == origen_falso:
            self.hallazgo("MEDIA", "CORS refleja cualquier origen",
                          "Cualquier sitio puede leer las respuestas públicas.",
                          "Limita Access-Control-Allow-Origin a los dominios que lo necesitan.")
        elif permitido == "*":
            self.hallazgo("INFO", "CORS abierto a todos los orígenes",
                          "Es aceptable solo si el contenido es totalmente público.",
                          "Confirma que ninguna ruta con datos privados responde con este valor.")

    # -- Contenido de la página ---------------------------------------------

    def revisar_html(self, r):
        tipo = (r.cabecera("content-type") or "").lower()
        if "html" not in tipo:
            return
        texto = r.cuerpo.decode("utf-8", "replace")
        if self.esquema == "https":
            mixto = re.findall(
                r"(?is)<(?:script|img|iframe|video|audio|source|embed)\b[^>]*?\bsrc\s*=\s*[\"'](http://[^\"']+)",
                texto)
            mixto += re.findall(
                r"(?is)<link\b[^>]*?\brel\s*=\s*[\"']?stylesheet[^>]*?\bhref\s*=\s*[\"'](http://[^\"']+)",
                texto)
            if mixto:
                self.hallazgo("MEDIA", "Contenido mixto: recursos cargados por HTTP",
                              "Ejemplos: " + ", ".join(sorted(set(mixto))[:3]),
                              "Carga todos los recursos por https://.")
        if re.search(r"(?is)<form\b[^>]*\baction\s*=\s*[\"']http://", texto):
            self.hallazgo("ALTA", "Un formulario envía datos por HTTP sin cifrar",
                          "Hay un <form> cuyo destino empieza con http://.",
                          "Cambia el destino del formulario a https://.")
        if self.esquema == "http" and not self.local and re.search(
                r"(?is)<input\b[^>]*type\s*=\s*[\"']?password", texto):
            self.hallazgo("ALTA", "Campo de contraseña en una página sin cifrado",
                          "La contraseña viajaría en texto claro.", "Publica la página en HTTPS.")
        externos = []
        for etiqueta in re.findall(r"(?is)<script\b[^>]*\bsrc\s*=\s*[\"'][^\"']+[\"'][^>]*>", texto):
            origen = re.search(r"(?is)\bsrc\s*=\s*[\"']([^\"']+)", etiqueta).group(1)
            destino = urllib.parse.urlsplit(urllib.parse.urljoin(self.inicio, origen))
            if destino.hostname and destino.hostname != self.host and "integrity=" not in etiqueta.lower():
                externos.append(destino.hostname)
        if externos:
            self.hallazgo("BAJA", "Scripts externos sin verificación de integridad",
                          "Orígenes: " + ", ".join(sorted(set(externos))[:6]),
                          "Si la versión del script es fija, añade integrity y crossorigin. "
                          "Mejor aún, sirve esos archivos desde tu propio dominio.")
        generador = re.search(
            r"(?is)<meta\b[^>]*name\s*=\s*[\"']generator[\"'][^>]*content\s*=\s*[\"']([^\"']+)", texto)
        if generador and re.search(r"\d", generador.group(1)):
            self.hallazgo("BAJA", "La página revela el sistema y su versión",
                          f"generator: {generador.group(1)}",
                          "Quita la etiqueta meta generator.")

    # -- Archivos y carpetas expuestos --------------------------------------

    def revisar_archivos(self):
        # Respuesta de referencia para una ruta que seguro no existe: muchos
        # sitios devuelven 200 con la página de inicio para cualquier ruta.
        falsa = pedir(f"{self.base}/{secrets.token_hex(8)}-no-existe.txt")
        referencia = falsa.cuerpo[:2000] if falsa.estado == 200 else None

        expuestos = 0
        for ruta, firma, gravedad, que_es in RUTAS_SENSIBLES:
            r = pedir(self.base + ruta)
            if r.estado != 200 or not r.cuerpo:
                continue
            if referencia is not None and r.cuerpo[:2000] == referencia:
                continue
            if not re.search(firma, r.cuerpo[:65536]):
                continue
            expuestos += 1
            self.hallazgo(gravedad, f"Archivo expuesto: {ruta}",
                          f"Cualquiera puede descargarlo. Es: {que_es}.",
                          SOLUCION_ARCHIVO if gravedad != "BAJA" else
                          "Quítalo de la carpeta pública: revela tecnologías y versiones.")
        if not expuestos:
            self.correctos.append(f"Ninguno de los {len(RUTAS_SENSIBLES)} archivos sensibles "
                                  "probados está expuesto")

        abiertas = []
        for carpeta in CARPETAS:
            r = pedir(self.base + carpeta)
            if r.estado == 200 and FIRMA_LISTADO.search(r.cuerpo[:65536]):
                abiertas.append(carpeta)
        if abiertas:
            self.hallazgo("MEDIA", "Listado de carpetas abierto",
                          "Se puede ver el contenido de: " + ", ".join(abiertas),
                          "Desactiva el listado: 'Options -Indexes' en .htaccess (Apache) "
                          "o 'autoindex off' (Nginx).")
        else:
            self.correctos.append("Sin listado de carpetas abierto")

        robots = pedir(self.base + "/robots.txt")
        if robots.estado == 200 and b"<html" not in robots.cuerpo[:500].lower():
            delicadas = re.findall(
                rb"(?im)^\s*Disallow:\s*(\S*(?:admin|backup|respaldo|privad|private|secret|intern)\S*)",
                robots.cuerpo)
            if delicadas:
                rutas = ", ".join(sorted({d.decode("utf-8", "replace") for d in delicadas})[:5])
                self.hallazgo("INFO", "robots.txt anuncia rutas delicadas", f"Rutas: {rutas}",
                              "robots.txt es público y no protege nada. Protege esas rutas "
                              "con inicio de sesión y no las anuncies.")

    # -- Ejecución -----------------------------------------------------------

    def ejecutar(self):
        r = pedir(self.inicio)
        saltos = 0
        while r.estado in (301, 302, 303, 307, 308) and saltos < 5:
            destino = urllib.parse.urljoin(self.inicio, r.cabecera("location") or "")
            partes = urllib.parse.urlsplit(destino)
            if partes.hostname and partes.hostname != self.host:
                # Se sigue solo hacia el mismo dominio o su variante con/sin www.
                sin_www = lambda h: h[4:] if h.startswith("www.") else h
                if sin_www(partes.hostname) != sin_www(self.host):
                    break
                self.host = partes.hostname
                self.base = f"{partes.scheme}://{partes.netloc}"
            self.esquema = partes.scheme
            self.inicio = destino
            r = pedir(destino)
            saltos += 1
        if r.estado == 0:
            if isinstance(getattr(r.error, "reason", None), ssl.SSLCertVerificationError):
                self.hallazgo("ALTA", "El certificado no es válido", str(r.error.reason),
                              "Instala un certificado válido para este dominio.")
                return True
            return False

        self.revisar_https()
        self.revisar_cabeceras(r)
        self.revisar_cookies(r)
        self.revisar_html(r)
        self.revisar_cors()
        self.revisar_archivos()
        return True


ORDEN = {"ALTA": 0, "MEDIA": 1, "BAJA": 2, "INFO": 3}
NOTA_ALCANCE = (
    "Alcance: revisión externa y superficial. No prueba el inicio de sesión, los "
    "permisos entre usuarios ni el código. No sustituye la auditoría completa."
)


def resumen(rev):
    cuenta = {g: sum(1 for h in rev.hallazgos if h["gravedad"] == g) for g in ORDEN}
    if cuenta["ALTA"]:
        veredicto = "FALLA"
    elif cuenta["MEDIA"] or cuenta["BAJA"]:
        veredicto = "PASA CON PENDIENTES"
    else:
        veredicto = "PASA"
    return cuenta, veredicto


def salida_texto(rev):
    cuenta, veredicto = resumen(rev)
    lineas = [f"REVISIÓN EXTERNA DE {rev.inicio}", ""]
    for h in sorted(rev.hallazgos, key=lambda h: ORDEN[h["gravedad"]]):
        lineas.append(f'[{h["gravedad"]}] {h["titulo"]}')
        lineas.append(f'    Qué pasa: {h["detalle"]}')
        lineas.append(f'    Cómo arreglarlo: {h["solucion"]}')
    if rev.hallazgos:
        lineas.append("")
    if rev.correctos:
        lineas.append("CORRECTO")
        lineas += [f"  [OK] {c}" for c in rev.correctos]
        lineas.append("")
    if rev.no_verificado:
        lineas.append("NO SE PUDO VERIFICAR")
        lineas += [f"  [?] {c}" for c in rev.no_verificado]
        lineas.append("")
    lineas.append(
        f'RESULTADO: {veredicto}  (alta {cuenta["ALTA"]}, media {cuenta["MEDIA"]}, '
        f'baja {cuenta["BAJA"]}, informativa {cuenta["INFO"]})'
    )
    lineas.append(NOTA_ALCANCE)
    return "\n".join(lineas)


def salida_md(rev):
    cuenta, veredicto = resumen(rev)
    lineas = [
        f"## Revisión externa de {rev.inicio}", "",
        f'**Resultado: {veredicto}** (alta {cuenta["ALTA"]}, media {cuenta["MEDIA"]}, '
        f'baja {cuenta["BAJA"]}, informativa {cuenta["INFO"]})', "",
    ]
    if rev.hallazgos:
        lineas += ["| Gravedad | Hallazgo | Qué pasa | Cómo arreglarlo |", "|---|---|---|---|"]
        for h in sorted(rev.hallazgos, key=lambda h: ORDEN[h["gravedad"]]):
            celdas = [h["gravedad"], h["titulo"], h["detalle"], h["solucion"]]
            lineas.append("| " + " | ".join(c.replace("|", "\\|") for c in celdas) + " |")
        lineas.append("")
    if rev.correctos:
        lineas += ["**Correcto:**", ""] + [f"- {c}" for c in rev.correctos] + [""]
    if rev.no_verificado:
        lineas += ["**No se pudo verificar:**", ""] + [f"- {c}" for c in rev.no_verificado] + [""]
    lineas += [NOTA_ALCANCE, ""]
    return "\n".join(lineas)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Revisión de seguridad externa de un sitio propio o autorizado."
    )
    p.add_argument("url", help="Dirección del sitio, por ejemplo https://ejemplo.com")
    p.add_argument("--sitio-autorizado", action="store_true",
                   help="Confirmo que el sitio es mío o tengo autorización escrita para revisarlo")
    p.add_argument("--md", metavar="ARCHIVO", help="Guardar el resultado en Markdown")
    p.add_argument("--json", action="store_true", help="Imprimir el resultado en JSON")
    args = p.parse_args(argv)

    if not args.sitio_autorizado:
        print("ERROR: este script solo debe usarse en sitios propios o con autorización "
              "escrita del dueño.\nSi es el caso, repite el comando añadiendo --sitio-autorizado",
              file=sys.stderr)
        return 2
    try:
        rev = Revision(args.url)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    if not rev.ejecutar():
        print(f"ERROR: no se pudo conectar con {args.url}. Revisa la dirección y la conexión.",
              file=sys.stderr)
        return 2

    if args.md:
        with open(args.md, "w", encoding="utf-8") as f:
            f.write(salida_md(rev))
    if args.json:
        cuenta, veredicto = resumen(rev)
        print(json.dumps({"url": rev.inicio, "veredicto": veredicto, "cuenta": cuenta,
                          "hallazgos": rev.hallazgos, "correctos": rev.correctos,
                          "no_verificado": rev.no_verificado}, ensure_ascii=False, indent=2))
    else:
        print(salida_texto(rev))
        if args.md:
            print(f"Guardado Markdown: {args.md}")
    return 1 if any(h["gravedad"] == "ALTA" for h in rev.hallazgos) else 0


if __name__ == "__main__":
    sys.exit(main())
