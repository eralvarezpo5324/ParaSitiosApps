#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
buscar_secretos.py - Busca contraseñas, llaves y archivos sensibles en un proyecto.

Un secreto que llega al repositorio debe considerarse expuesto: borrarlo en un
commit posterior no lo quita del historial. Por eso este script revisa tanto los
archivos actuales como, con --historial, todo lo que alguna vez se guardó en git.

Uso:
  python3 buscar_secretos.py                 # revisa la carpeta actual
  python3 buscar_secretos.py ruta/proyecto   # revisa otra carpeta
  python3 buscar_secretos.py --historial     # además revisa el historial de git

Para aceptar una línea como excepción consciente, añade en ella el comentario:
  secretos:ignorar

Nunca imprime un secreto completo: solo los primeros caracteres y su longitud.
Solo usa la biblioteca estándar de Python 3.
Códigos de salida: 0 = sin hallazgos de gravedad alta, 1 = hay al menos uno,
2 = error de uso.
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MARCA_IGNORAR = "secretos:ignorar"
TAMANO_MAXIMO = 1_500_000

CARPETAS_OMITIDAS = {
    ".git", "node_modules", "vendor", "dist", "build", ".next", ".nuxt", ".astro",
    ".svelte-kit", ".expo", ".dart_tool", "Pods", "__pycache__", ".venv", "venv",
    ".gradle", ".idea", "coverage", ".turbo", ".cache",
}
ARCHIVOS_OMITIDOS = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "composer.lock",
    "Podfile.lock", "pubspec.lock", "bun.lockb", "Cargo.lock", "poetry.lock",
}
EXTENSIONES_OMITIDAS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico", ".svg", ".pdf",
    ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".webm", ".mp3", ".wav",
    ".zip", ".gz", ".tar", ".7z", ".rar", ".map", ".lottie", ".riv",
}

# (nombre, expresión, gravedad, consejo)
PATRONES = [
    ("Llave privada",
     r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----",
     "ALTA", "Genera una llave nueva y guarda la privada fuera del repositorio."),
    ("Llave de acceso de AWS", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
     "ALTA", "Desactívala en la consola de AWS y crea otra."),
    ("Llave secreta de Stripe (producción)", r"\b[sr]k_live_[0-9A-Za-z]{16,}\b",
     "ALTA", "Revócala en el panel de Stripe y crea otra."),
    ("Secreto de webhook de Stripe", r"\bwhsec_[0-9A-Za-z]{16,}\b",
     "ALTA", "Regenera el secreto del webhook en el panel de Stripe."),
    ("Llave secreta de Stripe (pruebas)", r"\bsk_test_[0-9A-Za-z]{16,}\b",
     "MEDIA", "Aunque sea de pruebas, muévela a una variable de entorno."),
    ("Token de acceso de Mercado Pago (producción)",
     r"\bAPP_USR-[0-9]{8,}-[0-9]{6}-[0-9a-f]{32}-[0-9]+\b",
     "ALTA", "Renueva las credenciales en el panel de Mercado Pago."),
    ("Token de acceso de Mercado Pago (pruebas)",
     r"\bTEST-[0-9]{8,}-[0-9]{6}-[0-9a-f]{32}-[0-9]+\b",
     "MEDIA", "Aunque sea de pruebas, muévelo a una variable de entorno."),
    ("Token de GitHub", r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b",
     "ALTA", "Revócalo en GitHub, en la sección de tokens de acceso."),
    ("Token de Slack", r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b",
     "ALTA", "Revócalo en la administración de Slack."),
    ("Llave de SendGrid", r"\bSG\.[A-Za-z0-9_\-]{16,}\.[A-Za-z0-9_\-]{16,}\b",
     "ALTA", "Elimínala en SendGrid y crea otra."),
    ("Llave de un servicio de IA", r"\bsk-(?:ant|proj)-[A-Za-z0-9_\-]{20,}\b",
     "ALTA", "Revócala en el panel del proveedor y crea otra."),
    ("Token de npm", r"_authToken\s*=\s*[A-Za-z0-9_\-]{20,}",
     "ALTA", "Revoca el token en npm y usa una variable de entorno."),
    ("Llave de API de Google", r"\bAIza[0-9A-Za-z_\-]{35}\b",
     "MEDIA", "Si es la llave web de Firebase es pública por diseño, pero debe "
              "estar restringida por dominio en la consola de Google. Si es otra, cámbiala."),
    ("Llave de Twilio", r"\bSK[0-9a-f]{32}\b",
     "MEDIA", "Si es una llave real de Twilio, revócala y crea otra."),
]
PATRON_JWT = re.compile(
    r"\beyJ[A-Za-z0-9_\-]{10,}\.(eyJ[A-Za-z0-9_\-]{10,})\.[A-Za-z0-9_\-]{10,}\b"
)
PATRON_GENERICO = re.compile(
    r"(?i)\b(pass(?:word|wd)?|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|"
    r"private[_-]?key|client[_-]?secret|clave|contrase[nñ]a)\b[\"']?\s*(?:=>|[:=])\s*"
    r"[\"']([^\"'\s]{8,})[\"']"
)
# Valores que claramente son un ejemplo y no un secreto real (filtro amplio,
# para los hallazgos de gravedad media, donde hay más ruido).
MARCADORES_DE_EJEMPLO = re.compile(
    r"(?i)(example|ejemplo|changeme|change_me|cambiar|cambia|your[_-]|tu[_-]|xxxx|\*{3,}|"
    r"placeholder|password|contrase|secret|secreto|<|>|\$\{|\{\{|process\.env|getenv|"
    r"env\(|usuario|put your unique phrase|password_here|dummy|fake|falso)"
)
# Filtro estricto para los hallazgos de gravedad alta: solo descarta lo que es
# inequívocamente un ejemplo, para no dejar pasar una contraseña real débil.
MARCADORES_ESTRICTOS = re.compile(
    r"(?i)^(pass(word)?|contrase[nñ]a|secreto?|clave|changeme|change_me|root|admin|"
    r"user|usuario|test|demo)$|example|ejemplo|your[_-]|tu[_-]|xxxx|\*{3,}|<|>|\$\{|"
    r"\{\{|%s|password_here|put your unique phrase|placeholder"
)
PATRON_CONEXION = re.compile(
    r"\b(?:mysql|mariadb|postgres(?:ql)?|mongodb(?:\+srv)?|redis|amqps?|s?ftp|smtps?)"
    r"://[^\s:/@'\"<>]+:([^\s@'\"<>]{3,})@[^\s'\"<>]+"
)
PATRON_WP_CONFIG = re.compile(
    r"define\(\s*['\"](?:DB_PASSWORD|AUTH_KEY|SECURE_AUTH_KEY|LOGGED_IN_KEY|NONCE_KEY)"
    r"['\"]\s*,\s*['\"]([^'\"]{6,})['\"]"
)

PATRONES_COMPILADOS = [(n, re.compile(e), g, c) for n, e, g, c in PATRONES]

# (expresión sobre la ruta, gravedad, descripción, consejo)
ARCHIVOS_SENSIBLES = [
    (r"(^|/)\.env(\.[^/]*)?$", "ALTA", "Archivo de variables de entorno",
     "Sácalo del repositorio, añádelo a .gitignore y cambia todo lo que contenía."),
    (r"\.(pem|p12|pfx|jks|keystore|ppk)$", "ALTA", "Archivo de llave o certificado privado",
     "Guárdalo fuera del repositorio."),
    (r"(^|/)id_(rsa|dsa|ecdsa|ed25519)$", "ALTA", "Llave privada de SSH",
     "Genera un par nuevo y guarda la privada fuera del repositorio."),
    (r"(^|/)\.htpasswd$", "ALTA", "Archivo de contraseñas del servidor",
     "Guárdalo fuera del repositorio y fuera de la carpeta pública."),
    (r"(^|/)(sftp-config\.json|\.ftpconfig|\.vscode/sftp\.json)$", "ALTA",
     "Configuración de FTP o SFTP, suele traer la contraseña",
     "Sácalo del repositorio y cambia la contraseña."),
    (r"(^|/)(serviceAccount[^/]*|[^/]*-firebase-adminsdk-[^/]*)\.json$", "ALTA",
     "Cuenta de servicio de Firebase o Google", "Revoca la llave y guárdala fuera del repositorio."),
    (r"(^|/)wp-config\.php$", "MEDIA", "wp-config.php dentro del repositorio",
     "Usa un wp-config de ejemplo sin datos reales y excluye el real."),
    (r"\.(sql|sqlite3?|dump|bak)$|\.sql\.gz$", "MEDIA", "Respaldo o base de datos",
     "Si contiene datos reales de personas, sácalo del repositorio."),
]
ARCHIVOS_DE_EJEMPLO = re.compile(r"\.env\.(example|sample|template|dist|defaults?|ejemplo)$")
ARCHIVOS_SENSIBLES_COMPILADOS = [(re.compile(e), g, d, c) for e, g, d, c in ARCHIVOS_SENSIBLES]


def ocultar(valor, visibles=4):
    """Nunca se imprime un secreto completo.

    Las llaves con prefijo conocido muestran ese prefijo; las contraseñas, nada.
    """
    valor = valor.strip()
    if not visibles:
        return f"({len(valor)} caracteres)"
    return f"{valor[:visibles]}… ({len(valor)} caracteres)"


def es_jwt_delicado(carga_b64):
    """Devuelve 'servicio', 'anonimo' u 'otro' según el contenido del token."""
    try:
        relleno = carga_b64 + "=" * (-len(carga_b64) % 4)
        carga = json.loads(base64.urlsafe_b64decode(relleno))
    except Exception:
        return "otro"
    rol = str(carga.get("role", "")) if isinstance(carga, dict) else ""
    if rol == "service_role":
        return "servicio"
    if rol == "anon":
        return "anonimo"
    return "otro"


def revisar_linea(linea, solo_alta=False):
    """Genera (nombre, gravedad, muestra oculta, consejo) por cada hallazgo."""
    if MARCA_IGNORAR in linea:
        return
    for nombre, patron, gravedad, consejo in PATRONES_COMPILADOS:
        if solo_alta and gravedad != "ALTA":
            continue
        for m in patron.finditer(linea):
            yield nombre, gravedad, ocultar(m.group(0)), consejo
    for m in PATRON_CONEXION.finditer(linea):
        if not MARCADORES_ESTRICTOS.search(m.group(1)):
            yield ("Dirección de conexión con contraseña", "ALTA", ocultar(m.group(1), 0),
                   "Cambia esa contraseña y lee la dirección desde una variable de entorno.")
    for m in PATRON_WP_CONFIG.finditer(linea):
        if not MARCADORES_ESTRICTOS.search(m.group(1)):
            yield ("Contraseña o llave en wp-config", "ALTA", ocultar(m.group(1), 0),
                   "wp-config.php no debe estar en el repositorio. Cambia la contraseña "
                   "de la base de datos y regenera las llaves.")
    for m in PATRON_JWT.finditer(linea):
        tipo = es_jwt_delicado(m.group(1))
        if tipo == "servicio":
            yield ("Llave service_role de Supabase", "ALTA", ocultar(m.group(0)),
                   "Esta llave salta todas las reglas de seguridad. Regénerala en "
                   "Supabase y úsala solo en el servidor.")
        elif tipo == "otro" and not solo_alta:
            yield ("Token JWT", "MEDIA", ocultar(m.group(0)),
                   "Confirma que no sea una sesión real ni una llave de servicio.")
    if solo_alta:
        return
    for m in PATRON_GENERICO.finditer(linea):
        valor = m.group(2)
        if MARCADORES_DE_EJEMPLO.search(valor) or len(set(valor)) < 4:
            continue
        yield (f'Posible secreto en "{m.group(1)}"', "MEDIA", ocultar(valor, 0),
               "Si es real, muévelo a una variable de entorno y cámbialo.")


def listar_archivos(raiz):
    """Archivos a revisar. En un repositorio git respeta .gitignore."""
    try:
        salida = subprocess.run(
            ["git", "-C", str(raiz), "ls-files", "-co", "--exclude-standard", "-z"],
            capture_output=True, check=True,
        ).stdout
        rutas = [r for r in salida.decode("utf-8", "replace").split("\0") if r]
        return [raiz / r for r in rutas], True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    encontrados = []
    for carpeta, subcarpetas, archivos in os.walk(raiz):
        subcarpetas[:] = [s for s in subcarpetas if s not in CARPETAS_OMITIDAS]
        for nombre in archivos:
            encontrados.append(Path(carpeta) / nombre)
    return encontrados, False


def revisar_archivos(raiz):
    hallazgos = []
    archivos, es_git = listar_archivos(raiz)
    for ruta in archivos:
        try:
            relativa = ruta.relative_to(raiz).as_posix()
        except ValueError:
            relativa = ruta.as_posix()
        partes = set(Path(relativa).parts[:-1])
        if partes & CARPETAS_OMITIDAS or not ruta.is_file():
            continue

        if not ARCHIVOS_DE_EJEMPLO.search(relativa):
            for patron, gravedad, descripcion, consejo in ARCHIVOS_SENSIBLES_COMPILADOS:
                if patron.search(relativa):
                    hallazgos.append({
                        "gravedad": gravedad, "tipo": descripcion, "donde": relativa,
                        "muestra": "", "consejo": consejo,
                    })
                    break

        if (ruta.name in ARCHIVOS_OMITIDOS or ruta.suffix.lower() in EXTENSIONES_OMITIDAS
                or ruta.name.endswith(".min.js") or ruta.name.endswith(".min.css")):
            continue
        try:
            if ruta.stat().st_size > TAMANO_MAXIMO:
                continue
            datos = ruta.read_bytes()
        except OSError:
            continue
        if b"\0" in datos[:8000]:
            continue
        for numero, linea in enumerate(datos.decode("utf-8", "replace").splitlines(), 1):
            if len(linea) > 5000:
                continue
            for nombre, gravedad, muestra, consejo in revisar_linea(linea):
                hallazgos.append({
                    "gravedad": gravedad, "tipo": nombre, "donde": f"{relativa}:{numero}",
                    "muestra": muestra, "consejo": consejo,
                })

    if es_git:
        ignorado = subprocess.run(
            ["git", "-C", str(raiz), "check-ignore", "-q", ".env"], capture_output=True
        ).returncode == 0
        if not ignorado:
            hallazgos.append({
                "gravedad": "MEDIA", "tipo": ".gitignore no excluye los archivos .env",
                "donde": ".gitignore", "muestra": "",
                "consejo": "Añade una línea con .env y otra con .env.* (y conserva "
                           "!.env.example) antes de crear cualquier archivo de secretos.",
            })
    return hallazgos, es_git


def revisar_historial(raiz, ya_reportados=()):
    """Busca secretos de gravedad alta en todo lo que alguna vez se guardó en git.

    `ya_reportados` son pares (tipo, muestra) hallados en los archivos actuales,
    para no repetirlos.
    """
    hallazgos, vistos = [], set()
    ya_reportados = set(ya_reportados)
    try:
        proceso = subprocess.Popen(
            ["git", "-C", str(raiz), "log", "-p", "--all", "--no-color", "-U0",
             "--no-ext-diff", "--format=commit %h %ad", "--date=short"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return hallazgos
    commit, archivo = "?", "?"
    for cruda in proceso.stdout:
        linea = cruda.decode("utf-8", "replace").rstrip("\n")
        if linea.startswith("commit "):
            commit = linea[7:]
        elif linea.startswith("+++ "):
            archivo = linea[6:] if linea.startswith("+++ b/") else linea[4:]
        elif linea.startswith("+") and len(linea) < 5000:
            for nombre, gravedad, muestra, consejo in revisar_linea(linea[1:], solo_alta=True):
                clave = (nombre, muestra, archivo)
                if clave in vistos or (nombre, muestra) in ya_reportados:
                    continue
                vistos.add(clave)
                hallazgos.append({
                    "gravedad": gravedad, "tipo": nombre + " (en el historial)",
                    "historial": True,
                    "donde": f"{archivo} en el commit {commit}", "muestra": muestra,
                    "consejo": consejo + " Sigue en el historial aunque ya no esté "
                               "en los archivos: cámbialo de todos modos.",
                })
    proceso.wait()
    return hallazgos


def main(argv=None):
    p = argparse.ArgumentParser(description="Busca secretos y archivos sensibles.")
    p.add_argument("carpeta", nargs="?", default=".", help="Carpeta del proyecto")
    p.add_argument("--historial", action="store_true",
                   help="Revisar también el historial completo de git")
    p.add_argument("--json", action="store_true", help="Imprimir el resultado en JSON")
    args = p.parse_args(argv)

    raiz = Path(args.carpeta).resolve()
    if not raiz.is_dir():
        print(f"ERROR: no existe la carpeta {raiz}", file=sys.stderr)
        return 2

    hallazgos, es_git = revisar_archivos(raiz)
    if args.historial:
        if es_git:
            actuales = {(h["tipo"], h["muestra"]) for h in hallazgos}
            hallazgos += revisar_historial(raiz, actuales)
        else:
            print("AVISO: la carpeta no es un repositorio git; se omite el historial.",
                  file=sys.stderr)

    orden = {"ALTA": 0, "MEDIA": 1}
    hallazgos.sort(key=lambda h: (orden[h["gravedad"]], h.get("historial", False), h["donde"]))
    altas = sum(1 for h in hallazgos if h["gravedad"] == "ALTA")
    medias = len(hallazgos) - altas

    if args.json:
        print(json.dumps({"altas": altas, "medias": medias, "hallazgos": hallazgos},
                         ensure_ascii=False, indent=2))
        return 1 if altas else 0

    print(f"BÚSQUEDA DE SECRETOS en {raiz}")
    print(f'Historial de git: {"revisado" if args.historial and es_git else "no revisado"}')
    print()
    for h in hallazgos:
        print(f'[{h["gravedad"]}] {h["tipo"]}')
        print(f'    Dónde: {h["donde"]}')
        if h["muestra"]:
            print(f'    Valor: {h["muestra"]}')
        print(f'    Qué hacer: {h["consejo"]}')
    if hallazgos:
        print()
    if altas:
        veredicto = "FALLA"
    elif medias:
        veredicto = "PASA CON ADVERTENCIAS"
    else:
        veredicto = "PASA"
    print(f"RESULTADO: {veredicto}  ({altas} de gravedad alta, {medias} de gravedad media)")
    if altas:
        print("Todo secreto encontrado debe cambiarse en el servicio de origen. "
              "Borrarlo del archivo no basta.")
    return 1 if altas else 0


if __name__ == "__main__":
    sys.exit(main())
