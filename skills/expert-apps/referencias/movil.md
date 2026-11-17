# Apps móviles

Revisado: 17 de noviembre de 2026; la entrega en Android (sección 8) se verificó en la ayuda de Play Console, developer.android.com y la documentación de Expo. **Los requisitos de las tiendas cambian varias veces al año.** Antes de planear fechas o costos, verifica las fuentes oficiales del final. Los datos marcados "(verificar)" son una foto de esta fecha.

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

- **Cuentas de desarrollador a nombre del cliente.** Apple cobra una cuota anual (verificar importe) y Google un pago único de 25 dólares, con identificación oficial. Para registrarse como empresa, Apple y Google piden un número D-U-N-S: es gratuito, pero Google avisa que puede tardar hasta 30 días. **Empieza estos trámites al iniciar el proyecto.**
- **Cuentas personales nuevas en Google Play:** antes de publicar exigen una prueba cerrada de 14 días con al menos 12 personas, más la revisión de Google. Suma unas tres semanas al plan. Detalle en la sección 8.
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
- Versiones previas para el usuario y el cliente: en Android, un APK de prueba y después las pistas de prueba de Google Play (sección 8); en iPhone, TestFlight.
- Casos propios de móvil: sin conexión, conexión lenta, llamada entrante a mitad de una acción, app en segundo plano, permisos negados, pantalla girada, texto del sistema muy grande.
- Prueba guiada para el usuario por cada hito, igual que en web.

## 8. Entrega por etapas en Android

Explícale estos tres términos la primera vez que aparezcan:

- **APK:** el archivo que se instala directo en un teléfono Android. Sirve para probar y para uso interno sin tienda.
- **AAB (Android App Bundle):** el formato que se sube a Google Play; con él, Google arma el APK que le toca a cada teléfono. Desde agosto de 2021 es obligatorio para toda app nueva en Google Play: ahí no se sube un APK.
- **Firma:** toda app de Android va firmada con una llave. Usa la firma de apps de Google Play (Play App Signing): Google guarda la llave que firma lo que reciben los usuarios y el equipo solo usa una "llave de subida". Si esa llave se pierde, el dueño de la cuenta pide restablecerla. Sin la firma de Google Play, perder la llave obliga a publicar una app nueva.

### Las etapas

| Etapa | Qué se entrega | Quién la instala | Cuándo |
|---|---|---|---|
| 1. APK de prueba | APK firmado con un perfil de pruebas | El usuario y el cliente, directo en sus teléfonos | Desde el primer hito y en cada prueba guiada |
| 2. Prueba interna | AAB en la pista de prueba interna de Google Play | Hasta 100 personas invitadas por correo | En cuanto exista la ficha. Llega en segundos; las actualizaciones no esperan revisión, pero la primera versión de la app sí |
| 3. Prueba cerrada | AAB en la pista de prueba cerrada | Personas invitadas por listas de correo o un grupo de Google, que se apuntan con un enlace | Desde que haya una versión que se pueda usar de verdad |
| 4. Prueba abierta (opcional) | AAB en la pista de prueba abierta | Cualquiera que se apunte desde Google Play; sin límite o con un tope de 1,000 o más | Si se quiere una prueba pública antes del lanzamiento |
| 5. Producción | AAB en producción | El público | Cuando la revisión de Google lo apruebe |

Quien se apunta a la prueba interna recibe solo esa versión, aunque también esté invitado a otra pista. Las opiniones de las pruebas no afectan la calificación pública.

Con Expo (la opción por defecto de la sección 2), la compilación en la nube genera AAB por defecto. Para el APK de prueba se crea un perfil de compilación con `"buildType": "apk"` dentro de la sección `android` del archivo `eas.json`. Para Google Play se usa siempre el AAB.

### Cuentas personales nuevas: la prueba cerrada obligatoria

Google la exige a las cuentas personales creadas después del 13 de noviembre de 2023. No aplica a cuentas de organización. Si no se planea desde el principio, atrasa la publicación varias semanas.

- **Requisito:** al menos 12 personas apuntadas a una prueba cerrada **de forma continua durante los 14 días anteriores** a la solicitud. Si alguien se sale y vuelve a entrar, sus días empiezan de cero.
- **Las personas:** cada una necesita un teléfono Android y una cuenta de Google, y debe usar la app como un usuario real. Si no la usan, Google puede pedir más pruebas. Pídele al cliente desde la Fase 1 que reúna a más de 12, por si alguien se sale.
- **Después:** en el Panel de Play Console, el dueño de la cuenta presiona "Solicitar acceso a producción" y contesta un cuestionario sobre la prueba, la app y si está lista. Google suele responder en 7 días o menos.
- **Plazo realista:** unas tres semanas desde que la prueba cerrada arranca con 12 personas. Arráncala en cuanto haya una versión usable, no al final: los 14 días corren en paralelo con los hitos siguientes.
- **Alternativa:** si el cliente es una empresa, una cuenta de organización evita este requisito, pero pide número D-U-N-S.

### El salto del APK de prueba a la tienda

La versión que entrega Google Play suele quedar firmada con una llave distinta a la del APK de prueba. En ese caso el teléfono no la acepta como actualización: hay que desinstalar el APK primero, y lo que estaba guardado solo en el teléfono se pierde. Avísalo antes de que el cliente cargue datos reales en la versión de prueba.

### Si se distribuye solo con APK, sin tienda

Sirve para apps internas de un negocio (empleados, sucursales) o para pruebas. Ojo con:

- Cada persona debe permitir la instalación de apps de origen desconocido, y las actualizaciones no llegan solas: hay que mandar cada versión nueva.
- El APK se comparte por un canal privado y controlado, no en un enlace público: cualquiera que lo reciba puede instalarlo y examinar su contenido. Nada secreto dentro de la app.
- Si la app es solo para empleados, existe la distribución privada dentro de una organización. Evalúala antes de proponer el APK a mano como solución permanente.
- **Verificación de desarrolladores de Android:** desde el 30 de septiembre de 2026, en Brasil, Indonesia, Singapur y Tailandia, las apps que se descargan de tiendas participantes en teléfonos Android certificados deben estar registradas por un desarrollador con identidad verificada. Google anunció que lo extenderá a todo el mundo en 2027. A noviembre de 2026, el APK instalado directo todavía no lo exige (verificar); cuando llegue a todo el mundo, afectará también al APK de prueba de la etapa 1. Para no quedar bloqueado, registra la app desde ahora: con cuenta de Google Play, en Play Console; sin ella, en la consola para desarrolladores de Android, que tiene una cuenta gratuita de distribución limitada a 20 teléfonos y una completa con pago único de 25 dólares.

## 9. Publicación

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
- Ayuda de Play Console: "Set up an open, closed, or internal test" (answer/9845334), "App testing requirements for new personal developer accounts" (answer/14151465), "Use Play App Signing" (answer/9842756), "Get started with Play Console" (answer/6112435)
- Formato AAB: developer.android.com/guide/app-bundle
- Verificación de desarrolladores de Android: developer.android.com/developer-verification
- APK con Expo: docs.expo.dev/build-reference/apk
- Documentación de Expo, React Native y Flutter: docs.expo.dev, reactnative.dev, flutter.dev
- OWASP MASVS: mas.owasp.org
