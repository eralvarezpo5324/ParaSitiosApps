# Fase 3 · Arquitectura y elección de tecnología

Revisado: noviembre de 2026. Las versiones de herramientas cambian: consulta la versión estable actual antes de instalar cualquier cosa.

La pregunta de esta fase no es "¿cuál es la mejor tecnología?" sino "¿cuál es la más sencilla que cumple el brief, corre en el hosting del cliente y se puede mantener?".

## Principios

- **El hosting decide.** Primero averigua qué soporta; después elige.
- **Menos piezas.** Cada servicio, dependencia o proceso adicional es algo que puede fallar, costar o ser atacado.
- **Tecnología madura.** Herramientas con años de uso, documentación amplia y mantenimiento activo.
- **Contenido en HTML desde el servidor.** Lo que deba aparecer en buscadores y asistentes de IA no puede depender de que se ejecute JavaScript.
- **El cliente es dueño de todo:** dominio, hosting, cuentas y código. Evita servicios de los que no pueda salir.
- **Versiones fijadas.** Archivo de bloqueo de dependencias siempre en el repositorio.

## Paso 1. Averiguar qué soporta el hosting

Si el usuario no lo sabe, guíalo de uno en uno (detalle en `despliegue.md`). Lo que necesitas saber:

| Dato | Por qué importa |
|---|---|
| Tipo: compartido, VPS, plataforma | Define todo lo demás |
| Versión de PHP disponible | Marca qué se puede usar en hosting compartido |
| ¿Tiene "Setup Node.js App" o similar? | Si no, no hay aplicaciones Node |
| ¿Acceso por SSH o terminal? | Permite instalar dependencias y desplegar con git |
| Base de datos disponible | MySQL o MariaDB en compartido |
| Tareas programadas (cron) | Para envíos, limpiezas y respaldos |
| Certificado SSL automático | Sin HTTPS no se publica |
| Despliegue por git o solo por archivos | Define el método de publicación |
| Límites: espacio, memoria, tiempo de ejecución | Evita sorpresas con procesos largos |

## Paso 2. Elegir según el hosting

### Hosting compartido con cPanel
Lo más común entre los clientes del usuario. Funciona muy bien si se respeta lo que es.

| Necesidad | Solución recomendada |
|---|---|
| Sitio informativo o de aterrizaje | Sitio estático: se genera al construir y se suben solo archivos HTML, CSS y JavaScript. Rápido, barato y casi sin superficie de ataque |
| Formulario de contacto | Un archivo PHP pequeño que valida y envía por un proveedor de correo, o un servicio de formularios |
| Contenido que el cliente edita seguido | Evalúa en este orden: archivos de contenido que el usuario edita en nombre del cliente; un gestor de contenido ligero; WordPress con tema a la medida |
| Catálogo o tienda sencilla | PHP con MySQL, o tienda alojada enlazada desde el sitio. El pago siempre en la página de la pasarela |
| Aplicación con cuentas y datos | PHP moderno con un framework maduro si hay SSH y gestor de dependencias; o frontend estático más un servicio de backend externo |
| Tiempo real, procesos largos, Node | No aplica en compartido: servicio externo o cambio de hosting |

**Sobre WordPress.** Es válido cuando el cliente debe editar mucho contenido por sí mismo y el presupuesto es corto. "A la medida" significa tema propio, sin constructores visuales pesados y con los mínimos complementos, todos mantenidos. Di con claridad el costo: es el sistema más atacado de internet y exige actualizaciones constantes. Si nadie las hará, no lo recomiendes.

**Sobre servicios de backend externos** (base de datos, cuentas y archivos como servicio). Permiten tener una aplicación real con un frontend estático en hosting compartido. Exigen configurar bien las reglas de acceso a datos: es la falla más común y más grave (ver `seguridad.md`). Revisa costos al crecer y dónde se guardan los datos.

### VPS o servidor propio
Admite casi todo: aplicaciones Node, PHP, Python, bases de datos PostgreSQL, contenedores, tiempo real.

Antes de recomendarlo, responde: **¿quién va a mantener el servidor?** Un servidor sin actualizaciones ni respaldos es peor que un hosting compartido. Si nadie lo hará, recomienda una plataforma administrada.

Configuración base: proxy inverso con HTTPS automático, la aplicación como servicio sin privilegios de administrador, base de datos accesible solo desde el propio servidor, cortafuegos, respaldos automáticos fuera del servidor. Detalle en `despliegue.md`.

### Plataformas administradas
Cuando el cliente aún no tiene hosting, o la aplicación necesita funciones de servidor y nadie mantendrá uno. Publican desde el repositorio, dan HTTPS y versiones de prueba automáticas. Revisa el costo mensual al crecer y deja documentado cómo salir de la plataforma.

### Apps móviles
Sigue `movil.md`. La app casi siempre necesita un backend: se decide con estas mismas reglas.

## Paso 3. Modelo de datos

- Entidades, relaciones y campos, en una tabla sencilla.
- **Dueño de cada registro:** a qué usuario u organización pertenece. Es la base del control de acceso.
- **Clasificación:** público, interno, personal, sensible. Lo personal y lo sensible activan requisitos legales y de seguridad.
- Guarda lo mínimo. El dato que no se guarda no se puede filtrar.
- Dinero en enteros (centavos) con su moneda. Fechas en UTC.

## Paso 4. Modelo de amenazas

Aquí actúas como experto en ciberseguridad. Sigue el "momento 1" de `seguridad.md` y deja la tabla de amenazas y controles dentro de `arquitectura.md`. Define el nivel de seguridad: básico o reforzado.

## Paso 5. Entornos y estructura del repositorio

- **Tres entornos:** local, pruebas (un subdominio protegido con contraseña y oculto a buscadores) y producción.
- **Solo una carpeta se publica:** el resultado de la construcción (`public/`, `dist/` o la que use la herramienta). `docs/`, el código fuente, las pruebas y los archivos de configuración no se suben nunca a la carpeta pública.
- **Secretos fuera del código y fuera de la carpeta pública:** en variables de entorno. `.env` en `.gitignore` desde el primer commit, con un `.env.example` sin valores reales.

```
repositorio/
  CLAUDE.md
  docs/proyecto/        (documentos internos; nunca se publican)
  src/                  (código fuente)
  public/ o dist/       (lo único que llega al servidor)
  .env.example
  .gitignore
```

## Paso 6. Plan por hitos

- **Hito 0, esqueleto publicado:** un "hola mundo" en el hosting real, con el método real de publicación y HTTPS activo. Descubre los problemas de hosting el primer día.
- **Hitos siguientes:** cortes verticales. Cada uno entrega una función completa, de la pantalla a los datos, con sus pruebas. Empieza por la función más importante para el negocio o la de mayor riesgo técnico.
- **Último hito:** contenido real, textos legales y medición.

## Salida de la fase

`docs/proyecto/arquitectura.md` con la plantilla. Cada decisión lleva su porqué en una línea y la alternativa descartada. Al presentarla en la puerta de aprobación, explica en lenguaje llano: qué se usará, cuánto cuesta al mes, qué queda a cargo del usuario y qué riesgos se aceptan.

## Fuentes para verificar

- Documentación oficial y notas de versión de cada herramienta elegida.
- Documentación del proveedor de hosting sobre versiones de PHP, Node y límites.
- Fechas de fin de soporte de lenguajes y sistemas: no elijas versiones sin soporte.
