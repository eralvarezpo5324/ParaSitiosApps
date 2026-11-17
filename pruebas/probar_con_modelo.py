#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probar_con_modelo.py - Comprueba que la skill se comporta bien con un modelo dado.

Sirve para repetir la verificación cada vez que salga un modelo nuevo de Claude.
Lanza conversaciones reales con el comando `claude`, así que consume uso de la
cuenta: con un modelo pequeño es muy poco; con uno grande, bastante más.

Uso, desde la raíz del repositorio:
    python3 pruebas/probar_con_modelo.py                    # modelo por defecto
    python3 pruebas/probar_con_modelo.py --modelo NOMBRE    # un modelo concreto
    python3 pruebas/probar_con_modelo.py --solo color-de-marca

Cada caso se ejecuta en una carpeta temporal con la skill instalada. Se revisa:
  - que la skill se active cuando debe y no se active cuando no debe;
  - que use los scripts en lugar de calcular a mano;
  - que la respuesta contenga lo esencial del comportamiento esperado;
  - que no contenga lo que delataría un error conocido (por ejemplo, preguntar
    el tamaño de una app móvil).

Solo usa la biblioteca estándar de Python 3 y el comando `claude`.
Código de salida: 0 si todo pasa, 1 si algo falla.
"""

import argparse
import concurrent.futures
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / "skills" / "experto"

ESTADO_DE_EJEMPLO = """# Estado del proyecto: Taller Mecánico Ruiz

## Dónde nos quedamos
- **Fase actual:** 4 Diseño de 9
- **Última decisión:** Se aprobó la arquitectura: sitio estático con formulario en PHP, en hosting compartido cPanel.
- **Siguiente paso:** El experto propone la estructura de la página de inicio para aprobación.
- **Esperando:** nada

## Ficha
| Dato | Valor |
|---|---|
| Para quién | Cliente: Taller Mecánico Ruiz |
| Qué es | Página web |
| Ruta | Exprés |
| Países donde opera | México (Monterrey) |
| Dónde se publica | Hosting compartido cPanel |

## Respuestas del descubrimiento
- Acción principal: que escriban por WhatsApp para pedir cita.
- Estilo: serio, cercano, directo.
- Marca: colores azul marino #12305A y amarillo #F2B705.
"""

# nombre, mensaje, ¿debe activarse?, ¿debe usar verificar_color.py?,
# textos que deben aparecer en la respuesta (basta uno de cada grupo),
# textos que no deben aparecer, archivos previos
CASOS = [
    ("proyecto-nuevo",
     "Tengo un cliente nuevo, una dentista en Guadalajara. Quiere una página para que le "
     "agenden citas y aparecer en Google. Ya tiene hosting en Hostinger pero no sé de qué "
     "tipo. ¿Por dónde empezamos?",
     True, False, [["Ronda"], ["Recomendado", "recomendado"]], [], {}),
    ("app-para-cliente-en-usa",
     "un cliente de houston me pide una app para que sus clientes pidan tacos y paguen "
     "ahi mismo, como le hago?",
     True, False, [["Ronda"], ["Recomendado", "recomendado"]], [], {}),
    # La Fase 0 no debe preguntar el tamaño de una app móvil: la ruta es Completa.
    ("app-android",
     "Nuevo proyecto: una app para Android para mi taller de bicicletas, para que los "
     "clientes vean el estado de su reparación. Primero quiero generar el APK para "
     "probarla y después publicarla en Google Play.",
     True, False, [["Ronda"], ["Recomendado", "recomendado"], ["Completa", "completa"]],
     ["tan grande", "Pequeño", "Mediano"], {}),
    ("retomar-proyecto",
     "continuemos",
     True, False, [["Dónde nos quedamos", "dónde nos quedamos"]], [],
     {"docs/proyecto/ESTADO.md": ESTADO_DE_EJEMPLO}),
    ("color-de-marca",
     "Mi cliente quiere usar su naranja de marca #F7931E en los botones con texto blanco, "
     "verde #2E9E44 para los mensajes de éxito y rojo #D9342B para los errores, todo sobre "
     "fondo blanco. ¿Está bien esa combinación?",
     True, True, [["FALLA"], ["#"]], [], {}),
    ("elegir-colores",
     "oye que colores le pongo a la pagina de un despacho de abogados en monterrey? "
     "quieren algo serio pero no aburrido",
     True, True, [["PASA"], ["#"]], [], {}),
    ("ajeno-programacion",
     "ayudame a escribir una funcion en python que ordene una lista de diccionarios por "
     "fecha, las fechas vienen como texto dd/mm/aaaa",
     False, False, [], [], {}),
    ("ajeno-correo",
     "Redacta un correo breve para avisarle a mi contador que este mes le mando las "
     "facturas el dia 20 en lugar del 15.",
     False, False, [], [], {}),
    ("ajeno-hoja-de-calculo",
     "tengo un excel con las ventas del mes y quiero una formula que me sume solo las de "
     "la sucursal norte",
     False, False, [], [], {}),
]


def evaluar(salida, caso):
    """Revisa la salida stream-json de `claude` contra lo que espera el caso.

    Devuelve (paso, problemas, modelo_real).
    """
    _, _, debe_activarse, debe_usar_script, textos, prohibidos, _ = caso
    activada = uso_script = False
    respuesta, modelo_real = "", None
    for linea in salida.splitlines():
        try:
            evento = json.loads(linea)
        except json.JSONDecodeError:
            continue
        if evento.get("type") == "system" and evento.get("subtype") == "init":
            modelo_real = evento.get("model")
        elif evento.get("type") == "assistant":
            for parte in evento["message"]["content"]:
                if parte.get("type") != "tool_use":
                    continue
                if parte["name"] == "Skill":
                    activada = True
                if parte["name"] == "Bash" and "verificar_color.py" in json.dumps(parte["input"]):
                    uso_script = True
        elif evento.get("type") == "result":
            respuesta = evento.get("result") or ""

    problemas = []
    if not respuesta:
        problemas.append("no hubo respuesta")
    if activada != debe_activarse:
        problemas.append("la skill no se activó" if debe_activarse
                         else "la skill se activó sin deber")
    if debe_usar_script and not uso_script:
        problemas.append("no usó verificar_color.py")
    for grupo in textos:
        if not any(texto in respuesta for texto in grupo):
            problemas.append(f'la respuesta no contiene "{grupo[0]}"')
    for texto in prohibidos:
        if texto in respuesta:
            problemas.append(f'la respuesta contiene "{texto}" y no debería')
    return not problemas, problemas, modelo_real


def ejecutar_caso(caso, modelo, limite):
    nombre, mensaje, *_, archivos = caso
    carpeta = Path(tempfile.mkdtemp(prefix=f"experto-{nombre}-"))
    try:
        destino = carpeta / ".claude" / "skills" / "experto"
        shutil.copytree(SKILL, destino, ignore=shutil.ignore_patterns("__pycache__"))
        for ruta, contenido in archivos.items():
            archivo = carpeta / ruta
            archivo.parent.mkdir(parents=True, exist_ok=True)
            archivo.write_text(contenido, encoding="utf-8")
        subprocess.run(["git", "init", "-q", str(carpeta)], capture_output=True)

        comando = ["claude", "-p", mensaje, "--max-turns", "16",
                   "--output-format", "stream-json", "--verbose",
                   "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep,Skill"]
        if modelo:
            comando += ["--model", modelo]
        try:
            salida = subprocess.run(comando, cwd=carpeta, capture_output=True,
                                    text=True, timeout=limite).stdout
        except subprocess.TimeoutExpired:
            return nombre, False, ["se agotó el tiempo"], None

        paso, problemas, modelo_real = evaluar(salida, caso)
        return nombre, paso, problemas, modelo_real
    finally:
        shutil.rmtree(carpeta, ignore_errors=True)


def main(argv=None):
    p = argparse.ArgumentParser(description="Prueba la skill con un modelo de Claude.")
    p.add_argument("--modelo", help="Modelo a probar (por defecto, el de la sesión)")
    p.add_argument("--solo", help="Ejecutar únicamente el caso con este nombre")
    p.add_argument("--paralelo", type=int, default=4, help="Casos simultáneos (por defecto 4)")
    p.add_argument("--limite", type=int, default=480, help="Segundos máximos por caso")
    args = p.parse_args(argv)

    if not shutil.which("claude"):
        print("ERROR: no se encontró el comando claude.", file=sys.stderr)
        return 1
    casos = [c for c in CASOS if not args.solo or c[0] == args.solo]
    if not casos:
        print(f"ERROR: no existe el caso {args.solo}. Casos: {', '.join(c[0] for c in CASOS)}",
              file=sys.stderr)
        return 1

    print(f"Probando {len(casos)} casos con el modelo: {args.modelo or 'por defecto'}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.paralelo) as grupo:
        resultados = list(grupo.map(lambda c: ejecutar_caso(c, args.modelo, args.limite), casos))

    fallas = 0
    for nombre, paso, problemas, modelo_real in resultados:
        estado = "PASA" if paso else "FALLA"
        fallas += not paso
        detalle = "" if paso else "  -> " + "; ".join(problemas)
        print(f"  [{estado}] {nombre}{detalle}")
    modelos = sorted({m for *_, m in resultados if m})
    print(f"Modelo que respondió: {', '.join(modelos) or 'desconocido'}")
    print(f"RESULTADO: {'PASA' if not fallas else 'FALLA'}  "
          f"({len(resultados) - fallas} de {len(resultados)} casos pasan)")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
