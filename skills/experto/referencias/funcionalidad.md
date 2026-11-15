# Fase 5 · Funcionalidad

Revisado: noviembre de 2026.

"Funciona" significa que funciona también cuando algo sale mal: sin conexión, con datos raros, con doble clic, con la sesión vencida. Esta guía define cuándo una función está terminada.

## Cuándo una función está terminada

- Cumple su caso normal y sus casos de "¿y si...?" del análisis de conflictos.
- Tiene todos sus estados (ver abajo).
- Valida en el servidor, no solo en el navegador.
- Respeta los permisos de la matriz, comprobados en el servidor.
- Tiene pruebas automáticas de lo que importa.
- Pasó la prueba guiada del usuario.
- Sigue las reglas del "momento 2" de `seguridad.md`.

## Estados de toda pantalla

Ninguna vista puede dejar a la persona sin saber qué pasa o qué hacer.

| Estado | Qué debe verse |
|---|---|
| Cargando | Indicador o estructura provisional. Si tarda, un texto que lo diga |
| Vacío | Explicación y la acción para empezar ("Aún no hay pedidos. Crea el primero") |
| Error | Qué pasó en lenguaje llano y qué puede hacer la persona. Con icono y texto, no solo color |
| Éxito | Confirmación clara de que la acción se completó |
| Sin conexión o lento | Aviso, y reintento sin perder lo escrito |
| Sin permiso | Explicación y camino de salida, no una pantalla en blanco |

Páginas de "no encontrado" y de error del servidor: útiles, con enlace al inicio y sin detalles técnicos.

## Formularios

- Etiqueta visible en cada campo. El texto de ejemplo no sustituye a la etiqueta.
- Tipo de campo y autocompletado correctos: abre el teclado adecuado en el celular y permite rellenar automáticamente.
- Pide solo lo necesario. Cada campo de más reduce los envíos.
- Valida al salir del campo, no mientras se escribe. El mensaje va junto al campo, con icono y texto, y dice cómo corregirlo.
- Si hay error, conserva todo lo que la persona escribió.
- Marca los obligatorios con texto.
- Evita el doble envío: deshabilita el botón mientras se procesa y haz que el servidor ignore duplicados.
- Confirma el resultado en pantalla y, si aplica, por correo.
- **Contra el spam:** campo trampa oculto y límite de envíos por tiempo. Un desafío tipo "no soy un robot" solo si hace falta, y que sea accesible.
- Aviso de privacidad enlazado en el punto de captura.

## Cuentas e inicio de sesión

Usa una biblioteca o servicio probado. No escribas tu propio sistema de contraseñas ni de sesiones.

Flujos que deben existir y probarse: registro, verificación de correo, inicio y cierre de sesión, recuperación de contraseña, cambio de contraseña y de correo, y eliminación de cuenta (obligatoria en las tiendas de apps y exigida por las leyes de privacidad).

- Mensajes que no revelen si un correo está registrado: "Si el correo existe, te enviamos instrucciones".
- Permite pegar contraseñas y usar gestores de contraseñas.
- La sesión vence. Al vencer, lleva a iniciar sesión sin perder a dónde iba la persona.

## Permisos

La matriz de "quién puede hacer qué" se aplica en el servidor en cada petición. Ocultar un botón no es un permiso. Prueba obligatoria: con dos cuentas, la cuenta A intenta ver y modificar datos de la cuenta B cambiando el identificador en la dirección o en la petición. Debe fallar siempre.

## Pagos

- El cobro ocurre en la página o en los campos alojados de la pasarela. Los datos de tarjeta nunca pasan por el servidor del proyecto.
- El precio lo calcula el servidor. Nunca se confía en un importe que venga del navegador.
- Estados del pedido: pendiente, pagado, fallido, reembolsado. El estado cambia por el aviso firmado de la pasarela (webhook), no por la página de "gracias".
- Los avisos de la pasarela pueden llegar repetidos o en desorden: procesa cada uno una sola vez.
- Dinero en enteros (centavos) con su moneda. Sin decimales de punto flotante.
- Impuestos: IVA en México; impuesto sobre ventas por estado en Estados Unidos. Señala al usuario que el criterio fiscal lo confirma un contador.
- Factura en México (CFDI): si el negocio la requiere, se emite con un proveedor autorizado.
- Prueba primero en el modo de pruebas de la pasarela y, antes de entregar, haz un cobro real pequeño y su reembolso.

## Fechas, idiomas y formatos

- Guarda fechas en UTC y muéstralas en la zona de la persona. La mayor parte de México ya no cambia de horario en verano, pero los municipios de la frontera norte sí siguen el cambio de Estados Unidos: usa las zonas horarias con nombre y nunca diferencias fijas de horas.
- Textos fuera del código, en archivos de idioma, aunque hoy haya un solo idioma.
- Formatos locales: fecha, números, moneda, teléfono (+52, +1), código postal, estados.
- Una dirección por idioma (`/es/`, `/en/`). No redirijas por la ubicación del visitante.

## Correo y notificaciones

- Correos transaccionales por un proveedor especializado, no con la función de correo del hosting: llegan a la bandeja y dejan registro.
- Dominio con SPF, DKIM y DMARC configurados.
- Versión de texto plano además de la de HTML. Los correos de promoción llevan enlace para darse de baja.
- Cada correo dice quién lo envía y por qué lo recibe la persona.

## Archivos que suben los usuarios

Tamaño y tipos permitidos con límite, barra de progreso, y mensaje claro si se rechaza. Las reglas de seguridad están en `seguridad.md`.

## Errores

- A la persona: mensaje llano y siguiente paso. Nunca trazas de error, consultas ni rutas del servidor.
- Al registro interno: el detalle completo, sin contraseñas ni datos personales.
- Toda operación que pueda fallar a la mitad se revierte completa o se puede repetir sin daño.

## Pruebas

Proporción según la ruta. Lo mínimo:

| Tipo | Qué cubre | Exprés | Estándar | Completa |
|---|---|---|---|---|
| Unitarias | Reglas del negocio: precios, fechas, validaciones | Si hay lógica | Sí | Sí |
| De extremo a extremo en navegador | Caminos críticos: contacto, registro, inicio de sesión, compra | Formulario | Sí | Sí |
| De permisos | A no puede ver ni tocar lo de B; el anónimo no entra | No aplica | Si hay cuentas | Sí |
| Entre navegadores y dispositivos | Chrome, Safari en iPhone, Firefox; celular y computadora | Sí | Sí | Sí |
| Accesibilidad automática | Auditoría por página | Sí | Sí | Sí |

Prueba con contenido real: nombres largos, acentos y ñ, textos muy cortos y muy largos, listas vacías y con cientos de elementos.

## Prueba guiada para el usuario

Cada hito termina con una. El usuario las sigue con facilidad; aprovéchalo.

```
PRUEBA GUIADA · Hito 2: formulario de contacto
Dónde: https://pruebas.ejemplo.com/contacto

1. Abre la página. Debes ver un formulario con tres campos y un botón que dice "Enviar mensaje".
2. Presiona "Enviar mensaje" sin escribir nada.
   Debe aparecer, junto a cada campo, un icono de alerta y un texto que dice qué falta.
3. Llena los tres campos con tus datos y presiona "Enviar mensaje".
   Debe aparecer el texto "Mensaje enviado" con una palomita.
4. Revisa tu correo. Debe llegar un mensaje con lo que escribiste, en menos de un minuto.

Respóndeme: "todo bien", o el número del paso que falló y qué viste.
```

Reglas: pasos numerados, uno por acción; el resultado esperado descrito con palabras, formas y textos, **nunca con colores**; y una forma simple de responder.

## Antes de cerrar la Fase 5

- [ ] Todas las funciones del brief cumplen la definición de terminada.
- [ ] Todas las pantallas tienen sus seis estados.
- [ ] Las pruebas automáticas pasan. Pega el resultado real.
- [ ] El usuario hizo las pruebas guiadas de todos los hitos.
- [ ] Contenido real cargado, o lista clara de lo que falta y quién lo entrega.
- [ ] `ESTADO.md` actualizado con lo construido y lo pendiente.
