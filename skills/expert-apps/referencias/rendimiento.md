# Fase 6 · Rendimiento

Revisado: noviembre de 2026. Los umbrales de Core Web Vitals son los vigentes de Google; verifica que no hayan cambiado.

Un sitio lento pierde visitantes, ventas y posición en buscadores. La mayoría de los visitantes llega desde un celular de gama media con datos móviles: esa es la condición que hay que medir.

## Objetivos

Medidos en celular, en el percentil 75 de las visitas reales:

| Métrica | Qué mide | Bueno |
|---|---|---|
| LCP | Cuánto tarda en verse el contenido principal | 2.5 segundos o menos |
| INP | Cuánto tarda la página en responder a una acción | 200 milisegundos o menos |
| CLS | Cuánto se mueve el contenido mientras carga | 0.1 o menos |
| TTFB | Cuánto tarda el servidor en empezar a responder | 0.8 segundos o menos |

Presupuesto orientativo para un sitio de contenido: página inicial de menos de 1 MB en total, y menos de 170 KB de JavaScript comprimido.

## Regla de oro

**Mide antes, cambia una cosa, mide después.** Anota ambas mediciones en `ESTADO.md`. No declares una mejora que no mediste. Las mediciones de laboratorio y las de visitantes reales no coinciden: di siempre cuál estás dando.

## Imágenes: casi siempre lo más pesado

- Formatos modernos (AVIF o WebP) con alternativa.
- Varias resoluciones con `srcset` y `sizes`: el celular no descarga la imagen de escritorio.
- Ancho y alto declarados, para que la página no salte al cargar.
- Carga diferida en lo que queda fuera de la primera pantalla.
- **La imagen principal no se difiere:** se carga con prioridad alta.
- Comprime. Una foto de portada rara vez necesita pesar más de 200 KB.
- Video: nunca como archivo pesado en el hosting compartido. Plataforma externa y una imagen de portada que carga el reproductor solo al hacer clic.

## Fuentes

- Alojadas en el propio sitio, en WOFF2, solo con los caracteres necesarios.
- Una o dos familias, pocos pesos. Una fuente variable suele pesar menos que varios archivos.
- Precarga solo la del texto principal. Texto visible mientras carga la fuente.
- Ajusta la fuente de respaldo para que el cambio no mueva el contenido.

## CSS y JavaScript

- Envía solo lo que la página usa. Divide por página.
- JavaScript diferido. Nada bloquea el primer pintado.
- Prefiere HTML y CSS a JavaScript: menús, acordeones, ventanas de diálogo y muchas animaciones ya no lo necesitan.
- **Scripts de terceros:** cada uno debe justificar su peso. Mapas, chat, video y redes sociales se cargan al interactuar, tras una imagen de sustitución.
- Tareas largas de JavaScript partidas en trozos, para que la página responda.

## Forma de generar las páginas

- **Estático primero:** páginas generadas al construir. Lo más rápido y lo más seguro.
- Generación en el servidor cuando el contenido cambia por visitante o con mucha frecuencia.
- Evita que el contenido dependa de JavaScript en el navegador: es más lento y menos visible para buscadores y asistentes de IA.
- Como mejora progresiva: precarga de la página siguiente con reglas de especulación y transiciones de vista.

## Servidor y hosting

- Compresión activa (Brotli o gzip) y HTTP/2 o HTTP/3.
- Caché larga (un año, inmutable) para archivos con huella en el nombre; caché corta para el HTML.
- **CDN por delante del hosting compartido:** suele ser la mejora más grande y barata. Además filtra ataques básicos.
- PHP: versión con soporte vigente y caché de código activa.
- Base de datos: índices en las columnas por las que se busca, y sin consultas repetidas dentro de bucles.
- Caché de página para contenido que no cambia por visitante.

En hosting compartido con Apache, la compresión y la caché se configuran en `.htaccess`. El fragmento está en `despliegue.md`.

## Estabilidad visual

- Espacio reservado para imágenes, anuncios, mapas y contenido incrustado.
- Nada se inserta por encima del contenido que la persona ya está leyendo.
- Avisos de cookies y barras superiores sin empujar la página.

## Cómo medir

1. **Laboratorio, durante el desarrollo:** auditoría Lighthouse en modo celular, sobre el entorno de pruebas. Anota LCP, CLS, bloqueo total y peso de la página.
2. **Visitantes reales, tras publicar:** PageSpeed Insights y el informe de métricas web de Search Console. Los datos reales tardan semanas en aparecer; dilo.
3. **Dispositivo real:** abre el sitio en un Android de gama media con datos móviles. Si el usuario tiene uno, que sea parte de su prueba guiada.

Prueba las páginas que importan, no solo la portada: producto, formulario, pago.

## Apps móviles

- Tiempo de arranque: carga lo mínimo para mostrar la primera pantalla.
- Listas largas virtualizadas. Imágenes con caché y al tamaño de pantalla.
- Tamaño de la app: revisa lo que añade cada dependencia.
- Mide en un Android de gama baja. En el simulador todo parece rápido.

## Lista de comprobación

- [ ] Medición inicial y final anotadas en `ESTADO.md`, indicando si son de laboratorio o reales.
- [ ] LCP, INP y CLS dentro de objetivo en las páginas clave, o explicado qué lo impide.
- [ ] Imágenes en formato moderno, con dimensiones y carga diferida correcta.
- [ ] Fuentes alojadas en el sitio y recortadas.
- [ ] Scripts de terceros justificados y diferidos.
- [ ] Compresión y caché activas, comprobadas en las cabeceras de respuesta.
- [ ] Probado en un celular real.

## Fuentes para verificar

- web.dev/vitals: definiciones y umbrales vigentes.
- developers.google.com/search: relación entre experiencia de página y búsqueda.
- Documentación del hosting sobre compresión, caché y versiones de PHP.
