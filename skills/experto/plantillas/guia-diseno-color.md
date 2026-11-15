# Guía de diseño y color: [nombre del proyecto]

> Se redacta en el idioma del cliente.
> Todos los colores están verificados por cálculo: nadie necesita juzgarlos a ojo.

**Fecha:** [fecha] · **Versión:** [1]

## 1. Estilo

**En tres palabras:** [palabra], [palabra], [palabra].
**Lo que no debe parecer:** [...]

**Referencias y qué se tomó de cada una:**

| Referencia | Qué se tomó |
|---|---|
| | |

## 2. Colores

[Pega aquí la tabla que genera `verificar_color.py --md`. Incluye el veredicto, la tabla de colores, la de contraste y la de colores que deben distinguirse.]

### Cómo usar cada color

| Función | Código | Úsalo para | No lo uses para |
|---|---|---|---|
| | | | |

### Colores de marca y sus variantes accesibles

[Solo si aplica.]

| Color de marca | Variante accesible | Cuándo usar cada uno |
|---|---|---|
| | | |

### Regla que nunca se rompe

El color nunca es la única señal. Todo error, éxito, aviso, selección o estado lleva además texto, icono o forma.

### Si hay que cambiar un color

1. Cambia el código en `docs/proyecto/paleta.json`.
2. Ejecuta el verificador.
3. Si el resultado no es PASA, aplica la sugerencia o elige otro color y repite.

## 3. Tipografía

| Uso | Familia | Peso | Tamaño |
|---|---|---|---|
| Títulos | | | |
| Texto | | | |
| Botones y etiquetas | | | |

Tamaño base: [16 px o más]. Interlineado del texto: [1.5].

## 4. Espaciado y composición

- **Escala de espaciado:** [valores].
- **Ancho máximo del texto:** [valor].
- **Radios y sombras:** [valores].

## 5. Componentes

| Componente | Aspecto | Estados que tiene |
|---|---|---|
| Botón principal | | Normal, cursor encima, foco, presionado, deshabilitado, cargando |
| Enlace | Subrayado | Normal, cursor encima, foco, visitado |
| Campo de formulario | | Normal, foco, error (icono y texto), deshabilitado |
| Mensajes | Icono y título según el tipo | Éxito, aviso, error |

## 6. Movimiento

| Animación | Para qué sirve | Duración | Con movimiento reducido |
|---|---|---|---|
| | | | |

## 7. Imágenes

- **Estilo:** [fotografía real, ilustración; tono].
- **Texto alternativo:** toda imagen informativa lo lleva.
- **Texto sobre imagen:** siempre con una capa que asegure el contraste, verificado en el punto más desfavorable.

## 8. Accesibilidad

Nivel aplicado: WCAG 2.2 AA. Revisión realizada el [fecha]. Resultado: [...]
