# Fases 8 y 9 · Publicación y entrega

Revisado: noviembre de 2026. Los paneles de hosting cambian de aspecto: describe al usuario lo que debe buscar por su nombre y confirma lo que ve en pantalla.

## Contenido

1. Averiguar qué hosting hay
2. Antes de publicar
3. Hosting compartido con cPanel
4. VPS o servidor propio
5. Plataformas administradas
6. Dominio, DNS y correo
7. Sustituir un sitio existente
8. Verificación en vivo
9. Entrega (Fase 9)

---

## 1. Averiguar qué hosting hay

Si el usuario no sabe qué tipo de hosting tiene el cliente, guíalo con una pregunta a la vez:

1. "Entra al panel del hosting. ¿En la parte superior dice cPanel, Plesk, hPanel u otro nombre?"
2. "Busca una sección llamada 'Software'. ¿Aparece 'Seleccionar versión de PHP'? ¿Qué versión marca?"
3. "En esa misma sección, ¿aparece 'Setup Node.js App'?"
4. "Busca 'Terminal' o 'Acceso SSH'. ¿Existe?"
5. "Busca 'Git Version Control'. ¿Existe?"
6. "Busca 'SSL/TLS Status'. ¿El dominio aparece con certificado activo?"

Con esas respuestas tienes lo que pide `arquitectura.md`. Si tiene acceso completo por SSH a un servidor propio, es un VPS.

## 2. Antes de publicar

- [ ] El reporte de seguridad no tiene hallazgos críticos ni altos abiertos.
- [ ] El usuario aprobó la publicación (puerta de la Fase 8).
- [ ] Existe un respaldo del sitio y la base de datos actuales, si los hay.
- [ ] Hay plan de vuelta atrás: cómo regresar a la versión anterior en minutos.
- [ ] Los secretos de producción están listos y no están en el repositorio.
- [ ] Se sabe exactamente qué carpeta se sube. **Nunca se suben:** `docs/`, `.git/`, `.env`, `CLAUDE.md`, `.claude/`, el código fuente sin construir, pruebas, respaldos ni archivos de dependencias.

## 3. Hosting compartido con cPanel

### Método de publicación, del mejor al peor
1. **Git del propio cPanel**, si existe: el repositorio se clona en el hosting y un archivo de despliegue copia solo la carpeta construida a `public_html`.
2. **Automatización desde el repositorio:** al aprobar un cambio, se construye el sitio y se sube solo el resultado por SFTP o FTPS. Las credenciales van como secretos del repositorio.
3. **Subida manual** de un archivo comprimido con el Administrador de archivos, como último recurso y guiada paso a paso.

Nunca FTP sin cifrar: la contraseña viaja a la vista.

### Estructura en el servidor
```
/home/cuenta/
  .env                 (secretos: FUERA de public_html)
  app/                 (código que no debe ser accesible desde la web)
  public_html/         (lo único público)
```

### Pasos
1. Versión de PHP con soporte vigente.
2. Base de datos nueva, con un usuario propio y solo los permisos necesarios.
3. Certificado SSL activo.
4. Publicación con el método elegido.
5. Archivo `.htaccess` de endurecimiento (abajo).
6. Tareas programadas, si las hay.
7. Correo: cuentas, y registros SPF, DKIM y DMARC.
8. Respaldos automáticos activos y una copia fuera del hosting.

### `.htaccess` base (Apache)
Punto de partida. Ajusta la CSP al proyecto y prueba cada cambio en el entorno de pruebas: un error aquí tira el sitio.

```apache
# Forzar HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Sin listado de carpetas
Options -Indexes

# Bloquear archivos ocultos (excepto .well-known) y archivos sensibles
RedirectMatch 404 /\.(?!well-known/)
<FilesMatch "\.(env|ini|log|sql|bak|old|save|sh|md|lock|json|yml|yaml)$">
  Require all denied
</FilesMatch>

# Cabeceras de seguridad
<IfModule mod_headers.c>
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
  Header always set Content-Security-Policy "default-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'"
  Header unset X-Powered-By
</IfModule>

# Compresión
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>

# Caché: larga para archivos con huella en el nombre, corta para HTML
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 5 minutes"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/avif "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
</IfModule>
```

Notas:
- El bloqueo de `.json` rompe archivos públicos legítimos como el manifiesto de una aplicación web: quita esa extensión de la lista si el sitio los usa, y bloquea por nombre los que no deben verse.
- En la carpeta de archivos subidos por usuarios, añade un `.htaccess` que impida ejecutar código: `php_flag engine off` o `Require all denied` para archivos `.php`, según el servidor.

### CDN por delante
Un servicio de CDN con plan gratuito delante del hosting compartido da velocidad, HTTPS y un filtro básico de ataques. Implica mover los servidores de nombres del dominio: sigue con cuidado la sección de DNS para no afectar el correo.

## 4. VPS o servidor propio

Endurecimiento mínimo antes de poner nada en producción:

1. Sistema actualizado y actualizaciones de seguridad automáticas.
2. Usuario propio sin privilegios de administrador. Acceso por SSH solo con llave; sin contraseña y sin entrada directa del administrador.
3. Cortafuegos: solo los puertos 22, 80 y 443.
4. Bloqueo automático de intentos repetidos de acceso.
5. Proxy inverso con HTTPS automático y las cabeceras de seguridad.
6. La aplicación corre como servicio, con un usuario sin privilegios, y se reinicia sola.
7. Base de datos accesible solo desde el propio servidor.
8. Respaldos automáticos fuera del servidor, y una restauración de prueba.
9. Vigilancia: aviso de caída, de disco lleno y de certificado por vencer. Rotación de registros.
10. Publicación automatizada desde el repositorio, no copiando archivos a mano.

Deja escrito en el manual quién aplica las actualizaciones y cada cuánto. Si nadie, este no es el hosting adecuado.

## 5. Plataformas administradas

Conectar el repositorio, definir las variables de entorno en el panel, usar las versiones de prueba automáticas y enlazar el dominio. Revisa los límites del plan y deja anotado el costo mensual esperado.

## 6. Dominio, DNS y correo

- **El dominio es del cliente,** en una cuenta suya con verificación en dos pasos y renovación automática. Perder el dominio es perder el negocio en línea.
- **Antes de cambiar cualquier registro DNS, anota todos los actuales.** Captura de pantalla o exportación.
- **El correo depende de los registros MX y de los de SPF, DKIM y DMARC.** Si el correo del negocio usa el dominio, esos registros se copian idénticos. Cambiar los servidores de nombres sin copiarlos deja al cliente sin correo.
- Reduce el tiempo de vida de los registros un día antes del cambio; restáuralo después.
- Decide una sola versión, con o sin `www`, y redirige la otra.

## 7. Sustituir un sitio existente

1. Respaldo completo del sitio y la base de datos actuales, guardado fuera del hosting.
2. Lista de todas las direcciones actuales con visitas o enlaces.
3. Redirección permanente de cada una a su equivalente en el sitio nuevo.
4. Publica en horario de poco tráfico y verifica de inmediato.
5. Conserva el sitio anterior, sin publicar, durante unas semanas.

## 8. Verificación en vivo

Inmediatamente después de publicar:

- [ ] `revisar_sitio.py https://dominio --sitio-autorizado` sin hallazgos altos. Resultado añadido al reporte de seguridad.
- [ ] HTTPS activo en todas las variantes del dominio, con y sin `www`.
- [ ] **El sitio de producción es visible para buscadores:** sin `noindex` y sin bloqueo en `robots.txt`. Lo contrario para el entorno de pruebas.
- [ ] Formularios probados con un envío real; el correo llega.
- [ ] Pagos: un cobro real pequeño y su reembolso.
- [ ] Inicio de sesión y funciones críticas probados en producción.
- [ ] Páginas de error correctas.
- [ ] Analítica y eventos de conversión registrando.
- [ ] Mapa del sitio enviado a las consolas de búsqueda.
- [ ] Probado en un celular real con datos móviles.
- [ ] Respaldos automáticos activos.

Entrega al usuario una **prueba guiada de producción** corta, con el formato de `funcionalidad.md`.

Si algo crítico falla: vuelve a la versión anterior primero y diagnostica después.

## 9. Entrega (Fase 9)

### Cuentas y accesos
- Todas las cuentas a nombre del cliente: dominio, hosting, correo, pasarela, analítica, perfil de empresa, tiendas de apps. Con verificación en dos pasos.
- El usuario queda como colaborador con su propio acceso, no con la contraseña del cliente.
- Las credenciales se transfieren con un gestor de contraseñas o un enlace de un solo uso. Nunca por chat ni correo en texto claro.
- Cambia las contraseñas temporales usadas durante el desarrollo.

### Manual de entrega
`docs/proyecto/manual-entrega.md` con la plantilla, en el idioma del cliente y sin términos técnicos: qué es cada cosa, cómo actualizar el contenido, qué hacer si algo falla, a quién llamar, qué se renueva y cuándo, y qué obligaciones legales quedan a su cargo.

### Mantenimiento
Deja por escrito qué incluye y qué no: actualizaciones, respaldos, vigilancia, cambios de contenido, tiempo de respuesta. Un sitio sin mantenimiento acordado termina vulnerable; dilo al usuario para que lo ofrezca como servicio.

### Repositorio
Decide con el usuario qué recibe el cliente. El reporte de seguridad completo es interno: al cliente se le entrega la versión resumida. Si se transfiere el repositorio, revisa antes que no contenga secretos (`buscar_secretos.py --historial`).

### Cierre
- `ESTADO.md` marcado como entregado, con la fecha y los pendientes de la segunda etapa.
- Recordatorio a 30 días: comparar las métricas contra el punto de partida y revisar actualizaciones.

## Fuentes para verificar

- Documentación del proveedor de hosting del cliente.
- Documentación del servidor web usado (Apache, Nginx u otro) para cabeceras, caché y compresión.
- Requisitos vigentes de los proveedores de correo sobre SPF, DKIM y DMARC.
