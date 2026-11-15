#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar_color.py - Verifica una paleta de colores con cálculo, no con la vista.

Qué comprueba:
  1. Contraste WCAG 2.x de cada par frente/fondo.
  2. El mismo contraste simulando protanopia, deuteranopia y tritanopia.
  3. Que los colores que deben distinguirse entre sí (por ejemplo éxito y error)
     sigan siendo distintos con cada tipo de daltonismo y en escala de grises.
  4. Describe cada color con palabras y dice cómo se ve con daltonismo rojo-verde.

Uso:
  python3 verificar_color.py paleta.json
  python3 verificar_color.py paleta.json --md guia-color.md --html vista.html
  python3 verificar_color.py --par "#1B1F3B" "#FFFFFF"
  python3 verificar_color.py --describir "#C0392B"

Formato de paleta.json: ver plantillas/paleta-ejemplo.json.

Solo usa la biblioteca estándar de Python 3.
Códigos de salida: 0 = pasa, 1 = hay fallas, 2 = error en los datos de entrada.
"""

import argparse
import html
import json
import math
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Umbrales
# ---------------------------------------------------------------------------

# Contraste mínimo WCAG 2.2 por tipo de par.
UMBRALES = {
    "AA": {"texto": 4.5, "texto-grande": 3.0, "interfaz": 3.0},
    "AAA": {"texto": 7.0, "texto-grande": 4.5, "interfaz": 3.0},
}
DESCRIPCION_TIPO = {
    "texto": "texto normal",
    "texto-grande": "texto grande (24 px, o 19 px en negrita)",
    "interfaz": "borde, icono o control",
}
# Por debajo de esto, un par es ilegible para casi cualquiera.
CONTRASTE_ILEGIBLE = 3.0

# Diferencia de color (CIEDE2000) entre dos colores que deben distinguirse.
DIFERENCIA_FALLA = 10.0        # por debajo: se confunden
DIFERENCIA_ADVERTENCIA = 20.0  # por debajo: se distinguen con dificultad
# Diferencia de claridad (L*) mínima para distinguirse en escala de grises.
CLARIDAD_ADVERTENCIA = 15.0

# Matrices de Machado, Oliveira y Fernandes (2009), severidad 1.0.
# Se aplican sobre RGB lineal.
MATRICES = {
    "protanopia": (
        (0.152286, 1.052583, -0.204868),
        (0.114503, 0.786281, 0.099216),
        (-0.003882, -0.048116, 1.051998),
    ),
    "deuteranopia": (
        (0.367322, 0.860646, -0.227968),
        (0.280085, 0.672501, 0.047413),
        (-0.011820, 0.042940, 0.968881),
    ),
    "tritanopia": (
        (1.255528, -0.076749, -0.178779),
        (-0.078411, 0.930809, 0.147602),
        (0.004733, 0.691367, 0.303900),
    ),
}
TIPOS_DALTONISMO = ("protanopia", "deuteranopia", "tritanopia")
ROJO_VERDE = ("protanopia", "deuteranopia")


class ErrorDeEntrada(Exception):
    """Los datos de entrada no se pueden interpretar."""


# ---------------------------------------------------------------------------
# Conversión de color
# ---------------------------------------------------------------------------

def leer_hex(texto):
    """'#RRGGBB' o '#RGB' -> (r, g, b) con valores de 0 a 1."""
    if not isinstance(texto, str):
        raise ErrorDeEntrada(f"Se esperaba un color en texto, llegó: {texto!r}")
    valor = texto.strip().lstrip("#")
    if len(valor) == 3:
        valor = "".join(c * 2 for c in valor)
    if len(valor) == 8:
        raise ErrorDeEntrada(
            f"El color {texto!r} tiene transparencia. Escribe el color final "
            "que resulta sobre su fondo (6 dígitos)."
        )
    if len(valor) != 6:
        raise ErrorDeEntrada(f"Color no válido: {texto!r}. Usa el formato #RRGGBB.")
    try:
        return tuple(int(valor[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        raise ErrorDeEntrada(f"Color no válido: {texto!r}. Usa el formato #RRGGBB.")


def a_hex(rgb):
    return "#" + "".join(f"{round(min(1, max(0, c)) * 255):02X}" for c in rgb)


def a_lineal(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def desde_lineal(c):
    c = min(1.0, max(0.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def luminancia(rgb):
    r, g, b = (a_lineal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(rgb1, rgb2):
    l1, l2 = luminancia(rgb1), luminancia(rgb2)
    claro, oscuro = max(l1, l2), min(l1, l2)
    return (claro + 0.05) / (oscuro + 0.05)


def simular(rgb, tipo):
    """Devuelve el color como lo percibe una persona con ese tipo de daltonismo."""
    lineal = [a_lineal(c) for c in rgb]
    if tipo == "grises":
        y = 0.2126 * lineal[0] + 0.7152 * lineal[1] + 0.0722 * lineal[2]
        return tuple(desde_lineal(y) for _ in range(3))
    m = MATRICES[tipo]
    return tuple(
        desde_lineal(m[i][0] * lineal[0] + m[i][1] * lineal[1] + m[i][2] * lineal[2])
        for i in range(3)
    )


def a_lab(rgb):
    r, g, b = (a_lineal(c) for c in rgb)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.0
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def diferencia(lab1, lab2):
    """Diferencia de color CIEDE2000 entre dos colores en CIELAB."""
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c1, c2 = math.hypot(a1, b1), math.hypot(a2, b2)
    cm7 = ((c1 + c2) / 2) ** 7
    g = 0.5 * (1 - math.sqrt(cm7 / (cm7 + 25 ** 7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if c1p else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if c2p else 0.0

    dl = l2 - l1
    dc = c2p - c1p
    if c1p * c2p == 0:
        dh = 0.0
    else:
        dh = h2p - h1p
        if dh > 180:
            dh -= 360
        elif dh < -180:
            dh += 360
    dhh = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh / 2))

    lm = (l1 + l2) / 2
    cm = (c1p + c2p) / 2
    if c1p * c2p == 0:
        hm = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hm = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hm = (h1p + h2p + 360) / 2
    else:
        hm = (h1p + h2p - 360) / 2

    t = (1 - 0.17 * math.cos(math.radians(hm - 30))
         + 0.24 * math.cos(math.radians(2 * hm))
         + 0.32 * math.cos(math.radians(3 * hm + 6))
         - 0.20 * math.cos(math.radians(4 * hm - 63)))
    dtheta = 30 * math.exp(-(((hm - 275) / 25) ** 2))
    rc = 2 * math.sqrt(cm ** 7 / (cm ** 7 + 25 ** 7))
    sl = 1 + (0.015 * (lm - 50) ** 2) / math.sqrt(20 + (lm - 50) ** 2)
    sc = 1 + 0.045 * cm
    sh = 1 + 0.015 * cm * t
    rt = -math.sin(math.radians(2 * dtheta)) * rc
    return math.sqrt(
        (dl / sl) ** 2 + (dc / sc) ** 2 + (dhh / sh) ** 2
        + rt * (dc / sc) * (dhh / sh)
    )


def a_hsl(rgb):
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    l = (mx + mn) / 2
    if mx == mn:
        return (0.0, 0.0, l)
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return (h * 60, s, l)


def desde_hsl(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    sector = int(h // 60) % 6
    r, g, b = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][sector]
    return (r + m, g + m, b + m)


# ---------------------------------------------------------------------------
# Describir un color con palabras
# ---------------------------------------------------------------------------

def nombre_color(rgb):
    """Nombre aproximado en español, para quien no puede fiarse de su vista."""
    claridad, a, b = a_lab(rgb)
    croma = math.hypot(a, b)
    tono, _, _ = a_hsl(rgb)

    if croma < 8:
        if claridad >= 97:
            return "blanco"
        if claridad >= 85:
            return "gris muy claro"
        if claridad >= 65:
            return "gris claro"
        if claridad >= 40:
            return "gris medio"
        if claridad >= 20:
            return "gris oscuro"
        if claridad >= 6:
            return "gris casi negro"
        return "negro"

    if tono < 12 or tono >= 345:
        base = "rosa" if claridad > 72 else "rojo"
    elif tono < 40:
        base = "café" if claridad < 45 else "naranja"
    elif tono < 65:
        if claridad < 40:
            base = "café oliva"
        elif claridad < 62:
            base = "mostaza"
        else:
            base = "amarillo"
    elif tono < 90:
        base = "verde lima"
    elif tono < 150:
        base = "verde"
    elif tono < 175:
        base = "verde azulado"
    elif tono < 200:
        base = "turquesa"
    elif tono < 250:
        base = "azul"
    elif tono < 280:
        base = "violeta"
    elif tono < 320:
        base = "morado"
    else:
        base = "rosa" if claridad > 62 else "magenta"

    if claridad > 85:
        grado = " muy claro"
    elif claridad > 70:
        grado = " claro"
    elif claridad >= 45:
        grado = ""
    elif claridad >= 25:
        grado = " oscuro"
    else:
        grado = " muy oscuro"

    if croma < 25:
        viveza = " grisáceo"
    elif croma > 70:
        viveza = " intenso"
    else:
        viveza = ""
    return base + grado + viveza


def como_se_ve(rgb):
    """Texto que explica cómo percibe ese color alguien con daltonismo rojo-verde."""
    lab = a_lab(rgb)
    partes = []
    for tipo in ROJO_VERDE:
        sim = simular(rgb, tipo)
        cambio = diferencia(lab, a_lab(sim))
        nombre = nombre_color(sim)
        partes.append((tipo, nombre, cambio))
    if all(c < 5 for _, _, c in partes):
        return "se ve prácticamente igual"
    if partes[0][1] == partes[1][1]:
        return f"se ve como {partes[0][1]}"
    return "; ".join(f"con {t} se ve como {n}" for t, n, _ in partes)


# ---------------------------------------------------------------------------
# Sugerir una corrección
# ---------------------------------------------------------------------------

def sugerir(frente, fondo, objetivo):
    """Busca el color más parecido a `frente` (mismo tono) que alcance el objetivo.

    Devuelve (rgb, contraste, 'más oscuro' | 'más claro') o None.
    """
    h, s, l = a_hsl(frente)
    oscurecer = luminancia(frente) < luminancia(fondo)
    for direccion in (oscurecer, not oscurecer):
        paso = -0.005 if direccion else 0.005
        nuevo_l = l
        while 0.0 <= nuevo_l <= 1.0:
            candidato = desde_hsl(h, s, min(1.0, max(0.0, nuevo_l)))
            # Se redondea a hex porque ese es el color que se usará de verdad.
            candidato = leer_hex(a_hex(candidato))
            c = contraste(candidato, fondo)
            if c >= objetivo + 0.05:
                return candidato, c, ("más oscuro" if direccion else "más claro")
            nuevo_l += paso
    return None


def separacion(rgb1, rgb2):
    """La menor diferencia entre dos colores, con visión típica y con cada daltonismo."""
    valores = [diferencia(a_lab(rgb1), a_lab(rgb2))]
    valores += [
        diferencia(a_lab(simular(rgb1, t)), a_lab(simular(rgb2, t)))
        for t in TIPOS_DALTONISMO
    ]
    return min(valores)


def sugerir_distinguir(nombre, otro, paleta, nivel):
    """Busca el color más parecido a `nombre` que se distinga bien de `otro`.

    Prueba cambios pequeños de tono y de claridad, y descarta los que rompan
    algún contraste o alguna otra distinción en la que participa `nombre`.
    Devuelve el color (r, g, b) o None.
    """
    colores = paleta["colores"]
    original = colores[nombre]["rgb"]
    rival = colores[otro]["rgb"]
    lab_original = a_lab(original)
    claridad_rival = a_lab(rival)[0]
    h, s, l = a_hsl(original)

    pares = [(f, b, UMBRALES[nivel][t]) for f, b, t in paleta["pares"] if nombre in (f, b)]
    terceros = []
    for x, y in paleta["distinguir"]:
        if nombre in (x, y) and otro not in (x, y):
            tercero = colores[y if x == nombre else x]["rgb"]
            terceros.append((tercero, min(DIFERENCIA_ADVERTENCIA, separacion(original, tercero))))

    def no_rompe_nada(candidato):
        for frente, fondo, minimo in pares:
            f = candidato if frente == nombre else colores[frente]["rgb"]
            b = candidato if fondo == nombre else colores[fondo]["rgb"]
            if contraste(f, b) < minimo:
                return False
            if min(contraste(simular(f, t), simular(b, t)) for t in TIPOS_DALTONISMO) < minimo:
                return False
        return all(separacion(candidato, t) >= limite for t, limite in terceros)

    candidatos = []
    for cambio_tono in range(-120, 121, 5):
        for paso in range(-12, 13):
            claridad = l + paso * 0.025
            if (cambio_tono == 0 and paso == 0) or not 0.03 <= claridad <= 0.97:
                continue
            rgb = leer_hex(a_hex(desde_hsl((h + cambio_tono) % 360, s, claridad)))
            candidatos.append((diferencia(lab_original, a_lab(rgb)), rgb))
    candidatos.sort(key=lambda c: c[0])  # primero los más parecidos al original

    # Se intenta primero una corrección limpia; si no existe, una aceptable.
    for minima_diferencia, minima_claridad in (
        (DIFERENCIA_ADVERTENCIA, CLARIDAD_ADVERTENCIA),
        (DIFERENCIA_ADVERTENCIA, 0),
        (DIFERENCIA_FALLA, 0),
    ):
        for _, rgb in candidatos:
            if abs(a_lab(rgb)[0] - claridad_rival) < minima_claridad:
                continue
            if separacion(rgb, rival) < minima_diferencia:
                continue
            if no_rompe_nada(rgb):
                return rgb
    return None


# ---------------------------------------------------------------------------
# Análisis
# ---------------------------------------------------------------------------

def leer_paleta(datos):
    if not isinstance(datos, dict) or "colores" not in datos:
        raise ErrorDeEntrada('Falta la sección "colores" en el archivo de paleta.')
    colores = {}
    for nombre, valor in datos["colores"].items():
        if isinstance(valor, dict):
            if "hex" not in valor:
                raise ErrorDeEntrada(f'Al color "{nombre}" le falta el campo "hex".')
            colores[nombre] = {"rgb": leer_hex(valor["hex"]), "uso": valor.get("uso", "")}
        else:
            colores[nombre] = {"rgb": leer_hex(valor), "uso": ""}

    def existe(nombre, donde):
        if nombre not in colores:
            raise ErrorDeEntrada(
                f'{donde} menciona el color "{nombre}", que no está en "colores". '
                f"Colores definidos: {', '.join(colores)}."
            )

    pares = []
    for i, par in enumerate(datos.get("pares", []), 1):
        if isinstance(par, dict):
            frente, fondo, tipo = par.get("frente"), par.get("fondo"), par.get("tipo", "texto")
        elif isinstance(par, (list, tuple)) and len(par) in (2, 3):
            frente, fondo = par[0], par[1]
            tipo = par[2] if len(par) == 3 else "texto"
        else:
            raise ErrorDeEntrada(f"El par número {i} no tiene el formato esperado.")
        existe(frente, f"El par número {i}")
        existe(fondo, f"El par número {i}")
        if tipo not in UMBRALES["AA"]:
            raise ErrorDeEntrada(
                f'El par número {i} tiene tipo "{tipo}". '
                f"Tipos válidos: {', '.join(UMBRALES['AA'])}."
            )
        pares.append((frente, fondo, tipo))

    distinguir = []
    for i, grupo in enumerate(datos.get("distinguir", []), 1):
        if not isinstance(grupo, (list, tuple)) or len(grupo) < 2:
            raise ErrorDeEntrada(
                f'El grupo número {i} de "distinguir" necesita al menos dos colores.'
            )
        for nombre in grupo:
            existe(nombre, f'El grupo número {i} de "distinguir"')
        # Un grupo de tres o más se revisa por parejas.
        for a in range(len(grupo)):
            for b in range(a + 1, len(grupo)):
                distinguir.append((grupo[a], grupo[b]))

    return {
        "nombre": datos.get("nombre", "Paleta"),
        "colores": colores,
        "pares": pares,
        "distinguir": distinguir,
    }


def analizar(paleta, nivel="AA"):
    colores = paleta["colores"]
    resultado = {
        "nombre": paleta["nombre"],
        "nivel": nivel,
        "colores": [],
        "pares": [],
        "distinguir": [],
    }

    for nombre, info in colores.items():
        rgb = info["rgb"]
        resultado["colores"].append({
            "nombre": nombre,
            "hex": a_hex(rgb),
            "uso": info["uso"],
            "descripcion": nombre_color(rgb),
            "rojo_verde": como_se_ve(rgb),
            "simulado": {t: a_hex(simular(rgb, t)) for t in TIPOS_DALTONISMO + ("grises",)},
        })

    for frente, fondo, tipo in paleta["pares"]:
        f, b = colores[frente]["rgb"], colores[fondo]["rgb"]
        minimo = UMBRALES[nivel][tipo]
        base = contraste(f, b)
        simulados = {t: contraste(simular(f, t), simular(b, t)) for t in TIPOS_DALTONISMO}
        peor_tipo = min(simulados, key=simulados.get)
        peor = simulados[peor_tipo]

        estado, notas, sugerencia = "PASA", [], None
        if base < minimo:
            estado = "FALLA"
            notas.append(f"El contraste es {base:.2f} y el mínimo es {minimo}.")
            s = sugerir(f, b, minimo)
            if s:
                sugerencia = {"color": frente, "hex": a_hex(s[0]),
                              "contraste": round(s[1], 2), "cambio": s[2]}
            else:
                notas.append(
                    f'Ningún ajuste de "{frente}" alcanza el mínimo sobre este fondo. '
                    f'Cambia "{fondo}".'
                )
        elif peor < min(minimo, CONTRASTE_ILEGIBLE):
            estado = "FALLA"
            notas.append(
                f"Con {peor_tipo} el contraste baja a {peor:.2f}, por debajo de "
                f"{CONTRASTE_ILEGIBLE}: resulta ilegible."
            )
        elif peor < minimo:
            estado = "ADVERTENCIA"
            notas.append(
                f"Cumple la norma, pero con {peor_tipo} el contraste baja a "
                f"{peor:.2f} (mínimo {minimo}). Conviene dar más margen."
            )

        resultado["pares"].append({
            "frente": frente, "fondo": fondo, "tipo": tipo, "minimo": minimo,
            "contraste": round(base, 2),
            "simulado": {t: round(v, 2) for t, v in simulados.items()},
            "estado": estado, "notas": notas, "sugerencia": sugerencia,
        })

    for a, b in paleta["distinguir"]:
        ra, rb = colores[a]["rgb"], colores[b]["rgb"]
        base = diferencia(a_lab(ra), a_lab(rb))
        simulados = {
            t: diferencia(a_lab(simular(ra, t)), a_lab(simular(rb, t)))
            for t in TIPOS_DALTONISMO
        }
        claridad = abs(a_lab(ra)[0] - a_lab(rb)[0])
        todos = dict(simulados, **{"visión típica": base})
        peor_tipo = min(todos, key=todos.get)
        peor = todos[peor_tipo]

        estado, notas = "PASA", []
        if peor < DIFERENCIA_FALLA:
            estado = "FALLA"
            notas.append(
                f"Con {peor_tipo} la diferencia es {peor:.0f} (mínimo "
                f"{DIFERENCIA_FALLA:.0f}): se confunden. Cambia la claridad de uno "
                "de los dos, o cambia uno hacia azul o amarillo."
            )
        elif peor < DIFERENCIA_ADVERTENCIA:
            estado = "ADVERTENCIA"
            notas.append(
                f"Con {peor_tipo} la diferencia es {peor:.0f}: se distinguen con "
                "dificultad. Acompáñalos siempre con icono o texto."
            )
        if claridad < CLARIDAD_ADVERTENCIA and estado == "PASA":
            estado = "ADVERTENCIA"
        if claridad < CLARIDAD_ADVERTENCIA:
            notas.append(
                f"Tienen casi la misma claridad (diferencia {claridad:.0f}): en "
                "escala de grises o impresos en blanco y negro no se distinguen."
            )

        sugerencias = []
        if estado != "PASA":
            for cambia, otro in ((a, b), (b, a)):
                propuesto = sugerir_distinguir(cambia, otro, paleta, nivel)
                if propuesto:
                    sugerencias.append({"color": cambia, "hex": a_hex(propuesto),
                                        "descripcion": nombre_color(propuesto)})

        resultado["distinguir"].append({
            "a": a, "b": b,
            "diferencia": round(base, 1),
            "simulado": {t: round(v, 1) for t, v in simulados.items()},
            "claridad": round(claridad, 1),
            "estado": estado, "notas": notas, "sugerencias": sugerencias,
        })

    estados = [p["estado"] for p in resultado["pares"] + resultado["distinguir"]]
    resultado["fallas"] = estados.count("FALLA")
    resultado["advertencias"] = estados.count("ADVERTENCIA")
    if resultado["fallas"]:
        resultado["veredicto"] = "FALLA"
    elif resultado["advertencias"]:
        resultado["veredicto"] = "PASA CON ADVERTENCIAS"
    else:
        resultado["veredicto"] = "PASA"
    return resultado


# ---------------------------------------------------------------------------
# Salidas
# ---------------------------------------------------------------------------

RECORDATORIO = (
    "Recordatorio: el color nunca debe ser la única señal. Todo estado "
    "(error, éxito, activo, seleccionado) lleva además texto, icono o forma."
)


def cuenta(r):
    f, a = r["fallas"], r["advertencias"]
    return (f'{f} {"falla" if f == 1 else "fallas"}, '
            f'{a} {"advertencia" if a == 1 else "advertencias"}')


def texto_sugerencias_distinguir(d):
    """Frase con las alternativas calculadas para una pareja que se confunde."""
    if not d["sugerencias"]:
        return ("No se encontró un ajuste pequeño que lo resuelva. Elige un color "
                "de otra familia para uno de los dos.")
    opciones = [f'cambia "{x["color"]}" a {x["hex"]} ({x["descripcion"]})'
                for x in d["sugerencias"]]
    return ("Sugerencia: " + ", o ".join(opciones) + ". Basta uno de los cambios. "
            "Respeta los contrastes de la paleta; vuelve a verificar después.")


def texto_sugerencia(s):
    return (f'Sugerencia: cambia "{s["color"]}" a {s["hex"]} (mismo tono, '
            f'{s["cambio"]}); el contraste sube a {s["contraste"]}.')


def salida_texto(r):
    lineas = [f'PALETA: {r["nombre"]}   (nivel WCAG {r["nivel"]})', ""]

    lineas.append("COLORES")
    for c in r["colores"]:
        uso = f'  | uso: {c["uso"]}' if c["uso"] else ""
        lineas.append(f'  {c["nombre"]}  {c["hex"]}  {c["descripcion"]}{uso}')
        lineas.append(f'      con daltonismo rojo-verde {c["rojo_verde"]}')
    lineas.append("")

    if r["pares"]:
        lineas.append("CONTRASTE (frente sobre fondo)")
        for p in r["pares"]:
            lineas.append(
                f'  [{p["estado"]}] {p["frente"]} sobre {p["fondo"]}  '
                f'({DESCRIPCION_TIPO[p["tipo"]]}, mínimo {p["minimo"]}): '
                f'contraste {p["contraste"]}'
            )
            sim = " | ".join(f"{t} {v}" for t, v in p["simulado"].items())
            lineas.append(f"      simulado: {sim}")
            for n in p["notas"]:
                lineas.append(f"      {n}")
            if p["sugerencia"]:
                lineas.append(f'      {texto_sugerencia(p["sugerencia"])}')
        lineas.append("")

    if r["distinguir"]:
        lineas.append("COLORES QUE DEBEN DISTINGUIRSE ENTRE SÍ")
        for d in r["distinguir"]:
            sim = " | ".join(f"{t} {v}" for t, v in d["simulado"].items())
            lineas.append(
                f'  [{d["estado"]}] {d["a"]} y {d["b"]}: diferencia '
                f'{d["diferencia"]} | {sim} | claridad {d["claridad"]}'
            )
            for n in d["notas"]:
                lineas.append(f"      {n}")
            if d["estado"] != "PASA":
                lineas.append(f"      {texto_sugerencias_distinguir(d)}")
        lineas.append("")

    lineas.append(f'RESULTADO: {r["veredicto"]}  ({cuenta(r)})')
    lineas.append(RECORDATORIO)
    return "\n".join(lineas)


def salida_md(r):
    lineas = [
        f'## Paleta verificada: {r["nombre"]}',
        "",
        f'**Resultado: {r["veredicto"]}** (nivel WCAG {r["nivel"]}; {cuenta(r)}). '
        "Verificado por cálculo, no a ojo.",
        "",
        "### Colores",
        "",
        "| Nombre | Código | Se describe como | Para qué se usa | Con daltonismo rojo-verde |",
        "|---|---|---|---|---|",
    ]
    for c in r["colores"]:
        lineas.append(
            f'| {c["nombre"]} | `{c["hex"]}` | {c["descripcion"]} | '
            f'{c["uso"] or "-"} | {c["rojo_verde"]} |'
        )
    if r["pares"]:
        lineas += [
            "", "### Contraste", "",
            "| Combinación | Uso | Contraste | Mínimo | Peor caso con daltonismo | Resultado |",
            "|---|---|---|---|---|---|",
        ]
        for p in r["pares"]:
            peor = min(p["simulado"].values())
            lineas.append(
                f'| {p["frente"]} sobre {p["fondo"]} | {DESCRIPCION_TIPO[p["tipo"]]} | '
                f'{p["contraste"]} | {p["minimo"]} | {peor} | {p["estado"]} |'
            )
    if r["distinguir"]:
        lineas += [
            "", "### Colores que deben distinguirse entre sí", "",
            "| Colores | Diferencia | Peor caso con daltonismo | Diferencia de claridad | Resultado |",
            "|---|---|---|---|---|",
        ]
        for d in r["distinguir"]:
            peor = min(d["simulado"].values())
            lineas.append(
                f'| {d["a"]} y {d["b"]} | {d["diferencia"]} | {peor} | '
                f'{d["claridad"]} | {d["estado"]} |'
            )
    notas = []
    for p in r["pares"]:
        for n in p["notas"]:
            notas.append(f'- **{p["frente"]} sobre {p["fondo"]}:** {n}')
        if p["sugerencia"]:
            notas.append(f'- **{p["frente"]} sobre {p["fondo"]}:** '
                         f'{texto_sugerencia(p["sugerencia"])}')
    for d in r["distinguir"]:
        for n in d["notas"]:
            notas.append(f'- **{d["a"]} y {d["b"]}:** {n}')
        if d["estado"] != "PASA":
            notas.append(f'- **{d["a"]} y {d["b"]}:** {texto_sugerencias_distinguir(d)}')
    if notas:
        lineas += ["", "### Observaciones", ""] + notas
    lineas += ["", RECORDATORIO, ""]
    return "\n".join(lineas)


def salida_html(r):
    e = html.escape

    def muestra(hex_, etiqueta=""):
        return (f'<span class="muestra" style="background:{hex_}"></span>'
                f'<code>{hex_}</code>{" " + e(etiqueta) if etiqueta else ""}')

    filas_colores = []
    for c in r["colores"]:
        sims = "<br>".join(
            f'{t}: {muestra(c["simulado"][t])}' for t in TIPOS_DALTONISMO + ("grises",)
        )
        filas_colores.append(
            f'<tr><th scope="row">{e(c["nombre"])}</th><td>{muestra(c["hex"])}</td>'
            f'<td>{e(c["descripcion"])}</td><td>{e(c["uso"] or "-")}</td>'
            f'<td>{e(c["rojo_verde"])}</td><td>{sims}</td></tr>'
        )

    hex_de = {c["nombre"]: c["hex"] for c in r["colores"]}
    simbolo = {"PASA": "&#10004; PASA", "FALLA": "&#10008; FALLA",
               "ADVERTENCIA": "&#9888; ADVERTENCIA"}
    filas_pares = []
    for p in r["pares"]:
        notas = " ".join(p["notas"])
        if p["sugerencia"]:
            notas += " " + texto_sugerencia(p["sugerencia"])
        tam = "1.5rem" if p["tipo"] == "texto-grande" else "1rem"
        filas_pares.append(
            f'<tr><th scope="row">{e(p["frente"])} sobre {e(p["fondo"])}</th>'
            f'<td><span class="ejemplo" style="color:{hex_de[p["frente"]]};'
            f'background:{hex_de[p["fondo"]]};font-size:{tam}">Texto de ejemplo</span></td>'
            f'<td>{e(DESCRIPCION_TIPO[p["tipo"]])}</td><td>{p["contraste"]}</td>'
            f'<td>{p["minimo"]}</td><td><strong>{simbolo[p["estado"]]}</strong></td>'
            f'<td>{e(notas)}</td></tr>'
        )
    filas_dist = []
    for d in r["distinguir"]:
        filas_dist.append(
            f'<tr><th scope="row">{e(d["a"])} y {e(d["b"])}</th>'
            f'<td>{muestra(hex_de[d["a"]])} {muestra(hex_de[d["b"]])}</td>'
            f'<td>{d["diferencia"]}</td><td>{min(d["simulado"].values())}</td>'
            f'<td>{d["claridad"]}</td><td><strong>{simbolo[d["estado"]]}</strong></td>'
            f'<td>{e(" ".join(d["notas"] + ([texto_sugerencias_distinguir(d)] if d["estado"] != "PASA" else [])))}</td></tr>'
        )

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paleta verificada: {e(r["nombre"])}</title>
<style>
  body {{ font-family: system-ui, sans-serif; color: #111; background: #fff;
         margin: 0; padding: 1rem; line-height: 1.5; }}
  main {{ max-width: 70rem; margin: 0 auto; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0 2rem; }}
  th, td {{ border: 1px solid #555; padding: .5rem; text-align: left; vertical-align: top; }}
  thead th {{ background: #eee; }}
  .tabla {{ overflow-x: auto; }}
  .muestra {{ display: inline-block; width: 1.5rem; height: 1.5rem; border: 2px solid #111;
             vertical-align: middle; margin-right: .4rem; }}
  .ejemplo {{ display: inline-block; padding: .4rem .7rem; border: 1px solid #111; }}
  .resultado {{ border: 3px solid #111; padding: .75rem 1rem; font-size: 1.2rem; }}
</style>
</head>
<body>
<main>
<h1>Paleta verificada: {e(r["nombre"])}</h1>
<p class="resultado"><strong>Resultado: {e(r["veredicto"])}</strong>
 (nivel WCAG {e(r["nivel"])}; {cuenta(r)}).
 Verificado por cálculo, no a ojo.</p>
<h2>Colores</h2>
<div class="tabla"><table>
<thead><tr><th>Nombre</th><th>Código</th><th>Se describe como</th><th>Para qué se usa</th>
<th>Con daltonismo rojo-verde</th><th>Simulación</th></tr></thead>
<tbody>{"".join(filas_colores)}</tbody></table></div>
<h2>Contraste</h2>
<div class="tabla"><table>
<thead><tr><th>Combinación</th><th>Muestra</th><th>Uso</th><th>Contraste</th><th>Mínimo</th>
<th>Resultado</th><th>Observaciones</th></tr></thead>
<tbody>{"".join(filas_pares)}</tbody></table></div>
<h2>Colores que deben distinguirse entre sí</h2>
<div class="tabla"><table>
<thead><tr><th>Colores</th><th>Muestras</th><th>Diferencia</th><th>Peor caso con daltonismo</th>
<th>Diferencia de claridad</th><th>Resultado</th><th>Observaciones</th></tr></thead>
<tbody>{"".join(filas_dist)}</tbody></table></div>
<p>{e(RECORDATORIO)}</p>
</main>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Línea de comandos
# ---------------------------------------------------------------------------

def modo_par(frente, fondo, nivel):
    f, b = leer_hex(frente), leer_hex(fondo)
    paleta = {
        "nombre": "Comprobación rápida",
        "colores": {"frente": {"rgb": f, "uso": ""}, "fondo": {"rgb": b, "uso": ""}},
        "pares": [("frente", "fondo", "texto"), ("frente", "fondo", "interfaz")],
        "distinguir": [],
    }
    return analizar(paleta, nivel)


def modo_describir(colores):
    lineas = []
    for texto in colores:
        rgb = leer_hex(texto)
        lineas.append(f"{a_hex(rgb)}  {nombre_color(rgb)}")
        lineas.append(f"    con daltonismo rojo-verde {como_se_ve(rgb)}")
        sims = " | ".join(f"{t} {a_hex(simular(rgb, t))}" for t in TIPOS_DALTONISMO)
        lineas.append(f"    simulado: {sims}")
    return "\n".join(lineas)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Verifica contraste y daltonismo de una paleta, por cálculo."
    )
    p.add_argument("paleta", nargs="?", help="Archivo JSON con la paleta")
    p.add_argument("--par", nargs=2, metavar=("FRENTE", "FONDO"),
                   help="Comprobar solo dos colores, por ejemplo: --par '#1B1F3B' '#FFFFFF'")
    p.add_argument("--describir", nargs="+", metavar="COLOR",
                   help="Describir colores con palabras")
    p.add_argument("--nivel", choices=("AA", "AAA"), default="AA",
                   help="Nivel WCAG exigido (por defecto AA)")
    p.add_argument("--md", metavar="ARCHIVO", help="Guardar tabla en Markdown")
    p.add_argument("--html", metavar="ARCHIVO", help="Guardar vista en HTML")
    p.add_argument("--json", action="store_true", help="Imprimir el resultado en JSON")
    args = p.parse_args(argv)

    try:
        if args.describir:
            print(modo_describir(args.describir))
            return 0
        if args.par:
            resultado = modo_par(args.par[0], args.par[1], args.nivel)
        elif args.paleta:
            ruta = Path(args.paleta)
            if not ruta.is_file():
                raise ErrorDeEntrada(f"No existe el archivo {ruta}.")
            try:
                datos = json.loads(ruta.read_text(encoding="utf-8"))
            except json.JSONDecodeError as err:
                raise ErrorDeEntrada(f"{ruta} no es JSON válido: {err}")
            resultado = analizar(leer_paleta(datos), args.nivel)
        else:
            p.print_help()
            return 2
    except ErrorDeEntrada as err:
        print(f"ERROR EN LOS DATOS: {err}", file=sys.stderr)
        return 2

    if args.md:
        Path(args.md).write_text(salida_md(resultado), encoding="utf-8")
    if args.html:
        Path(args.html).write_text(salida_html(resultado), encoding="utf-8")
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(salida_texto(resultado))
        if args.par:
            print('Nota: esta comprobación rápida revisa un solo par. Para saber si varios '
                  'colores se distinguen entre sí (por ejemplo éxito y error), usa un '
                  'archivo de paleta con la sección "distinguir".')
        for etiqueta, ruta in (("Markdown", args.md), ("HTML", args.html)):
            if ruta:
                print(f"Guardado {etiqueta}: {ruta}")
    return 1 if resultado["fallas"] else 0


if __name__ == "__main__":
    sys.exit(main())
