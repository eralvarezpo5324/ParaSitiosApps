# Fase 6 · SEO, GEO y CRO a la medida

Revisado: noviembre de 2026. Las reglas de los buscadores y de los asistentes de IA cambian con frecuencia: verifica las fuentes al final antes de aplicar esta guía.

- **SEO:** que el sitio aparezca en los buscadores.
- **GEO** (también llamado AEO): que el negocio aparezca y sea citado en las respuestas de asistentes de IA y en las respuestas generadas de los buscadores.
- **CRO:** que más visitantes hagan lo que el negocio necesita: escribir, comprar, agendar.

"A la medida" significa que nada de esto sale de una lista genérica. Sale de quién busca, qué escribe, desde dónde, en qué idioma y qué le impide decidirse.

El plan se esboza en la Fase 2 (va en el brief), se construye en la Fase 5 y se verifica aquí.

## 1. Punto de partida: la investigación del negocio

Antes de tocar etiquetas, responde con el usuario:

- **¿Qué escribiría un cliente ideal?** Por servicio, por problema ("fuga de agua urgente"), por comparación, por zona ("dentista en Zapopan").
- **¿Qué intención hay detrás?** Informarse, comparar, comprar o contratar ya. Cada intención pide una página distinta.
- **¿Qué preguntas hace la gente antes de contratar?** Las que el cliente responde por teléfono todos los días son el mejor contenido posible.
- **¿Quién aparece hoy?** Revisa los primeros resultados y qué ofrecen que este negocio pueda superar.
- **¿En qué idioma y país?** El español de México y el de otros países usan palabras distintas para lo mismo.

Resultado: un mapa de páginas, cada una con su tema principal y su intención. Una página, un tema.

## 2. SEO técnico

- El contenido está en el HTML que entrega el servidor.
- Un título y una descripción únicos por página, escritos para la persona que busca.
- Un solo encabezado principal por página; subtítulos en orden.
- Direcciones limpias, estables y legibles. Dirección canónica declarada.
- `sitemap.xml` y `robots.txt` correctos. **El entorno de pruebas va oculto a buscadores; el de producción, no.** Compruébalo al publicar: es un error clásico y muy costoso.
- HTTPS, adaptado a celular, y métricas de rendimiento en objetivo.
- Datos estructurados en JSON-LD donde correspondan de verdad: organización o negocio local, producto, artículo, preguntas frecuentes, migas de pan. Valídalos con la herramienta oficial.
- Etiquetas para compartir en redes y mensajería: título, descripción e imagen.
- Texto alternativo en imágenes. Enlaces internos con texto descriptivo.
- **Si se sustituye un sitio existente:** inventario de las direcciones actuales y redirección permanente de cada una a su equivalente. Sin esto se pierde la posición ganada.

## 3. Contenido

- Responde la pregunta real en las primeras líneas y luego amplía.
- Demuestra experiencia: quién está detrás, casos reales, fotos propias, precios o rangos, zonas de servicio, horarios.
- Contenido propio y específico. El texto genérico de relleno no posiciona y resta confianza.
- Página "Quiénes somos" y datos de contacto completos y coherentes.
- No crees páginas casi idénticas por ciudad si el negocio no atiende realmente ahí.

## 4. SEO local

Para negocios con local o zona de servicio, suele ser lo que más clientes trae:

- Perfil de empresa en Google completo: categoría, horarios, fotos, servicios. Es una cuenta del cliente.
- Nombre, dirección y teléfono idénticos en el sitio, el perfil y los directorios.
- Datos estructurados de negocio local.
- Reseñas reales y respuesta a todas.
- En México, botón de WhatsApp visible. Mapa cargado al interactuar, no al abrir.

## 5. Sitios en dos idiomas

- Una dirección por idioma (`/es/`, `/en/`) y etiquetas `hreflang` que las relacionen.
- Traducción real, revisada por alguien que hable el idioma. No traducción automática sin revisar.
- No redirijas automáticamente por ubicación; ofrece el cambio de idioma a la vista.
- La investigación de búsquedas se hace por separado en cada idioma.

## 6. GEO: aparecer en respuestas de IA

Estado a noviembre de 2026: la guía oficial de Google sobre sus funciones de IA generativa dice que se apoyan en los mismos sistemas de búsqueda, por lo que **las buenas prácticas de SEO siguen siendo la base**. No hacen falta archivos especiales, marcado "para IA" ni reescrituras en fragmentos. Desconfía de quien venda trucos.

Lo que sí ayuda, porque ayuda a cualquier sistema a entender y citar un negocio:

- **Respuestas directas y completas** a preguntas concretas, cerca del inicio de la página.
- **Datos específicos y verificables:** precios, medidas, plazos, zonas, horarios, garantías.
- **Identidad clara:** el mismo nombre del negocio en todas partes, página de "Quiénes somos", datos estructurados de organización con enlaces a sus perfiles oficiales.
- **Información propia** que no esté en otros sitios: casos, cifras, comparativas, experiencia.
- **Menciones en fuentes de terceros:** directorios del sector, prensa local, reseñas, asociaciones. Los asistentes se apoyan en lo que otros dicen del negocio.
- **Contenido rastreable:** en HTML, sin muros de inicio de sesión para lo público.

Dos decisiones que se consultan con el cliente:

- **Acceso de los rastreadores de IA** en `robots.txt`. Si el objetivo es visibilidad, se permite. Si el cliente no quiere que su contenido se use para entrenar modelos, se puede restringir, sabiendo que reduce su presencia.
- **Archivo `llms.txt`:** es opcional. Google declara que no le da trato especial; otros asistentes podrían leerlo. Costo bajo y beneficio incierto: dilo así.

Medición: visitas que llegan desde asistentes de IA en la analítica, y pruebas manuales periódicas preguntando a los asistentes lo que preguntaría un cliente. No hay todavía una medición tan fiable como la de buscadores: no prometas resultados.

## 7. CRO: convertir visitas en clientes

- **Un objetivo principal por página.**
- **Propuesta de valor en la primera pantalla,** en palabras llanas: qué ofreces, para quién y por qué elegirte.
- **Llamada a la acción clara y repetida** en puntos naturales, con verbo y beneficio: "Agenda tu valoración gratis".
- **Menos fricción:** menos campos, menos pasos, sin registro obligatorio para comprar o contactar.
- **Confianza:** testimonios reales con nombre, fotos reales, garantías, políticas claras, datos de contacto visibles, precios o rangos.
- **Velocidad:** cada segundo de espera reduce las conversiones.
- **Celular:** botón principal al alcance del pulgar; teléfono y WhatsApp con un toque.
- **Textos pequeños que resuelven dudas** junto a la acción: "Sin costo", "Respondemos en menos de 24 horas".
- **Errores recuperables:** el formulario nunca pierde lo escrito.

Recorre el embudo completo como lo haría un cliente, en un celular, y anota cada punto de duda o de espera.

### Medir las conversiones
- Define los eventos: clic en WhatsApp, clic en teléfono, envío de formulario, inicio y fin de compra.
- Analítica instalada y probada antes de publicar. Hay alternativas que no usan cookies y simplifican el cumplimiento legal.
- El consentimiento para rastreadores depende del mercado (ver `legal-privacidad.md`).
- **Pruebas A/B solo con tráfico suficiente.** Con pocas visitas no dan resultados fiables: haz un cambio a la vez y compara periodos.
- Grabaciones de sesión y mapas de calor solo con aviso y consentimiento; en Estados Unidos hay demandas por usarlos sin avisar.

## 8. Al publicar

- [ ] Sitio verificado en la consola de búsqueda de Google y en la de Bing. Mapa del sitio enviado.
- [ ] Producción visible para buscadores; pruebas oculto.
- [ ] Redirecciones del sitio anterior funcionando.
- [ ] Analítica y eventos de conversión registrando datos reales.
- [ ] Datos estructurados validados.
- [ ] Medición inicial guardada en `ESTADO.md`: es el punto de comparación.

Dile al usuario lo que puede esperar: el SEO tarda semanas o meses en mostrar efecto, y nadie puede garantizar una posición.

## 9. Apps móviles

Optimización en las tiendas: nombre, subtítulo, palabras clave, descripción, capturas que muestran el beneficio y valoraciones. Enlaces profundos entre el sitio y la app.

## Fuentes para verificar

- Google Search Central: guía de inicio de SEO, "Optimizing for generative AI features on Google Search" y políticas contra spam. developers.google.com/search
- schema.org y la herramienta de prueba de resultados enriquecidos de Google.
- web.dev: rendimiento y experiencia de página.
