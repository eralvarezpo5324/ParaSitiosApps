# Apps móviles

Revisado: noviembre de 2026. **Los requisitos de las tiendas cambian varias veces al año.** Antes de planear fechas o costos, verifica las fuentes oficiales del final. Los datos marcados "(verificar)" son una foto de esta fecha.

## 1. ¿De verdad hace falta una app?

Es la primera pregunta, y muchas veces la respuesta ahorra meses al cliente.

| El cliente necesita | Recomendación |
|---|---|
| Mostrar información, catálogo, citas o ventas, sin funciones del teléfono | Sitio web bien hecho. Sin app |
| Icono en la pantalla de inicio, uso sin conexión básico, sin pasar por las tiendas | Aplicación web instalable (PWA) |
| Presencia en las tiendas, notificaciones fiables, cámara, ubicación, uso sin conexión | App multiplataforma |
| Rendimiento extremo, realidad aumentada, integración profunda con una plataforma | App nativa para cada sistema |

Límites de la PWA que debes decir: en iPhone las notificaciones exigen que la persona la instale en su pantalla de inicio, no aparece en la tienda y algunas funciones del teléfono no están disponibles.

Una app que solo envuelve un sitio web suele ser rechazada por Apple por "funcionalidad mínima".

## 2. Elegir el enfoque

| Enfoque | Cuándo conviene | Ojo con |
|---|---|---|
| Multiplataforma con React Native y Expo | Opción por defecto para este usuario: un solo código, mismo lenguaje que la web, compilación en la nube sin necesidad de una Mac y actualizaciones sin pasar por revisión para cambios de JavaScript | Funciones muy específicas del sistema requieren módulos nativos |
| Multiplataforma con Flutter | Interfaz muy personalizada e idéntica en ambos sistemas | Otro lenguaje (Dart); no comparte código con la web |
| Envolver una aplicación web existente | Ya existe una aplicación web sólida y se necesitan pocas funciones del teléfono | Riesgo de rechazo si no aporta nada frente al sitio |
| Nativa | Requisitos que lo otro no cubre | Doble desarrollo y doble mantenimiento |

Consulta la versión estable actual y los requisitos de cada herramienta antes de empezar.

## 3. Lo que el cliente debe saber desde el primer día

Dilo en la Fase 2, porque afecta costo y plazo:

- **Cuentas de desarrollador a nombre del cliente.** Apple cobra una cuota anual y Google un pago único (verificar importes). Para registrarse como empresa, Apple pide un número D-U-N-S, que puede tardar días o semanas. **Empieza estos trámites al iniciar el proyecto.**
- **Cuentas personales nuevas en Google Play:** exigen una prueba cerrada con un grupo de personas durante un periodo antes de poder publicar (verificar condiciones vigentes).
- **La revisión tarda** y puede rechazar la app. Nunca prometas una fecha de publicación exacta.
- **Política de privacidad pública** obligatoria, y declaración de qué datos recoge la app en ambas tiendas.
- **Eliminación de cuenta:** si la app permite crear cuentas, debe permitir borrarlas desde la app. Google pide además un enlace web para solicitarlo.
- **Cobros dentro de la app:** los bienes y servicios digitales deben cobrarse con el sistema de la tienda, que cobra comisión. Los bienes físicos y servicios del mundo real, no. Las excepciones cambian según país y fecha: verificar siempre.
- **Inicio de sesión con terceros:** si se ofrece, Apple exige ofrecer también una opción equivalente que proteja la privacidad, como "Iniciar sesión con Apple" (verificar excepciones).
- **Requisitos técnicos anuales (verificar):** a noviembre de 2026, Google Play exige que las apps nuevas y las actualizaciones apunten al nivel de API 36 (Android 16), y la App Store exige compilar con el SDK de iOS 26. Esto sube cada año: el mantenimiento anual no es opcional.
- **Mantenimiento:** una app sin actualizar acaba retirada de las tiendas.

## 4. Arquitectura

- **Backend:** casi toda app lo necesita. Se decide con `arquitectura.md`. Si hay sitio web, comparten el mismo backend.
- **Sesión:** tokens en el almacenamiento seguro del sistema.
- **Sin conexión:** define qué se puede consultar sin red, qué se puede hacer y cómo se resuelven los conflictos al volver la conexión.
- **Notificaciones:** servicio de envío, permiso pedido en el momento en que tiene sentido y no al abrir la app, y qué pasa si la persona lo niega.
- **Enlaces profundos:** enlaces universales que abren la pantalla correcta.
- **Actualización obligatoria:** mecanismo para pedir actualizar cuando una versión vieja ya no es compatible o segura.
- **Reporte de fallos y analítica,** con el consentimiento que corresponda.

## 5. Seguridad móvil

Marco de referencia: OWASP MASVS. La regla que lo resume: **todo lo que va dentro de la app es público.** Cualquiera puede descargarla y extraer su contenido.

- **Ningún secreto en la app:** ni llaves de servicios de pago, ni llaves de administrador, ni contraseñas. Lo que necesite un secreto se hace en el servidor.
- **Todas las reglas en el servidor.** La app es solo una pantalla: permisos, precios y validaciones se comprueban atrás.
- Tokens en el llavero del sistema (Keychain en iOS, Keystore en Android). Nunca en almacenamiento sin cifrar.
- Solo conexiones HTTPS. Fijar certificados solo si el modelo de amenazas lo justifica: añade riesgo de dejar la app sin servicio.
- Valida todo lo que llega por enlaces profundos antes de usarlo.
- Biometría con las API del sistema, como comodidad sobre una sesión real, no como sustituto.
- Sin datos personales en registros ni en reportes de fallos.
- Pantallas sensibles ocultas en la vista de apps recientes, cuando el riesgo lo pida.
- Ofuscar el código no es una medida de seguridad.
- Permisos del teléfono: solo los necesarios, pedidos en contexto y con explicación.
- Auditoría de dependencias igual que en web.

## 6. Diseño

- Sigue las convenciones de cada plataforma: guías de interfaz de Apple y Material Design de Google. Una app que se comporta distinto a lo esperado se siente rota.
- Áreas seguras (muesca, barra inferior), zonas táctiles de 44 puntos en iOS y 48 dp en Android.
- Respeta el tamaño de texto del sistema, el modo oscuro y el ajuste de reducir movimiento.
- Compatible con lectores de pantalla: VoiceOver y TalkBack.
- La paleta sigue el protocolo de `color-daltonismo.md`. Si hay modo oscuro, se verifica como segunda paleta.

## 7. Pruebas

- **En teléfonos reales:** al menos un Android de gama baja o media y un iPhone. El simulador no muestra los problemas de rendimiento.
- Canales de prueba de las tiendas para que el usuario y el cliente instalen versiones previas.
- Casos propios de móvil: sin conexión, conexión lenta, llamada entrante a mitad de una acción, app en segundo plano, permisos negados, pantalla girada, texto del sistema muy grande.
- Prueba guiada para el usuario por cada hito, igual que en web.

## 8. Publicación

Lo que solo puede hacer el usuario o su cliente, guiado paso a paso y de uno en uno:
- Crear y verificar las cuentas de desarrollador, con verificación en dos pasos.
- Aceptar contratos y llenar datos fiscales y bancarios si hay cobros.
- Invitar al usuario como miembro del equipo, sin compartir la cuenta principal.

Lo que preparas tú:
- Ficha de la tienda: nombre, subtítulo, descripción, palabras clave y capturas, en el idioma de cada mercado.
- Declaraciones de privacidad y de datos, coherentes con lo que la app hace de verdad.
- Clasificación por edades y respuestas sobre cifrado.
- Notas para el revisor con una cuenta de prueba, si la app requiere iniciar sesión.

Si rechazan la app: lee el motivo exacto, corrige eso y responde con claridad. Es normal y no es un fracaso.

## Fuentes para verificar

- Apple, App Store Review Guidelines y requisitos de envío: developer.apple.com
- Google Play, centro de políticas y requisito de nivel de API: support.google.com/googleplay/android-developer
- Documentación de Expo, React Native y Flutter: docs.expo.dev, reactnative.dev, flutter.dev
- OWASP MASVS: mas.owasp.org
