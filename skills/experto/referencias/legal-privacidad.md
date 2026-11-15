# Legal y privacidad: México y Estados Unidos

Revisado: noviembre de 2026. **Las leyes cambian y esta guía no es asesoría legal.** Sirve para no olvidar requisitos y para saber qué preguntar. Los textos que redactes se entregan marcados como "BORRADOR: revisar con un abogado". En proyectos de salud, finanzas, menores o datos sensibles, la revisión legal es un requisito del proyecto.

## Qué ley aplica

La ley depende de **dónde opera el negocio y dónde están sus usuarios**, no del idioma. Un negocio de Texas con clientes que hablan español sigue las leyes de Estados Unidos. Un sitio mexicano que vende a residentes de California puede quedar sujeto a normas de ese estado. Pregúntalo en la Fase 0 y anótalo en `ESTADO.md`.

Los textos legales se escriben en el idioma de los usuarios. Si el sitio es bilingüe, en ambos.

## México

### Datos personales
Ley vigente: Ley Federal de Protección de Datos Personales en Posesión de los Particulares, publicada en el Diario Oficial el 20 de marzo de 2025, que sustituyó a la de 2010. La autoridad ya no es el INAI: sus funciones pasaron a la Secretaría Anticorrupción y Buen Gobierno. Avisos de privacidad anteriores a esa fecha deben revisarse.

Lo que el proyecto necesita:

- **Aviso de privacidad** a disposición de la persona en el momento en que entrega sus datos: enlazado en cada formulario y en el pie de página. Puede haber una versión completa y una simplificada o corta que remita a la completa.
- El aviso debe decir, como mínimo: quién es el responsable y su domicilio; qué datos se recaban y si alguno es sensible; para qué se usan, distinguiendo los fines que requieren consentimiento; cómo ejercer los derechos de acceso, rectificación, cancelación y oposición (ARCO); si los datos se transfieren a terceros; cómo se avisará de cambios al aviso; y el uso de cookies u otras tecnologías de rastreo. Confirma la lista contra el texto vigente de la ley.
- **Consentimiento:** en general basta el consentimiento tácito tras poner el aviso a disposición. Los datos financieros o patrimoniales requieren consentimiento expreso, y los sensibles (salud, origen, creencias, biométricos, entre otros) consentimiento expreso y por escrito. Confirma estos supuestos en el texto vigente antes de diseñar el formulario.
- **Un canal real para solicitudes ARCO,** con alguien responsable de contestarlas en plazo.
- **Medidas de seguridad** proporcionales a los datos, y aviso a los titulares si ocurre una vulneración que afecte de forma significativa sus derechos.
- **Proveedores** que tratan datos por cuenta del negocio (hosting, correo, analítica): identificados y con sus condiciones revisadas.

### Comercio electrónico
- Ley Federal de Protección al Consumidor: identidad y domicilio del proveedor, precio total con impuestos incluidos, costos de envío antes de pagar, términos y condiciones, política de cambios y devoluciones, y un medio para reclamaciones.
- Publicidad veraz. Promociones con vigencia y condiciones.
- **Factura (CFDI):** si el negocio debe facturar, se resuelve con un proveedor autorizado de certificación. El criterio fiscal lo confirma el contador del cliente.

### Publicidad
- Correo y mensajes de promoción, solo con consentimiento y con forma de darse de baja.
- Existe un registro público para no recibir publicidad telefónica: si el negocio hace llamadas o envía mensajes promocionales, debe consultarlo.

## Estados Unidos

No hay una ley federal general de privacidad. Aplican leyes federales por tema, leyes de cada estado y el riesgo de demandas.

### Privacidad
- **Leyes estatales:** alrededor de veinte estados tienen leyes generales de privacidad en vigor en 2026 y el número crece cada año. La mayoría tiene umbrales de tamaño que un negocio pequeño no alcanza, pero no todas: verifica el estado del cliente y el de sus usuarios.
- **California:** una norma anterior exige una política de privacidad visible a cualquier sitio que recoja datos personales de residentes de California, sin umbral de tamaño. En la práctica, todo sitio con formulario debe tener una.
- **Regla general de la autoridad federal de comercio:** lo que la política de privacidad dice, se cumple. Prometer algo y no hacerlo es práctica engañosa.
- **Menores de 13 años:** la ley federal exige consentimiento verificable de los padres. La regla se actualizó en 2025. Lo más simple es no dirigirse a menores ni recoger sus datos.
- **Señal de control de privacidad del navegador:** varios estados obligan a respetarla como solicitud de exclusión.
- **Salud, finanzas, educación y biométricos** tienen leyes propias y estrictas. Si el proyecto los toca, revisión legal obligatoria.

### Rastreadores, chat y grabación de sesiones
Hay muchas demandas, sobre todo en California, contra sitios que usan píxeles de publicidad, grabación de sesiones o chats de terceros sin avisar ni pedir consentimiento. Regla práctica: ningún rastreador, grabación de sesión o chat de terceros se activa antes del consentimiento, y la política de privacidad los menciona.

### Accesibilidad
La ley de personas con discapacidad (ADA) se aplica a negocios abiertos al público y los tribunales la extienden a sus sitios web. No existe una norma técnica federal obligatoria para empresas privadas, pero las demandas son frecuentes y el criterio que usan tribunales y acuerdos es WCAG nivel AA. Para todo cliente en Estados Unidos:
- WCAG 2.2 nivel AA es requisito del proyecto (ver `diseno.md`).
- Declaración de accesibilidad con un medio de contacto.
- Evita las capas automáticas que prometen accesibilidad instantánea: no la dan y no protegen de demandas.

### Comunicaciones
- **Correo comercial:** remitente veraz, dirección postal física y baja que funcione y se respete.
- **Mensajes de texto y llamadas automáticas:** consentimiento previo expreso y por escrito, con constancia. Las multas se calculan por mensaje.

### Comercio
- **Impuesto sobre ventas:** depende del estado y del volumen vendido en cada uno. Decisión del contador del cliente; avísale al usuario que existe el tema.
- Términos de servicio, política de devoluciones y, en suscripciones, cancelación tan fácil como la contratación.

## Visitantes de la Unión Europea

Si el sitio se dirige a residentes de la Unión Europea, aplica su reglamento de protección de datos: base legal para cada uso, consentimiento previo para cookies no esenciales y derechos ampliados. Si no se dirige a ellos, basta con no hacerlo de forma activa.

## Pagos

Con cobro totalmente alojado por la pasarela, el negocio queda en el nivel más sencillo de la norma de seguridad de tarjetas (PCI DSS). Guardar o transmitir datos de tarjeta por cuenta propia no es viable en estos proyectos.

## Lista de comprobación por proyecto

- [ ] País o países del negocio y de sus usuarios anotados en `ESTADO.md`.
- [ ] **Inventario de datos** en `arquitectura.md`: qué dato, para qué, dónde se guarda, quién accede, cuánto tiempo y qué proveedor interviene.
- [ ] Aviso o política de privacidad enlazado en cada formulario y en el pie de página.
- [ ] Casilla de consentimiento sin marcar por defecto, donde la ley la pida.
- [ ] Rastreadores y herramientas de terceros solo después del consentimiento, según el mercado.
- [ ] Términos y condiciones. En tiendas: precios con impuestos, envíos, devoluciones y reclamaciones.
- [ ] Canal y responsable para solicitudes de datos personales.
- [ ] Forma de eliminar la cuenta y los datos.
- [ ] Baja de comunicaciones comerciales que funciona.
- [ ] Edad mínima definida, si hay cuentas.
- [ ] Clientes en Estados Unidos: WCAG 2.2 AA verificado y declaración de accesibilidad.
- [ ] Plan ante una vulneración: quién avisa, a quién y cómo.
- [ ] Textos legales entregados como borrador, con la recomendación de revisión por un abogado.

## Qué produces tú

- El inventario de datos.
- Borradores de aviso de privacidad, términos y política de cookies, a partir de lo que el sitio hace de verdad.
- La lista de requisitos legales dentro del brief, con lo que debe decidir o conseguir el cliente.
- En el manual de entrega: qué obligaciones quedan a cargo del cliente.

## Fuentes para verificar

- México: texto vigente de la ley en diputados.gob.mx (LFPDPPP), Secretaría Anticorrupción y Buen Gobierno, PROFECO y SAT.
- Estados Unidos: Comisión Federal de Comercio (ftc.gov), fiscal general del estado correspondiente, ADA.gov.
- Accesibilidad: W3C, WCAG 2.2.
- Reglas de la pasarela de pagos elegida.
