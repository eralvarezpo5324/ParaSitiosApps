# Experto en sitios y aplicaciones a la medida

Una skill de Claude que te guía paso a paso para diseñar, construir, blindar y publicar **páginas web, aplicaciones web y apps móviles** hechas a la medida.

Está hecha para trabajar con TDAH y daltonismo rojo-verde:

- Pregunta en rondas cortas de 3 o 4 preguntas, con opciones y una recomendación.
- Siempre te dice dónde vas y cuál es el siguiente paso.
- **Nunca te pide juzgar un color a ojo.** Los colores se verifican por cálculo y recibes un veredicto escrito: PASA o FALLA.

---

## 1. Instalar (una sola vez)

### Opción A: en tu cuenta de Claude (recomendada)

Queda disponible en todas tus sesiones y en todos tus repositorios.

1. Descarga el archivo [`dist/expert-apps.zip`](dist/expert-apps.zip) de este repositorio.
2. Entra a claude.ai y abre **Customize** (Personalizar) y luego **Skills**.
3. Presiona **+**, después **Create skill** y elige **Upload a skill**.
4. Selecciona `expert-apps.zip`. No lo descomprimas.
5. Debe aparecer "expert-apps" en tu lista de skills, activada.

Si Claude te muestra en el chat una tarjeta con el archivo `expert-apps.skill`, basta con presionar **Guardar skill** en esa tarjeta.

Los nombres del menú pueden cambiar con el tiempo. Si no los encuentras, pregúntale a Claude: "¿cómo subo una skill a mi cuenta?".

### Actualizar una versión ya instalada

Repite los mismos pasos con el archivo nuevo. Si Claude pregunta, elige **reemplazar**. Si al terminar ves dos skills con el mismo propósito en tu lista, borra la más antigua: dos versiones activas a la vez se estorban.

### Opción B: dentro de un solo repositorio

Copia la carpeta `skills/expert-apps` de este repositorio a `.claude/skills/expert-apps` en el repositorio del cliente. Úsala solo si no puedes instalar la opción A. No instales las dos a la vez.

---

## 2. Usar

### Antes de un proyecto nuevo: un repositorio por cliente

1. En github.com, presiona el botón **+** de arriba a la derecha y elige **New repository**.
2. Escribe el nombre del cliente o del proyecto, marca **Private** y marca **Add a README file**.
3. Presiona **Create repository**.
4. En Claude Code, inicia una sesión nueva y elige ese repositorio.

Si el repositorio nuevo no aparece en la lista de Claude, falta darle acceso a Claude en GitHub. Si empiezas en otro repositorio por error, el experto te avisa y te guía.

### Qué escribir

Con la sesión abierta en el repositorio del cliente, escribe una de estas cosas:

| Quieres | Escribe |
|---|---|
| Empezar un proyecto | `/expert-apps`, o cuenta con tus palabras lo que pidió el cliente |
| Seguir donde te quedaste | `continuemos` |
| Validar colores | "¿Está bien esta combinación?" con los códigos de color |
| Revisar la seguridad de un sitio | "Revisa la seguridad antes de publicar" |

En el menú, la skill puede aparecer como `expert-apps` o como `anthropic-skills:expert-apps`. Es la misma.

---

## 3. Cómo trabaja: 10 fases con puntos de aprobación

El experto se detiene a pedir tu aprobación solo en las fases marcadas. Entre ellas avanza solo y te informa.

| # | Fase | Qué se logra | Te pide aprobación |
|---|---|---|---|
| 0 | Arranque | Qué se construye, para quién, sus funciones clave, idioma y países | |
| 1 | Descubrimiento | Negocio, usuarios, funciones, referencias y dónde se publica | |
| 2 | Análisis y propuesta | Conflictos, huecos, mejoras y preguntas para el cliente | Sí |
| 3 | Arquitectura | Tecnología según el hosting, datos y modelo de amenazas | Sí |
| 4 | Diseño | Estructura, tipografía, colores verificados y animación | Sí |
| 5 | Construcción | Cada parte funcionando, con una prueba guiada para ti | Sí |
| 6 | Optimización | Velocidad, SEO, GEO, CRO y accesibilidad | |
| 7 | Seguridad | Auditoría como experto en ciberseguridad | Sí |
| 8 | Publicación | Sitio en línea y verificado | Sí |
| 9 | Entrega | Manual, accesos y mantenimiento | |

El experto elige el recorrido según las funciones, no te pregunta el tamaño. Una página que solo informa recorre una versión corta. Un proyecto con cuentas de usuario, pagos o datos sensibles, y cualquier app móvil, recorre la completa con seguridad reforzada.

En el arranque, lo primero que te pide es que cuentes el proyecto con tus palabras o pegues lo que pidió el cliente. Después pregunta solo lo que falte. Nunca pone en el mismo bloque una pregunta que dependa de la respuesta de otra: esa espera a la ronda siguiente.

---

## 4. Qué crea en cada proyecto

Todo queda en la carpeta `docs/proyecto/` del repositorio del cliente:

| Archivo | Para qué sirve |
|---|---|
| `ESTADO.md` | La memoria del proyecto: en qué fase vas y qué sigue. Por esto puedes cerrar la sesión y retomar otro día |
| `brief-propuesta.md` | El documento que aprueba tu cliente |
| `preguntas-cliente.md` | Las preguntas que le llevas a tu cliente, en lenguaje sencillo |
| `arquitectura.md` | Tecnología elegida, datos y amenazas previstas |
| `paleta.json` y `guia-diseno-color.md` | Los colores con nombre, código, uso y verificación |
| `reporte-seguridad.md` | Qué se probó, qué se encontró y qué riesgos quedan. Es interno |
| `manual-entrega.md` | La guía para tu cliente |

Estos documentos nunca se suben al servidor público.

---

## 5. Las tres verificaciones automáticas

Son programas pequeños que dan siempre el mismo resultado, sin importar qué modelo de Claude los ejecute. Solo necesitan Python 3.

| Programa | Qué revisa |
|---|---|
| `verificar_color.py` | Contraste de cada combinación y cómo se ve con cada tipo de daltonismo. Describe cada color con palabras y propone la corrección |
| `buscar_secretos.py` | Contraseñas y llaves olvidadas en el código o en su historial |
| `revisar_sitio.py` | Un sitio ya publicado, visto desde fuera: cifrado, cabeceras, archivos expuestos |

Normalmente los ejecuta el experto. Si quieres probar uno tú:

```bash
python3 skills/expert-apps/scripts/verificar_color.py skills/expert-apps/plantillas/paleta-ejemplo.json
```

`revisar_sitio.py` solo debe usarse en sitios tuyos o con autorización escrita del dueño.

---

## 6. Mantener al experto al día

Las guías llevan su fecha de revisión y sus fuentes oficiales. El experto las verifica al iniciar cada fase cuando tiene acceso a internet. Para actualizarlo tú:

1. Abre una sesión de Claude Code en este repositorio y pide el cambio. Por ejemplo: "actualiza la guía móvil con los requisitos vigentes de las tiendas".
2. Genera el paquete nuevo:
   ```bash
   python3 empaquetar.py
   ```
3. Vuelve a subir `dist/expert-apps.zip` a tu cuenta (paso 1 de la instalación).

### Cuando salga un modelo nuevo de Claude

La skill no fija ningún modelo. Para comprobar que se comporta igual con uno nuevo:

```bash
python3 pruebas/probar_con_modelo.py --modelo NOMBRE-DEL-MODELO
```

Lanza varias conversaciones de prueba y responde PASA o FALLA en cada una. Consume uso de tu cuenta.

---

## 7. Qué hay en este repositorio

```
skills/expert-apps/
  SKILL.md           El flujo por fases y las reglas de trato
  referencias/       13 guías: descubrimiento, conflictos, arquitectura, diseño, color,
                     animación, funcionalidad, rendimiento, SEO-GEO-CRO, seguridad,
                     móvil, legal y publicación
  plantillas/        Los documentos que se generan en cada proyecto
  revisores/         Instrucciones de los dos revisores independientes
  scripts/           Las tres verificaciones automáticas
pruebas/
  test_scripts.py        Pruebas de los scripts (no consumen uso de la cuenta)
  probar_con_modelo.py   Pruebas de comportamiento con un modelo real
dist/                El paquete listo para instalar
empaquetar.py        Genera el paquete
```

Para ejecutar las pruebas de los scripts:

```bash
python3 -m unittest discover -s pruebas
```

---

## 8. Lo que el experto no puede prometer

- **Seguridad al 100 %.** No existe. El experto aplica los estándares, hace las pruebas y te deja por escrito qué se revisó y qué riesgos quedan.
- **Asesoría legal o fiscal.** Los textos legales que redacta son borradores para que los revise un abogado.
- **Posiciones en buscadores.** Nadie puede garantizarlas.
- **Sustituir una prueba de penetración profesional** en proyectos con pagos en volumen o datos muy sensibles. Cuando haga falta, te lo dirá.
