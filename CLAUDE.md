# ParaSitiosApps

Este repositorio es el código fuente de la skill `experto`: un experto que guía el diseño, la construcción, la seguridad y la publicación de páginas web, aplicaciones web y apps móviles a la medida. No contiene proyectos de clientes: cada cliente tiene su propio repositorio.

## Con quién trabajas

La persona dueña de este repositorio tiene TDAH y daltonismo rojo-verde, y un nivel técnico de básico a intermedio. Sigue instrucciones y pruebas guiadas con facilidad. Háblale siempre en español.

- Preguntas en rondas de 3 o 4, con opciones y una recomendación.
- Un objetivo por mensaje. Termina siempre con el siguiente paso concreto.
- Pasos manuales de uno en uno, diciendo qué debe ver en pantalla.
- Nunca le pidas juzgar colores a ojo, y no uses el color como única señal al escribirle.

## Estructura

- `skills/experto/SKILL.md`: flujo por fases y reglas de trato. Menos de 500 líneas.
- `skills/experto/referencias/`: una guía por tema. Se leen solo cuando la fase lo pide.
- `skills/experto/plantillas/`: documentos que se generan en cada proyecto.
- `skills/experto/revisores/`: instrucciones de los revisores independientes.
- `skills/experto/scripts/`: verificaciones automáticas. Solo biblioteca estándar de Python 3.
- `pruebas/`: pruebas de los scripts y de comportamiento.
- `dist/`: paquete generado. No se edita a mano.

## Reglas al modificar la skill

- **No fijes ningún modelo.** La cabecera de `SKILL.md` solo lleva `name` y `description`. Debe funcionar con cualquier modelo de Claude, actual o futuro.
- **No nombres herramientas concretas del entorno** en las guías. Describe la capacidad ("si tienes una herramienta de preguntas con opciones"), para que sirva en cualquier superficie.
- La descripción tiene un máximo de 1024 caracteres, en una sola línea, sin los signos `<` ni `>`, sin dos puntos seguidos de espacio y sin espacio seguido de `#`.
- Todo en español. Nombres de archivo sin acentos ni ñ.
- Al cambiar una guía, actualiza su línea "Revisado" y verifica el dato en la fuente oficial.
- Al cambiar un script, añade o ajusta su prueba en `pruebas/test_scripts.py`.
- Ningún archivo debe contener algo con forma de secreto real. En las pruebas, los secretos de ejemplo se arman por partes en tiempo de ejecución.
- Una verificación que pueda hacerse con un script va en un script, no en instrucciones: así el resultado no depende del modelo.

## Comandos

```bash
python3 -m unittest discover -s pruebas            # pruebas de los scripts
python3 empaquetar.py                              # ejecuta las pruebas y genera dist/
python3 pruebas/probar_con_modelo.py --modelo X    # comportamiento con un modelo real
```

`probar_con_modelo.py` consume uso de la cuenta: ejecútalo solo cuando cambie la descripción, el flujo de `SKILL.md` o haya un modelo nuevo.

## Antes de dar un cambio por terminado

1. `python3 empaquetar.py` termina en PASA.
2. Si cambió la descripción o el flujo: `probar_con_modelo.py` termina en PASA.
3. `dist/` quedó regenerado y va en el mismo commit.
