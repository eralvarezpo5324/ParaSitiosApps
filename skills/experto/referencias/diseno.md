# Fase 4 · Diseño

Revisado: noviembre de 2026. Norma de accesibilidad vigente: WCAG 2.2 (W3C). WCAG 3 sigue en borrador y no es exigible.

Diseño a la medida significa que cada decisión sale del negocio, su público y su contenido. No se parte de una plantilla genérica.

## Cómo se aprueba el diseño con este usuario

El usuario puede juzgar bien la estructura, la jerarquía, la tipografía, el espaciado, el estilo general y el movimiento. No puede juzgar el color. Por eso el orden es:

1. **Estructura.** Qué secciones hay, en qué orden y qué dice cada una. Preséntala como esquema en texto o como maqueta sin color (grises).
2. **Tipografía y espaciado.**
3. **Paleta.** La propones y la verificas tú con `color-daltonismo.md`. Al usuario le presentas el veredicto y la descripción en palabras.
4. **Componentes y estados.**
5. **Movimiento,** con `animacion.md`.

Si tienes navegador, enséñale capturas o una vista previa. Acompaña siempre la imagen con una descripción escrita de lo que debe notar. Pregunta cosas como "¿la información más importante queda arriba?" y nunca "¿te gusta este azul?".

## De dónde sale el diseño

- **Tres palabras** del descubrimiento (por ejemplo: serio, cercano, moderno) y lo que no debe parecer.
- **El contenido real manda.** Diseña con los textos y fotos reales o con borradores verosímiles, no con texto de relleno.
- **Las referencias** aportan principios: ritmo, densidad, escala tipográfica, tipo de movimiento. Di por escrito qué se toma de cada una. No se copia.
- **La marca existente** se respeta: logotipo, tipografía y colores como punto de partida.

## Estructura y composición

- **Primero el celular.** Diseña para pantalla pequeña y amplía después.
- **Una acción principal por pantalla,** visible sin desplazarse en el celular.
- **Jerarquía por tamaño, peso y posición,** no solo por color.
- **Líneas de texto de 45 a 75 caracteres.** Más anchas cansan.
- **Espaciado con una escala fija** (múltiplos de 4 u 8 píxeles). El espacio en blanco agrupa y separa: úsalo con intención.
- **Composición fluida** con rejilla y cajas flexibles, y componentes que se adaptan a su contenedor. Los puntos de cambio los decide el contenido, no una lista de dispositivos.
- La página debe verse bien a 320 píxeles de ancho y con el texto ampliado al 200 %.

## Tipografía

- Una o dos familias. Más de dos casi nunca se justifica.
- Texto base de 16 píxeles o más. Interlineado cercano a 1.5 en párrafos.
- Tamaños fluidos que crecen con la pantalla, dentro de un mínimo y un máximo.
- Fuentes alojadas en el propio sitio, en formato WOFF2, con solo los caracteres necesarios y texto visible mientras cargan. Comprueba que incluyan acentos, ñ y signos de apertura.
- Evita texto en mayúsculas en párrafos largos y texto justificado.

## Componentes y estados

Cada elemento interactivo necesita todos sus estados diseñados: normal, cursor encima, foco de teclado, presionado, deshabilitado, cargando y error. Cada vista necesita además sus estados vacío, cargando, error y éxito (ver `funcionalidad.md`).

- **Foco visible siempre:** contorno de al menos 2 píxeles con contraste 3 a 1. Nunca lo quites sin sustituirlo.
- **Tamaño de zona táctil:** mínimo exigido 24 por 24 píxeles; recomendado 44 a 48 en pantallas táctiles.
- **Los enlaces dentro de un texto se subrayan.** El color solo no basta.
- **Botones con verbo:** "Enviar mensaje", "Agendar cita". No "Aceptar" ni "Clic aquí".

## Accesibilidad: requisitos mínimos (WCAG 2.2 nivel AA)

- HTML semántico: encabezados en orden, regiones (`header`, `nav`, `main`, `footer`), botones que son botones y enlaces que son enlaces.
- Texto alternativo en imágenes informativas; vacío en las decorativas.
- Todo se puede usar con teclado, en un orden lógico, y el elemento con foco nunca queda tapado.
- Contraste: 4.5 a 1 en texto normal; 3 a 1 en texto grande, iconos, bordes de campos y foco.
- El color no es la única señal de nada.
- Formularios: etiqueta visible por campo, errores con texto junto al campo, no pedir dos veces el mismo dato, y un inicio de sesión que no dependa de memorizar o transcribir (permitir pegar y gestores de contraseñas).
- Lo que se arrastra tiene una alternativa con clic.
- La ayuda y el contacto aparecen en el mismo lugar en todas las páginas.
- Idioma de la página declarado; cambios de idioma marcados.
- Video con subtítulos. Nada se reproduce con sonido por sí solo.
- Respeto a la preferencia de reducir movimiento (ver `animacion.md`).

Para clientes en Estados Unidos, trata estos puntos como requisito del proyecto y no como mejora: el riesgo legal es real (ver `legal-privacidad.md`).

## CSS moderno: qué usar

Regla: usa sin reservas lo que ya está ampliamente disponible en todos los navegadores. Lo recién disponible, solo como mejora progresiva: la página debe funcionar igual sin ello. Verifica el estado de cada función en el momento del proyecto.

Ampliamente adoptado y útil: variables de CSS, rejilla y subrejilla, consultas de contenedor, selector `:has()`, anidamiento, capas (`@layer`), propiedades lógicas, funciones `clamp()`, `min()` y `max()`, unidades de ventana dinámicas, `aspect-ratio`, equilibrio de líneas en títulos (`text-wrap: balance`), colores OKLCH, `color-mix()`, y los elementos nativos de diálogo y ventana emergente.

Como mejora progresiva (verificar soporte): transiciones de vista entre páginas, animaciones ligadas al desplazamiento, posicionamiento por anclas.

## Sistema de diseño mínimo

Define como variables de CSS, con nombres por función y no por apariencia:

- Colores por función: `--color-fondo`, `--color-texto`, `--color-primario`. La fuente de verdad es `docs/proyecto/paleta.json`.
- Escala tipográfica, escala de espaciado, radios, sombras y duraciones de animación.

Cambiar un color es cambiar una variable y volver a ejecutar el verificador.

## Modo oscuro

Solo si aporta al público del sitio o el cliente lo pide. Es una segunda paleta completa: se verifica aparte (`paleta-oscuro.json`) con el mismo script y duplica las pruebas visuales.

## Lo que se evita

- Carruseles que avanzan solos.
- Texto sobre fotos sin una capa que asegure el contraste. Verifica el contraste en el punto más desfavorable de la imagen.
- Texto gris claro "elegante" que no alcanza el contraste.
- Ventanas emergentes al entrar.
- Alterar el desplazamiento natural de la página.
- Usar el texto de ejemplo del campo como etiqueta.
- Iconos sin texto para acciones que no son universales.
- Desplazamiento infinito sin forma de llegar al pie de página.

## Apps móviles

Sigue las convenciones de cada plataforma (guías de interfaz de Apple y Material Design de Google): navegación, gestos, áreas seguras, tamaño de texto ajustable por el usuario y modo oscuro del sistema. La paleta se verifica con el mismo protocolo.

## Salida de la fase

- `docs/proyecto/paleta.json` con veredicto PASA.
- `docs/proyecto/guia-diseno-color.md` con la plantilla, incluida la tabla que genera el verificador.
- Revisión con `revisores/auditor-accesibilidad-color.md`.
- Puerta de aprobación: estructura, estilo y movimiento los aprueba el usuario; el color se presenta ya verificado.

## Fuentes para verificar

- W3C, WCAG 2.2: w3.org/TR/WCAG22
- Estado de funciones en navegadores: web.dev/baseline y developer.mozilla.org
- Guías de interfaz de Apple y Material Design.
