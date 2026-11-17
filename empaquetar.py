#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
empaquetar.py - Genera dist/expert-apps.skill y dist/expert-apps.zip a partir de skills/expert-apps.

Los dos archivos tienen el mismo contenido. El .skill sirve para instalar con un
clic desde la tarjeta del archivo; el .zip, para subirlo a mano en claude.ai.

Uso, desde la raíz del repositorio:
    python3 empaquetar.py

Antes de empaquetar ejecuta las pruebas. Si alguna falla, no genera nada.
Solo usa la biblioteca estándar de Python 3.
"""

import re
import subprocess
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SKILL = RAIZ / "skills" / "expert-apps"
SALIDA = RAIZ / "dist"
CARPETAS_EXCLUIDAS = {"__pycache__", "node_modules"}
ARCHIVOS_EXCLUIDOS = {".DS_Store"}


def validar():
    texto = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    cabecera = re.match(r"^---\n(.*?)\n---\n", texto, re.DOTALL)
    if not cabecera:
        return "SKILL.md no empieza con la cabecera entre líneas ---"
    campos = dict(
        linea.split(": ", 1) for linea in cabecera.group(1).splitlines() if ": " in linea
    )
    permitidos = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
    sobrantes = set(campos) - permitidos
    if sobrantes:
        return f"La cabecera tiene campos no admitidos: {', '.join(sorted(sobrantes))}"
    if campos.get("name") != SKILL.name:
        return f'El campo name debe ser "{SKILL.name}", igual que la carpeta'
    descripcion = campos.get("description", "")
    if not descripcion or len(descripcion) > 1024:
        return f"La descripción debe tener entre 1 y 1024 caracteres (tiene {len(descripcion)})"
    if "<" in descripcion or ">" in descripcion:
        return "La descripción no puede contener los signos < o >"
    if len(list(SKILL.rglob("SKILL.md"))) != 1:
        return "Debe existir exactamente un SKILL.md"
    return None


def main():
    error = validar()
    if error:
        print(f"FALLA: {error}")
        return 1

    pruebas = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "pruebas"],
        cwd=RAIZ, capture_output=True, text=True,
    )
    if pruebas.returncode != 0:
        print(pruebas.stderr[-3000:])
        print("FALLA: las pruebas no pasan. No se generó ningún archivo.")
        return 1
    print(pruebas.stderr.strip().splitlines()[-3])

    archivos = sorted(
        ruta for ruta in SKILL.rglob("*")
        if ruta.is_file()
        and not (set(ruta.relative_to(SKILL).parts) & CARPETAS_EXCLUIDAS)
        and ruta.name not in ARCHIVOS_EXCLUIDOS
        and ruta.suffix != ".pyc"
        and ruta.relative_to(SKILL).parts[0] != "evals"
    )
    SALIDA.mkdir(exist_ok=True)
    for extension in ("skill", "zip"):
        destino = SALIDA / f"{SKILL.name}.{extension}"
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as paquete:
            for ruta in archivos:
                # Fecha fija: el paquete no cambia si el contenido no cambió.
                info = zipfile.ZipInfo(ruta.relative_to(SKILL.parent).as_posix(),
                                       date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                paquete.writestr(info, ruta.read_bytes())
        print(f"PASA: {destino.relative_to(RAIZ)}  ({len(archivos)} archivos, "
              f"{destino.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
