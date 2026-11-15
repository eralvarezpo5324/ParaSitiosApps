#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas de los scripts de la skill.

Ejecutar desde la raíz del repositorio:
    python3 -m unittest discover -s pruebas -v

Los secretos de prueba se arman por partes en tiempo de ejecución para que
ningún archivo del repositorio contenga algo con forma de secreto real.
"""

import base64
import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / "skills" / "experto"
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))

import buscar_secretos  # noqa: E402
import revisar_sitio  # noqa: E402
import verificar_color as vc  # noqa: E402


def ejecutar(script, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *map(str, args)],
        capture_output=True, text=True,
    )


class ColorMatematica(unittest.TestCase):
    def test_contraste_valores_conocidos(self):
        blanco = vc.leer_hex("#FFFFFF")
        self.assertAlmostEqual(vc.contraste(vc.leer_hex("#000"), blanco), 21.0, places=2)
        self.assertAlmostEqual(vc.contraste(vc.leer_hex("#767676"), blanco), 4.54, places=2)
        self.assertAlmostEqual(vc.contraste(vc.leer_hex("#777777"), blanco), 4.48, places=2)

    def test_lab_del_rojo(self):
        l, a, b = vc.a_lab((1, 0, 0))
        self.assertAlmostEqual(l, 53.24, places=1)
        self.assertAlmostEqual(a, 80.09, places=1)
        self.assertAlmostEqual(b, 67.20, places=1)

    def test_ciede2000_datos_de_referencia(self):
        # Pares del conjunto de prueba publicado por Sharma, Wu y Dalal (2005).
        casos = [
            ((50, 2.6772, -79.7751), (50, 0, -82.7485), 2.0425),
            ((50, 3.1571, -77.2803), (50, 0, -82.7485), 2.8615),
            ((50, 2.8361, -74.0200), (50, 0, -82.7485), 3.4412),
            ((50, -1.3802, -84.2814), (50, 0, -82.7485), 1.0000),
            ((50, 2.5, 0), (50, 0, -2.5), 4.3065),
            ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
            ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
        ]
        for lab1, lab2, esperado in casos:
            self.assertAlmostEqual(vc.diferencia(lab1, lab2), esperado, places=4)

    def test_las_matrices_conservan_blanco_y_negro(self):
        for tipo in vc.TIPOS_DALTONISMO + ("grises",):
            self.assertEqual(vc.a_hex(vc.simular((1, 1, 1), tipo)), "#FFFFFF")
            self.assertEqual(vc.a_hex(vc.simular((0, 0, 0), tipo)), "#000000")

    def test_ida_y_vuelta_hsl(self):
        for hex_ in ("#1D4ED8", "#B45309", "#0B7285", "#808080", "#FFFFFF"):
            rgb = vc.leer_hex(hex_)
            self.assertEqual(vc.a_hex(vc.desde_hsl(*vc.a_hsl(rgb))), hex_)

    def test_nombres_en_palabras(self):
        self.assertEqual(vc.nombre_color(vc.leer_hex("#FFFFFF")), "blanco")
        self.assertEqual(vc.nombre_color(vc.leer_hex("#000000")), "negro")
        self.assertIn("rojo", vc.nombre_color(vc.leer_hex("#FF0000")))
        self.assertIn("azul", vc.nombre_color(vc.leer_hex("#1D4ED8")))
        self.assertIn("verde", vc.nombre_color(vc.leer_hex("#00A000")))

    def test_colores_no_validos(self):
        for malo in ("#12", "rojo", "#GGGGGG", "#11223344", 5):
            with self.assertRaises(vc.ErrorDeEntrada):
                vc.leer_hex(malo)


class ColorAnalisis(unittest.TestCase):
    def analizar(self, datos, nivel="AA"):
        return vc.analizar(vc.leer_paleta(datos), nivel)

    def test_rojo_y_verde_se_confunden(self):
        r = self.analizar({
            "colores": {"verde": "#2E9E44", "rojo": "#D9342B"},
            "distinguir": [["verde", "rojo"]],
        })
        self.assertEqual(r["distinguir"][0]["estado"], "FALLA")
        self.assertEqual(r["veredicto"], "FALLA")

    def test_las_alternativas_propuestas_resuelven_la_confusion(self):
        datos = {
            "colores": {"fondo": "#FFFFFF", "exito": "#2E9E44", "error": "#D9342B"},
            "pares": [["exito", "fondo", "texto"], ["error", "fondo", "texto"]],
            "distinguir": [["exito", "error"]],
        }
        sugerencias = self.analizar(datos)["distinguir"][0]["sugerencias"]
        self.assertEqual({s["color"] for s in sugerencias}, {"exito", "error"})
        for s in sugerencias:
            corregido = json.loads(json.dumps(datos))
            corregido["colores"][s["color"]] = s["hex"]
            r = self.analizar(corregido)
            self.assertEqual(r["distinguir"][0]["estado"], "PASA", s)
            # El color cambiado no rompe su propio contraste sobre el fondo.
            par = next(p for p in r["pares"] if p["frente"] == s["color"])
            self.assertEqual(par["estado"], "PASA", s)

    def test_comprobacion_rapida_avisa_de_su_limite(self):
        r = ejecutar("verificar_color.py", "--par", "#16203A", "#FFFFFF")
        self.assertEqual(r.returncode, 0)
        self.assertIn('sección "distinguir"', r.stdout)

    def test_azul_y_amarillo_se_distinguen(self):
        r = self.analizar({
            "colores": {"azul": "#1D4ED8", "amarillo": "#FBBF24"},
            "distinguir": [["azul", "amarillo"]],
        })
        self.assertEqual(r["distinguir"][0]["estado"], "PASA")

    def test_la_sugerencia_alcanza_el_minimo(self):
        r = self.analizar({
            "colores": {"gris": "#999999", "fondo": "#FFFFFF"},
            "pares": [["gris", "fondo", "texto"]],
        })
        par = r["pares"][0]
        self.assertEqual(par["estado"], "FALLA")
        sugerido = vc.leer_hex(par["sugerencia"]["hex"])
        self.assertGreaterEqual(vc.contraste(sugerido, vc.leer_hex("#FFFFFF")), 4.5)

    def test_nivel_aaa_es_mas_estricto(self):
        datos = {"colores": {"a": "#767676", "b": "#FFFFFF"}, "pares": [["a", "b", "texto"]]}
        self.assertEqual(self.analizar(datos, "AA")["pares"][0]["estado"], "PASA")
        self.assertEqual(self.analizar(datos, "AAA")["pares"][0]["estado"], "FALLA")

    def test_color_inexistente_en_un_par(self):
        with self.assertRaises(vc.ErrorDeEntrada):
            vc.leer_paleta({"colores": {"a": "#000"}, "pares": [["a", "no-existe"]]})

    def test_la_paleta_de_ejemplo_pasa_limpia(self):
        r = ejecutar("verificar_color.py", SKILL / "plantillas" / "paleta-ejemplo.json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("RESULTADO: PASA  (0 fallas, 0 advertencias)", r.stdout)

    def test_codigos_de_salida_y_archivos(self):
        with tempfile.TemporaryDirectory() as carpeta:
            carpeta = Path(carpeta)
            mala = carpeta / "mala.json"
            mala.write_text(json.dumps({
                "colores": {"gris": "#999999", "fondo": "#FFFFFF"},
                "pares": [["gris", "fondo"]],
            }), encoding="utf-8")
            r = ejecutar("verificar_color.py", mala, "--md", carpeta / "s.md",
                         "--html", carpeta / "s.html")
            self.assertEqual(r.returncode, 1)
            self.assertIn("FALLA", (carpeta / "s.md").read_text(encoding="utf-8"))
            self.assertIn('lang="es"', (carpeta / "s.html").read_text(encoding="utf-8"))
            self.assertEqual(ejecutar("verificar_color.py", carpeta / "no-existe.json").returncode, 2)
            rota = carpeta / "rota.json"
            rota.write_text("{no es json", encoding="utf-8")
            self.assertEqual(ejecutar("verificar_color.py", rota).returncode, 2)


def token_jwt(rol):
    def b64(objeto):
        return base64.urlsafe_b64encode(json.dumps(objeto).encode()).decode().rstrip("=")
    return f'{b64({"alg": "HS256", "typ": "JWT"})}.{b64({"iss": "x", "role": rol})}.{"s" * 43}'


class Secretos(unittest.TestCase):
    def hallazgos(self, linea, solo_alta=False):
        return list(buscar_secretos.revisar_linea(linea, solo_alta))

    def test_detecta_llaves_con_prefijo_conocido(self):
        casos = {
            "Stripe": "sk_" + "live_" + "A1b2C3d4E5f6G7h8I9j0K1l2",
            "AWS": "AKIA" + "ABCDEFGHIJKLMNOP",
            "GitHub": "ghp_" + "abcdefghijklmnopqrstuvwxyz0123456789AB",
        }
        for nombre, valor in casos.items():
            encontrados = self.hallazgos(f'const k = "{valor}";')
            self.assertTrue(any(h[1] == "ALTA" and nombre in h[0] for h in encontrados), nombre)

    def test_nunca_imprime_el_secreto_completo(self):
        valor = "sk_" + "live_" + "A1b2C3d4E5f6G7h8I9j0K1l2"
        for _, _, muestra, _ in self.hallazgos(f'k = "{valor}"'):
            self.assertNotIn(valor, muestra)
            self.assertLessEqual(len(muestra.split("…")[0]), 4)

    def test_conexion_con_contrasena_real_y_de_ejemplo(self):
        real = "mysql://admin:" + "S3cr3t0Real" + "@db.tienda.mx:3306/tienda"
        self.assertTrue(any(h[1] == "ALTA" for h in self.hallazgos(f"$dsn = '{real}';")))
        ejemplo = "mysql://usuario:password@localhost/db"
        self.assertEqual(self.hallazgos(f"$dsn = '{ejemplo}';"), [])

    def test_contrasena_debil_real_en_wp_config_no_se_descarta(self):
        linea = "define('DB_PASSWORD', '" + "Admin" + "1234!" + "');"
        self.assertTrue(any(h[1] == "ALTA" for h in self.hallazgos(linea)))
        relleno = "define('AUTH_KEY', 'put your unique phrase here');"
        self.assertEqual(self.hallazgos(relleno), [])

    def test_llave_de_servicio_de_supabase(self):
        servicio = self.hallazgos(f'const k = "{token_jwt("service_role")}";')
        self.assertTrue(any(h[1] == "ALTA" and "service_role" in h[0] for h in servicio))
        self.assertEqual(self.hallazgos(f'const k = "{token_jwt("anon")}";'), [])

    def test_marcadores_de_ejemplo_y_excepcion(self):
        self.assertEqual(self.hallazgos('api_key = "tu_llave_aqui"'), [])
        self.assertEqual(self.hallazgos('password = "process.env.DB_PASS"'), [])
        real = 'apiKey = "' + "Zx9$kLm2pQ7vR" + '"'
        self.assertTrue(self.hallazgos(real))
        self.assertEqual(self.hallazgos(real + "  // secretos:ignorar"), [])

    def test_repositorio_completo_con_historial(self):
        with tempfile.TemporaryDirectory() as carpeta:
            repo = Path(carpeta)

            def git(*args):
                subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)

            git("init", "-q")
            git("config", "user.email", "prueba@ejemplo.test")
            git("config", "user.name", "prueba")
            git("config", "commit.gpgsign", "false")
            (repo / ".gitignore").write_text(".env\n.env.*\n!.env.example\n", encoding="utf-8")
            (repo / ".env.example").write_text("DB_PASS=\n", encoding="utf-8")
            (repo / "limpio.js").write_text("export const x = 1;\n", encoding="utf-8")
            git("add", "-A")
            git("commit", "-qm", "inicial")

            limpio = ejecutar("buscar_secretos.py", repo, "--historial")
            self.assertEqual(limpio.returncode, 0, limpio.stdout)
            self.assertIn("RESULTADO: PASA", limpio.stdout)

            token = "ghp_" + "abcdefghijklmnopqrstuvwxyz0123456789AB"
            (repo / "viejo.js").write_text(f'const k = "{token}";\n', encoding="utf-8")
            git("add", "-A")
            git("commit", "-qm", "token")
            git("rm", "-q", "viejo.js")
            git("commit", "-qm", "quitar token")

            self.assertEqual(ejecutar("buscar_secretos.py", repo).returncode, 0)
            con_historial = ejecutar("buscar_secretos.py", repo, "--historial")
            self.assertEqual(con_historial.returncode, 1)
            self.assertIn("en el historial", con_historial.stdout)
            self.assertNotIn(token, con_historial.stdout)

            (repo / ".env").write_text("DB_PASS=algo\n", encoding="utf-8")
            git("add", "-f", ".env")
            rastreado = ejecutar("buscar_secretos.py", repo)
            self.assertEqual(rastreado.returncode, 1)
            self.assertIn("Archivo de variables de entorno", rastreado.stdout)


class ServidorDePrueba:
    """Sitio local para probar revisar_sitio.py sin tocar internet."""

    def __init__(self, manejador):
        self.servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
        self.url = f"http://127.0.0.1:{self.servidor.server_address[1]}"
        self.hilo = threading.Thread(target=self.servidor.serve_forever, daemon=True)

    def __enter__(self):
        self.hilo.start()
        return self

    def __exit__(self, *args):
        self.servidor.shutdown()
        self.servidor.server_close()


def manejador(rutas, cabeceras=(), para_todo=None):
    class Manejador(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            ruta = self.path.split("?")[0]
            if ruta in rutas:
                estado, cuerpo = 200, rutas[ruta]
            elif para_todo is not None:
                estado, cuerpo = 200, para_todo
            else:
                estado, cuerpo = 404, b"no encontrado"
            self.send_response(estado)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            for nombre, valor in cabeceras:
                self.send_header(nombre, valor)
            if self.headers.get("Origin") and ("X-Refleja-Origen", "si") in cabeceras:
                self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
                self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)

        def log_message(self, *args):
            pass

    return Manejador


CABECERAS_BUENAS = (
    ("Content-Security-Policy", "default-src 'self'; frame-ancestors 'self'"),
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ("Permissions-Policy", "camera=()"),
    ("Set-Cookie", "sesion_id=abc; HttpOnly; SameSite=Lax; Path=/"),
)
PAGINA = b"<!doctype html><html><head><title>x</title></head><body>hola</body></html>"


class SitioPublicado(unittest.TestCase):
    def setUp(self):
        revisar_sitio.PAUSA = 0

    def revisar(self, url):
        rev = revisar_sitio.Revision(url)
        self.assertTrue(rev.ejecutar())
        return rev

    def titulos(self, rev, gravedad=None):
        return [h["titulo"] for h in rev.hallazgos if gravedad in (None, h["gravedad"])]

    def test_exige_confirmar_autorizacion(self):
        r = ejecutar("revisar_sitio.py", "http://127.0.0.1:9")
        self.assertEqual(r.returncode, 2)
        self.assertIn("--sitio-autorizado", r.stderr)

    def test_sitio_inalcanzable(self):
        r = ejecutar("revisar_sitio.py", "http://127.0.0.1:9", "--sitio-autorizado")
        self.assertEqual(r.returncode, 2)

    def test_detecta_archivos_expuestos_y_cabeceras_faltantes(self):
        rutas = {
            "/": b"<html><form action='http://x.test/entrar'></form></html>",
            "/.env": b"DB_PASSWORD=abc12345\nAPP_KEY=zzz\n",
            "/.git/config": b"[core]\n\trepositoryformatversion = 0\n",
            "/backup.sql": b"CREATE TABLE usuarios (id int);\n",
            "/uploads/": b"<html><title>Index of /uploads</title></html>",
        }
        with ServidorDePrueba(manejador(rutas)) as sitio:
            rev = self.revisar(sitio.url)
        altas = self.titulos(rev, "ALTA")
        for esperado in ("Archivo expuesto: /.env", "Archivo expuesto: /.git/config",
                         "Archivo expuesto: /backup.sql",
                         "Un formulario envía datos por HTTP sin cifrar"):
            self.assertIn(esperado, altas)
        todos = self.titulos(rev)
        self.assertIn("Listado de carpetas abierto", todos)
        self.assertIn("Falta la política de seguridad de contenido (CSP)", todos)
        self.assertIn("El sitio puede incrustarse en páginas ajenas (clickjacking)", todos)

    def test_sitio_bien_configurado_no_da_falsos_positivos(self):
        # Responde 200 con la misma página a cualquier ruta, como muchas
        # aplicaciones de una sola página. No debe reportar archivos expuestos.
        with ServidorDePrueba(manejador({}, CABECERAS_BUENAS, para_todo=PAGINA)) as sitio:
            rev = self.revisar(sitio.url)
        self.assertEqual(self.titulos(rev, "ALTA"), [])
        self.assertEqual(self.titulos(rev, "MEDIA"), [])
        self.assertFalse(any("expuesto" in t for t in self.titulos(rev)))
        self.assertTrue(any("bien protegida" in c for c in rev.correctos))

    def test_cookie_de_sesion_sin_proteccion(self):
        cabeceras = CABECERAS_BUENAS[:-1] + (("Set-Cookie", "PHPSESSID=abc; Path=/"),)
        with ServidorDePrueba(manejador({"/": PAGINA}, cabeceras)) as sitio:
            rev = self.revisar(sitio.url)
        self.assertTrue(any("PHPSESSID" in t for t in self.titulos(rev, "MEDIA")))

    def test_cors_que_refleja_el_origen_con_credenciales(self):
        cabeceras = CABECERAS_BUENAS + (("X-Refleja-Origen", "si"),)
        with ServidorDePrueba(manejador({"/": PAGINA}, cabeceras)) as sitio:
            rev = self.revisar(sitio.url)
        self.assertIn("CORS acepta cualquier origen con credenciales", self.titulos(rev, "ALTA"))


class EstructuraDeLaSkill(unittest.TestCase):
    def test_los_archivos_citados_existen(self):
        import re
        texto = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for carpeta in ("referencias", "plantillas", "revisores", "scripts"):
            for nombre in set(re.findall(rf"`(?:{carpeta}/)?([\w-]+\.(?:md|py|json))`", texto)):
                candidatos = list(SKILL.rglob(nombre))
                if nombre in ("paleta.json", "brief-propuesta.md", "preguntas-cliente.md",
                              "reporte-seguridad.md", "manual-entrega.md",
                              "guia-diseno-color.md", "arquitectura.md", "ESTADO.md",
                              "CLAUDE.md"):
                    continue  # también son nombres de archivos del proyecto del cliente
                self.assertTrue(candidatos, f"SKILL.md cita {nombre} y no existe")

    def test_guias_citadas_entre_si_existen(self):
        import re
        nombres = {p.name for p in SKILL.rglob("*") if p.is_file()}
        del_proyecto = {"paleta.json", "paleta-oscuro.json", "paleta-verificada.md",
                        "paleta-verificada.html", "CLAUDE.md", "llms.txt", "robots.txt",
                        "sitemap.xml", "hooks.json", "manifest.json", "sftp.json",
                        "sftp-config.json", "installed.json", "package.json",
                        "composer.json", "package-lock.json", "guia-color.md"}
        for guia in list((SKILL / "referencias").glob("*.md")) + list((SKILL / "revisores").glob("*.md")):
            texto = guia.read_text(encoding="utf-8")
            for nombre in set(re.findall(r"`(?:[\w/-]+/)?([\w-]+\.(?:md|py|json))`", texto)):
                if nombre in del_proyecto:
                    continue
                self.assertIn(nombre, nombres, f"{guia.name} cita {nombre} y no existe")

    def test_un_solo_skill_md_y_frontmatter_valido(self):
        self.assertEqual(len(list(SKILL.rglob("SKILL.md"))), 1)
        texto = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(texto.startswith("---\nname: experto\ndescription: "))
        descripcion = texto.split("\n")[2][len("description: "):]
        self.assertLessEqual(len(descripcion), 1024)
        self.assertLess(len(texto.splitlines()), 500)

    def test_la_skill_no_fija_ningun_modelo(self):
        cabecera = (SKILL / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
        self.assertNotIn("model:", cabecera)
        self.assertNotIn("effort:", cabecera)


if __name__ == "__main__":
    unittest.main(verbosity=2)
