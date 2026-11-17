# Fase 2 · Análisis de conflictos y propuesta

Revisado: 17 de noviembre de 2026 (requisito de prueba cerrada de Google Play verificado en la ayuda de Play Console).

Lo que pide un cliente casi nunca es lo que necesita, y casi siempre trae contradicciones que nadie ha notado. Tu trabajo aquí es encontrarlas antes de escribir una línea de código, y devolver una propuesta mejor que el encargo original.

## Método en cinco pasos

### 1. Matriz de quién puede hacer qué
Escribe una tabla con los tipos de usuario en columnas y las acciones en filas (ver, crear, editar, borrar, aprobar, pagar). Cada celda vacía o dudosa es una pregunta. Esta tabla será después la base del control de acceso.

### 2. Recorrido de cada función con "¿y si...?"
Para cada función, describe el camino normal y luego pregunta:
- ¿Y si el campo viene vacío, duplicado o con un formato raro?
- ¿Y si falla a la mitad? Un pago, un envío de correo, la conexión.
- ¿Y si lo hacen dos personas al mismo tiempo? El último producto, la misma cita.
- ¿Y si se arrepiente? Cancelar, editar, devolver, borrar.
- ¿Y si vence? Un enlace, una oferta, una sesión, una reserva sin pagar.
- ¿Y si alguien abusa? Mil registros falsos, cupones reutilizados, precios manipulados.

### 3. Ciclo de vida de cada dato
Para cada dato importante: quién lo crea, quién lo ve, quién lo cambia, cuánto tiempo se guarda y cómo se borra. Un dato sin dueño claro es una falla de seguridad futura.

### 4. Cruce contra los límites
Revisa cada función contra: el hosting, el presupuesto, el plazo, la ley, el contenido disponible y quién mantendrá el sitio.

### 5. Clasificación
- **Bloqueante:** no se puede construir o publicar así. Hay que resolverlo antes de avanzar.
- **Importante:** se puede construir, pero saldrá mal o caro si no se decide ahora.
- **Menor:** conviene decidirlo; hay un supuesto razonable mientras tanto.

## Catálogo de conflictos frecuentes

### Entre funciones
| Lo que piden | El conflicto | Qué preguntar o proponer |
|---|---|---|
| "Que se registren" sin decir para qué | Una cuenta sin beneficio aleja a la gente y añade riesgo | ¿Qué gana el usuario con la cuenta? Si nada, compra o contacto sin registro |
| Roles "administrador y usuario" sin más | Faltan permisos reales: quién aprueba, quién ve datos de otros | Completar la matriz del paso 1 |
| Tienda sin definir envíos, impuestos ni devoluciones | No se puede calcular un total ni cumplir con el consumidor | Zonas de envío, costos, IVA incluido, política de devolución |
| Citas en línea con agenda en papel | Doble reserva segura | ¿Cuál será la agenda única? ¿Quién confirma? |
| Pagos y también "pago al recoger" | Inventario y pedidos sin pagar | ¿Cuánto tiempo se aparta un producto sin pago? |
| Varios idiomas con contenido que cambia seguido | Las traducciones quedan atrasadas | ¿Quién traduce cada cambio? Si nadie, un solo idioma |
| Blog sin quien escriba | Sección vacía que resta confianza | Quitar el blog o comprometer un calendario |
| Buscador con veinte productos | Costo sin beneficio | Filtros simples o nada |
| Notificaciones por WhatsApp automáticas | Requiere la API oficial, con costo por mensaje y plantillas aprobadas | Enlace directo a WhatsApp o correo |
| Borrar cuentas y conservar facturas | La ley fiscal obliga a conservar ciertos datos | Separar datos de la cuenta y registros fiscales |
| Comentarios o reseñas abiertos | Spam y contenido ofensivo | ¿Quién modera? ¿Antes o después de publicar? |

### Entre funciones y hosting
| Lo que piden | El conflicto | Alternativa |
|---|---|---|
| Chat o datos en tiempo real en hosting compartido | No admite conexiones permanentes | Servicio externo de tiempo real, consulta periódica, o cambiar de hosting |
| Aplicación con Node.js en cPanel sin esa opción | No se puede ejecutar | Sitio estático con PHP para lo dinámico, o un servicio de backend externo |
| Procesos largos: reportes, envíos masivos, video | El hosting compartido corta a los pocos segundos | Tareas programadas por lotes o un servicio externo |
| Envío de muchos correos desde el hosting | Caen en spam o bloquean la cuenta | Proveedor de correo transaccional |
| Archivos grandes de video | Agota espacio y ancho de banda | Plataforma de video externa |
| Tráfico alto por temporada | El hosting compartido se cae | Sitio estático con CDN por delante |

### Entre funciones y presupuesto o plazo
| Lo que piden | El conflicto | Alternativa |
|---|---|---|
| App nativa para iOS y Android con presupuesto de página web | Dos desarrollos, cuentas, revisiones de tienda | Aplicación web instalable (PWA) o multiplataforma |
| "Como Amazon" o "como Uber" | Años de trabajo de equipos enteros | Identificar la única función que realmente necesita |
| Panel de administración a la medida para cambiar tres textos | Mucho desarrollo para poco uso | Edición de contenido sencilla o cambios por solicitud |
| Animaciones 3D con fecha en dos semanas | Riesgo de no llegar y de lentitud | Movimiento sencillo bien hecho |
| Todo para el lanzamiento | Nada se termina bien | Versión mínima primero, lo demás por etapas |

### Entre funciones y ley
| Lo que piden | El conflicto | Qué hacer |
|---|---|---|
| Formulario sin aviso de privacidad | Incumple la ley de datos personales en México | Aviso visible en el punto de captura |
| Guardar datos de tarjetas | Exige certificación que no es viable | Pago alojado por la pasarela: los datos de tarjeta nunca tocan el sitio |
| Lista de correos comprada | Ilegal o de alto riesgo según el país | Solo contactos con consentimiento |
| Mensajes SMS de promoción en Estados Unidos | Exigen consentimiento previo por escrito | Registro explícito con constancia |
| Usuarios menores de edad | Reglas especiales de consentimiento | Definir edad mínima o flujo con padres |
| Datos de salud o financieros | Obligaciones reforzadas | Ruta Completa y revisión legal |
| Sitio para público de Estados Unidos sin accesibilidad | Riesgo real de demanda | WCAG 2.2 nivel AA como requisito del proyecto |
| Herramientas de seguimiento sin consentimiento | Riesgo legal según el mercado | Consentimiento antes de activar rastreadores |

### Entre diseño, rendimiento y SEO
| Lo que piden | El conflicto | Alternativa |
|---|---|---|
| Video a pantalla completa al abrir | Página lenta y peor posición en buscadores | Imagen optimizada que se sustituye por el video al cargar |
| Carrusel automático en la portada | Casi nadie pasa de la primera imagen y perjudica la accesibilidad | Un mensaje principal claro |
| Todo el texto dentro de imágenes | Ni Google ni los lectores de pantalla lo leen | Texto real sobre la imagen |
| Sitio de una sola página y aparecer en muchas búsquedas | Una página no puede responder a todo | Una página por servicio o tema |
| Colores de marca con poco contraste | Texto ilegible | Variante accesible del color para textos, verificada por cálculo |
| Mucho movimiento | Marea a algunas personas y distrae | Movimiento con propósito y respeto a quien lo desactiva |

### Propios de apps móviles
| Lo que piden | El conflicto | Qué hacer |
|---|---|---|
| App que solo muestra el sitio web | Las tiendas la rechazan por funcionalidad mínima | Aplicación web instalable, o añadir funciones propias de app |
| Vender contenido digital con pasarela propia | Las tiendas exigen su sistema de cobro, con comisión | Revisar reglas vigentes y calcular la comisión |
| Publicar "la próxima semana" | La revisión y las cuentas tardan | Empezar los trámites de cuentas desde el primer día |
| Publicar pronto en Google Play con una cuenta personal nueva | La prueba cerrada obligatoria (12 personas, 14 días) y la revisión suman unas tres semanas | Arrancar la prueba cerrada en cuanto haya una versión usable, o usar una cuenta de organización (pide D-U-N-S). Ver `movil.md`, sección 8 |
| Funcionar sin conexión y con datos siempre al día | Se contradicen | Definir qué se consulta sin conexión y cómo se sincroniza |
| Cuenta de desarrollador a nombre del programador | El cliente pierde su app si cambia de proveedor | Cuentas a nombre del cliente |

## Optimizar la solicitud

Después de encontrar los conflictos, propón una versión mejor:

1. **Ordena por valor.** Para cada función: imprescindible para lanzar, importante pero puede esperar, o deseable.
2. **Busca la versión más simple** que cumpla el objetivo del negocio. Enlace a WhatsApp en lugar de chat propio. Formulario en lugar de cuenta. Página estática en lugar de sistema.
3. **Añade lo que falta y nadie pidió:** aviso de privacidad, página de error, respaldos, medición de resultados, quién mantiene.
4. **Propón etapas.** Lanzamiento con lo imprescindible; segunda etapa con lo importante.

## Preguntas para el cliente

Cuando el proyecto es de un cliente, redacta `preguntas-cliente.md` con la plantilla. Reglas:

- **Entre 5 y 10 preguntas**, ordenadas de mayor a menor impacto. Más de diez no se contestan.
- **Lenguaje del cliente**, sin términos técnicos. "¿Quién contestará los mensajes que lleguen del sitio?" y no "¿cuál es el flujo de atención de leads?".
- **Una decisión por pregunta**, con opciones y la consecuencia de cada una en costo o tiempo.
- **Di qué pasa si no responde:** el supuesto con el que seguirás.
- Escríbelas en el idioma del cliente.

## Salida de la fase

`brief-propuesta.md` con la plantilla: objetivo, alcance por etapas, lo que queda fuera, supuestos, conflictos resueltos y pendientes, requisitos legales, plan de SEO, GEO y CRO en pocas líneas, y plazo estimado por hitos. Después, la puerta de aprobación.
