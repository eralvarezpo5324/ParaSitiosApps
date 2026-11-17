# Color con daltonismo rojo-verde: protocolo completo

Revisado: noviembre de 2026.

El usuario confunde rojos, verdes, cafés y naranjas, y no puede confirmar a ojo un contraste. El color es una responsabilidad tuya de principio a fin: lo propones, lo verificas por cálculo y lo explicas con palabras. Además, lo que construyes debe funcionar para visitantes con cualquier tipo de daltonismo, que son cerca de uno de cada doce hombres.

## Protocolo en seis pasos

### 1. Reúne los datos de partida
- ¿Hay colores de marca? Pide los códigos exactos o el archivo del logotipo.
- Las tres palabras de estilo del descubrimiento.
- El sector: hay convenciones que el público espera (salud, finanzas, comida, infantil).

### 2. Propón la paleta por funciones
Define los colores por lo que hacen, no por cómo se ven. Conjunto habitual:

| Función | Para qué |
|---|---|
| `fondo`, `superficie` | Fondo general y fondo de tarjetas o secciones alternas |
| `texto`, `texto-secundario` | Texto principal y de apoyo |
| `primario`, `sobre-primario` | Botones y enlaces; y el texto que va encima |
| `acento`, `sobre-acento` | Resaltar con moderación; y el texto que va encima |
| `borde` | Bordes de campos y separadores que deben verse |
| `exito`, `error`, `aviso` | Estados. Siempre acompañados de icono y texto |

### 3. Escribe `docs/proyecto/paleta.json`
Usa `plantillas/paleta-ejemplo.json` como base. Tres secciones:

- `colores`: cada función con su código y su uso.
- `pares`: cada combinación de frente sobre fondo que exista de verdad en el diseño. Tipos: `texto` (mínimo 4.5), `texto-grande` (mínimo 3; desde 24 píxeles, o 19 en negrita) e `interfaz` (mínimo 3; bordes de campos, iconos, foco).
- `distinguir`: grupos de colores que el visitante debe poder diferenciar entre sí, como éxito y error, o las series de una gráfica.

Incluye todos los pares reales. Un par que no está en el archivo no fue verificado.

### 4. Verifica y corrige hasta que dé PASA
```
python3 <ruta de la skill>/scripts/verificar_color.py docs/proyecto/paleta.json
```
- **FALLA de contraste:** aplica la sugerencia que da el script (mismo tono, más claro o más oscuro) o cambia el color, y vuelve a ejecutar.
- **FALLA porque dos colores se confunden:** el script propone una alternativa ya calculada para cada uno de los dos, con su descripción en palabras. Elige la que mejor conserve el significado (un color de error debe seguir leyéndose como error) y vuelve a ejecutar. Oscurecer los dos por igual no lo arregla: tienen que separarse en claridad o en el eje azul-amarillo.
- **ADVERTENCIA:** corrígela si es barato. Si no, deja escrito en la guía de color por qué se acepta y qué la compensa.
- No pases a construir con una paleta en FALLA.

### 5. Preséntala al usuario
Una tabla con función, descripción en palabras, código y uso, más el veredicto. Las descripciones las da el script. Ejemplo:

> **Paleta verificada: PASA** (0 fallas, 0 advertencias)
> - Primario: azul oscuro intenso `#1D4ED8`. Botones y enlaces.
> - Acento: amarillo claro intenso `#FBBF24`. Etiquetas de oferta.
>
> Sensación general: seria y confiable, con un toque cálido en las ofertas.

Pregúntale por la sensación ("¿seria y confiable es lo que busca tu cliente?"), nunca por el color en sí.

### 6. Genera la guía para el cliente
```
python3 <ruta de la skill>/scripts/verificar_color.py docs/proyecto/paleta.json \
  --md docs/proyecto/paleta-verificada.md --html docs/proyecto/paleta-verificada.html
```
Inserta la tabla en `guia-diseno-color.md`. La vista HTML muestra cada color con su nombre y código escritos, así el usuario puede enseñarla al cliente sin depender de su vista.

## Estrategias que funcionan con daltonismo rojo-verde

- **Apóyate en la claridad.** Dos colores con claridad muy distinta se diferencian con cualquier tipo de visión. Es la herramienta más segura.
- **Apóyate en el eje azul frente a amarillo o naranja.** Se conserva con daltonismo rojo-verde.
- **Combinaciones de riesgo:** rojo con verde; verde con café o naranja; azul con morado; rosa con gris; turquesa con gris; rojo oscuro con negro (con protanopia el rojo se ve muy oscuro).
- **Éxito y error:** además de distinto color, distinta claridad, icono distinto (palomita, signo de alerta) y texto. El script los revisa si están en `distinguir`.
- **Gráficas y mapas:** etiquetas directas sobre los datos, tramas o formas distintas y, como mucho, cinco o seis categorías por color.

## El color nunca es la única señal

Revisa cada uno de estos casos en lo que construyas:

| Caso | Señal adicional obligatoria |
|---|---|
| Campo con error | Icono, texto del error junto al campo y borde más grueso |
| Campo obligatorio | La palabra "obligatorio" o un texto equivalente, no solo un asterisco de color |
| Enlace dentro de un párrafo | Subrayado |
| Pestaña o menú activo | Peso de letra, subrayado o marca, además del color |
| Elemento seleccionado | Marca de verificación o borde grueso |
| Estados: disponible, agotado, pendiente | Texto con el estado |
| Etiquetas e insignias | Texto dentro de la etiqueta |
| Mensajes de éxito, aviso y error | Icono y título con el tipo de mensaje |
| Gráficas | Etiquetas y tramas |
| Botón de acción destructiva | Texto explícito ("Eliminar cuenta") y confirmación |

## Cuando la marca del cliente no cumple

Es frecuente: un naranja o un verde claro de marca no alcanza contraste sobre blanco.

1. Conserva el color de marca para superficies grandes, fondos de botón con texto oscuro, ilustraciones y el logotipo.
2. Crea una **variante accesible** del mismo tono, más oscura, para textos y enlaces. El script la sugiere.
3. Documenta ambos en la guía: "Naranja de marca `#F7931E`: solo fondos y elementos grandes. Naranja accesible `#B45309`: textos y enlaces."
4. Explícaselo al usuario con el dato: "El naranja de marca tiene contraste 2.3 sobre blanco y la norma pide 4.5. La variante accesible llega a 5.0 y conserva el tono."

Nunca cambies el logotipo del cliente.

## Cómo hablar de color con el usuario

- Usa palabras de sensación y de claridad: claro u oscuro, cálido o frío, intenso o apagado, serio o alegre.
- Da siempre el código. Es lo que puede copiar, comparar y comunicar sin error.
- No digas "como puedes ver", "el botón verde" ni "fíjate en el tono".
- Si necesita hablar de color con su cliente, entrégale la frase lista: "El color principal es un azul oscuro intenso, código 1D4ED8; transmite seriedad y cumple la norma de accesibilidad."
- Si el usuario recibe un comentario de color del cliente ("lo quiero más vivo"), tradúcelo tú a un cambio concreto, verifícalo y devuélvele el resultado.

## Comprobar lo ya construido

La paleta puede pasar y el sitio fallar: un texto sobre una foto, un degradado, un estado olvidado.

- Revisa en el código que todos los colores vengan de las variables de la paleta. Un código de color suelto es un color sin verificar.
- Si tienes navegador automatizado, ejecuta una herramienta de auditoría de accesibilidad sobre cada página y estado.
- Texto sobre imagen o degradado: verifica contra el punto más claro y el más oscuro del fondo con `--par`.
- Para dudas puntuales: `verificar_color.py --par "#frente" "#fondo"` y `--describir "#color"`.

## Cómo leer el resultado del script

- **Contraste:** relación de luminosidad entre frente y fondo, de 1 a 21, según WCAG.
- **Simulado:** el mismo contraste tal como lo percibe alguien con protanopia, deuteranopia o tritanopia.
- **Diferencia:** qué tan distintos se perciben dos colores. Menos de 10, se confunden. Entre 10 y 20, se distinguen con dificultad.
- **Claridad:** diferencia de luminosidad percibida. Menos de 15 significa que en blanco y negro son iguales.

Límites: la simulación es un modelo matemático de los casos más marcados y no sustituye una prueba con personas. No analiza imágenes ni degradados: esos pares se verifican en su peor punto.

## Si no hay Python

Haz el cálculo a mano y muéstralo:

1. Convierte cada canal de 0 a 255 a una fracción `c`. Si `c` es menor o igual a 0.04045 usa `c / 12.92`; si no, `((c + 0.055) / 1.055)` elevado a 2.4.
2. Luminancia = 0.2126 × rojo + 0.7152 × verde + 0.0722 × azul.
3. Contraste = (luminancia mayor + 0.05) / (luminancia menor + 0.05).

Sin simulación de daltonismo disponible, compensa asegurando una diferencia grande de claridad entre los colores que deban distinguirse, y dilo en el entregable: "simulación de daltonismo no ejecutada".

## Fuentes para verificar

- W3C, WCAG 2.2, criterios 1.4.1, 1.4.3 y 1.4.11: w3.org/TR/WCAG22
- Machado, Oliveira y Fernandes (2009), modelo de simulación de daltonismo que usa el script.
