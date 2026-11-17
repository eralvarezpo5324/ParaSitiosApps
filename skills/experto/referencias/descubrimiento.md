# Fase 1 · Descubrimiento

Revisado: 17 de noviembre de 2026 (requisito de prueba cerrada de Google Play verificado en la ayuda de Play Console).

El objetivo es entender el negocio lo suficiente para proponer algo mejor que lo que se pidió. Preguntar bien ahorra reconstruir después.

## Cómo preguntar

- Lee primero la descripción libre que dio el usuario en la Fase 0. **No preguntes lo que ya contestó.**
- Rondas de 3 o 4 preguntas. Cada una con 2 a 4 opciones, la recomendada primero.
- Ninguna pregunta de una ronda puede depender de la respuesta a otra de la misma ronda. Si depende, va en la ronda siguiente.
- Añade siempre la salida "No lo sé, hay que preguntarle al cliente" cuando el proyecto sea de un cliente. Esa respuesta no bloquea: la pregunta pasa a `preguntas-cliente.md` y sigues con un supuesto razonable, anotado como supuesto.
- Di al inicio cuántas rondas serán. Al cerrar cada una, resume en 3 a 5 viñetas y guarda en `ESTADO.md`.
- Pregunta por el problema, no por la solución. "¿Qué debe poder hacer un visitante?" sirve más que "¿quiere un carrito?".

**Formato cuando no hay herramienta de opciones:**

```
Ronda 2 de 3 · Funciones

1. ¿Los visitantes necesitan crear una cuenta?
   a) No, todo es público (Recomendado: más simple y más seguro)
   b) Sí, para ver sus pedidos
   c) No lo sé, hay que preguntarle al cliente

Responde así: 1a, 2c, 3b
```

## Qué bloques preguntar según la ruta

| Bloque | Exprés | Estándar | Completa |
|---|---|---|---|
| A. Negocio y objetivo | Sí | Sí | Sí |
| B. Usuarios | Breve | Sí | Sí |
| C. Funciones | Breve | Sí | A fondo |
| D. Contenido e idiomas | Sí | Sí | Sí |
| E. Marca y estilo | Sí | Sí | Sí |
| F. Referencias | Sí | Sí | Sí |
| G. Publicación y cuentas | **Sí, siempre** | **Sí, siempre** | **Sí, siempre** |
| H. Datos, pagos y legal | Solo si hay formulario | Sí | A fondo |
| I. Plazo, presupuesto y mantenimiento | Sí | Sí | Sí |
| J. Cómo se medirá el éxito | Una pregunta | Sí | Sí |

## Banco de preguntas

Elige y adapta. No las leas todas en orden.

### A. Negocio y objetivo
- ¿A qué se dedica el negocio, en una frase?
- ¿Cuál es la acción más importante que debe hacer un visitante? Opciones: llamar o escribir por WhatsApp; llenar un formulario; comprar; agendar una cita; registrarse; informarse.
- ¿Qué problema hay hoy? Opciones: no existe sitio; el actual se ve viejo; no aparece en Google; no genera contactos; es lento o falla; no se puede actualizar.
- ¿Existe un sitio o app actual? Si existe, pide la dirección: hay que conservar lo que funciona y las direcciones que ya están en Google.
- ¿Quiénes son los competidores directos? Pide uno o dos enlaces.

### B. Usuarios
- ¿Quién lo va a usar? Edad aproximada, qué tanto usa tecnología, si entra desde el celular o la computadora.
- ¿En qué situación llega? Con prisa, comparando precios, buscando confianza, por recomendación.
- ¿Hay tipos de usuario distintos? Visitante, cliente, empleado, administrador. Cada tipo adicional multiplica el trabajo de permisos y pruebas.

### C. Funciones
Parte de "¿qué debe poder hacer cada tipo de usuario?". Después profundiza según lo que aparezca:

| Si menciona | Pregunta de seguimiento obligada |
|---|---|
| Cuentas o inicio de sesión | ¿Quién crea las cuentas? ¿Qué puede ver cada tipo? ¿Cómo se recupera la contraseña? ¿Se podrá borrar la cuenta? |
| Pagos | ¿Pago único o suscripción? ¿Qué pasarela? ¿Se necesita factura (CFDI en México)? ¿Qué pasa con devoluciones y reembolsos? |
| Tienda o catálogo | ¿Cuántos productos? ¿Quién los actualiza y cada cuánto? ¿Hay inventario, variantes, envíos, impuestos? |
| Citas o reservas | ¿Quién confirma? ¿Cancelaciones y reagendado? ¿Qué pasa si no llega el cliente? ¿Varias sucursales o zonas horarias? |
| Formulario de contacto | ¿A dónde llegan los mensajes? ¿Quién responde y en cuánto tiempo? |
| Blog o noticias | ¿Quién escribe y cada cuánto? Si nadie lo hará, es mejor no incluirlo. |
| Panel de administración | ¿Qué exactamente necesita cambiar el cliente sin ayuda? |
| Notificaciones | ¿Por correo, WhatsApp, SMS o notificación en el celular? ¿Quién paga el envío? |
| App móvil | ¿Qué necesita del teléfono que una página web no pueda dar? Cámara, notificaciones, uso sin conexión, presencia en la tienda de apps. ¿Cómo llegará a los teléfonos? Ver bloque G. |
| Chat | ¿Propio o enlace a WhatsApp? El enlace a WhatsApp resuelve casi siempre. |
| Varios idiomas | ¿Quién traduce y quién mantiene las traducciones al día? |
| Mapas, calendarios, facturación, CRM | ¿Con qué sistema exacto se conecta y quién tiene esa cuenta? |
| Subir archivos | ¿Qué tipo, de qué tamaño, quién puede verlos después? |
| Datos de salud, menores, finanzas | Marca el proyecto como de datos sensibles: sube a ruta Completa y revisa `legal-privacidad.md`. |

### D. Contenido e idiomas
- ¿Quién entrega los textos y las fotos, y cuándo? Es la causa más común de retraso.
- ¿Las fotos son propias, de un fotógrafo o de banco de imágenes? Hay que confirmar los derechos de uso.
- ¿En qué idioma o idiomas estará?

### E. Marca y estilo
El usuario no puede juzgar colores. Pregunta por sensación y por lo que ya existe:
- ¿El cliente ya tiene logotipo y colores definidos? Pide el archivo del logotipo y los códigos de color si los tiene, o un manual de marca.
- ¿Qué tres palabras deben describir el sitio? Opciones para elegir: serio, cercano, elegante, moderno, divertido, sobrio, cálido, tecnológico, artesanal, minimalista.
- ¿Qué NO debe parecer? Ayuda tanto como lo anterior.
- ¿Hay tipografía definida?

### F. Referencias de sitios y animaciones
Pide **dos o tres sitios** que le gusten al usuario o a su cliente, y para cada uno:
- El enlace.
- Qué le gusta exactamente: la estructura, el estilo, una sección, la forma de mostrar los productos.
- Qué no le gusta.

Si quiere **animaciones**, pide para cada una:
- El enlace y el momento exacto: "al bajar a la segunda sección", "al pasar el cursor por las tarjetas".
- Qué le gusta: la velocidad, la suavidad, la sorpresa.

Si tienes navegador, visita las referencias y describe con palabras lo que ves: estructura, ritmo, densidad, tipo de movimiento. De una referencia se toman principios, nunca se copia. Clasifica cada animación con la tabla de `animacion.md` para estimar su costo.

Si no da referencias, propón tú tres direcciones de estilo descritas con palabras y pide que elija una.

### G. Publicación y cuentas (obligatorio)
No pases a la Fase 3 sin esto:
- **¿Dónde se va a publicar?** Opciones: hosting que el cliente ya tiene; hosting que el usuario administra; todavía no hay, recomiéndame; tiendas de apps.
- **¿Qué tipo de hosting es?** Opciones: compartido con cPanel; servidor propio o VPS con acceso completo; plataforma moderna; no lo sé. Si no lo sabe, guíalo paso a paso para averiguarlo con `despliegue.md`.
- **¿Quién tiene los accesos?** Dominio, hosting, correo. ¿A nombre de quién están?
- **¿El dominio ya existe?** ¿El correo del negocio usa ese dominio? Mover el sitio sin cuidado puede tirar el correo.

**Para apps móviles**, además (el dominio sigue importando: la política de privacidad y la página para borrar la cuenta van en la web):
- **¿Cómo llegará a los teléfonos?** Va primero, en la Fase 0 si ya sabías que era app.
  a) Android: primero un APK de prueba y después Google Play (Recomendado: se prueba en teléfonos reales desde el primer hito y después llega a cualquiera)
  b) Android y iPhone, por Google Play y App Store
  c) Solo un APK instalado directo en teléfonos conocidos, sin tienda (uso interno)
  d) No lo sé, recomiéndame
- **¿Existe ya la cuenta de desarrollador de Google Play? ¿Es personal o de empresa, y a nombre de quién?** Si es personal y se creó después del 13 de noviembre de 2023, o aún no existe y será personal, la publicación espera una prueba cerrada de 14 días con al menos 12 personas (`movil.md`, sección 8). Dilo ya: cambia el plazo.
- **¿Quién reunirá a las personas de la prueba cerrada?** Más de 12, cada una con teléfono Android y cuenta de Google, dispuestas a usar la app dos semanas.
- Si también va a iPhone: ¿existe la cuenta de Apple, y a nombre de quién?

### H. Datos, pagos y legal
- ¿Qué datos de personas se van a guardar? Nombre, correo, teléfono, dirección, documentos, pagos.
- ¿Dónde están el negocio y sus usuarios? Define la ley aplicable, sin importar el idioma.
- ¿Ya existen aviso de privacidad y términos y condiciones?
- ¿Se enviará publicidad por correo, WhatsApp o SMS?
- ¿Pueden usarlo menores de edad?

### I. Plazo, presupuesto y mantenimiento
- ¿Hay una fecha que no se puede mover? Un evento, una campaña, una temporada.
- ¿El presupuesto permite servicios de pago mensual o todo debe caber en el hosting actual?
- ¿Quién actualizará el contenido después de la entrega?
- ¿Quién dará mantenimiento técnico: actualizaciones, respaldos, renovaciones?

### J. Cómo se medirá el éxito
- ¿Qué número debe mejorar? Contactos por semana, ventas, citas, descargas, tiempo ahorrado.
- ¿Cuál es el número hoy? Sin punto de partida no se puede demostrar la mejora.

## Qué guardar al terminar

En `ESTADO.md`: respuestas, supuestos (marcados como tales), preguntas abiertas para el cliente y las referencias con lo que se tomará de cada una. Con eso pasas a la Fase 2.
