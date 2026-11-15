# Animación

Revisado: noviembre de 2026. El soporte de navegadores cambia rápido: verifica cada técnica reciente antes de usarla.

La animación es algo que el usuario sí puede juzgar. Enséñasela en movimiento y pide su aprobación por sensación: más lenta o más rápida, más sutil o más notoria.

## Para qué se anima

Cada animación debe cumplir al menos una de estas funciones. Si no cumple ninguna, se quita.

- **Orientar:** mostrar de dónde viene y a dónde va algo (un menú que se abre, un cambio de página).
- **Responder:** confirmar que una acción se registró (un botón presionado, un envío).
- **Dirigir la atención** hacia lo importante, una sola vez.
- **Dar carácter** a la marca, sin estorbar la lectura ni la tarea.

## Analizar una animación de referencia

Pide el enlace y el momento exacto. Clasifícala y estima su costo antes de prometerla:

| Efecto | Técnica | Costo y riesgo |
|---|---|---|
| Cambios al pasar el cursor o al enfocar | Transiciones de CSS | Bajo |
| Elementos que aparecen al desplazarse | Animaciones de CSS ligadas al desplazamiento, con alternativa por observador de intersección | Bajo |
| Barra de progreso de lectura, cabecera que se encoge | Animaciones de CSS ligadas al desplazamiento | Bajo |
| Transición suave entre páginas | API de transiciones de vista | Bajo a medio |
| Texto que se revela letra por letra o línea por línea | Biblioteca de animación | Medio |
| Secuencias coordinadas y líneas de tiempo complejas | Biblioteca de animación | Medio |
| Paralaje (capas a distinta velocidad) | CSS ligado al desplazamiento o biblioteca | Medio. Marea a algunas personas |
| Sección que se fija mientras se desplaza el contenido | CSS (posición fija por tramo) más biblioteca | Medio a alto |
| Ilustraciones animadas | Formatos vectoriales animados | Medio. Depende de quién las diseñe |
| Desplazamiento suavizado de toda la página | Biblioteca | Medio. Altera el comportamiento natural: evítalo salvo petición expresa |
| Escenas 3D, partículas, efectos con WebGL | Biblioteca 3D | Alto: rendimiento, batería y plazo |
| Cursor personalizado | JavaScript | Medio. No existe en pantallas táctiles |

Devuelve al usuario la clasificación en una línea: "Lo que te gusta es una aparición al desplazarse con retraso escalonado. Costo bajo. Se puede hacer con CSS."

## Reglas de ejecución

**Duración**
- Respuestas a una acción: 100 a 200 milisegundos.
- Cambios de estado de la interfaz: 200 a 400.
- Movimientos grandes o de página: 400 a 700.
- Nada debe hacer esperar más de un segundo para leer o actuar.

**Curvas**
- Entrada: desacelerando. Salida: acelerando. Lineal solo para movimiento continuo, como un indicador de carga.
- Escalonado entre elementos: 30 a 80 milisegundos, y pocos elementos.

**Rendimiento**
- Anima solo desplazamiento, escala, rotación y opacidad. Animar tamaño, márgenes o posición obliga al navegador a recalcular la página.
- No retrases el contenido principal: el título y la imagen principal deben ser visibles sin esperar a JavaScript ni a que termine una animación. Ocultarlos para animarlos empeora la métrica de carga.
- El contenido debe ser legible aunque el JavaScript falle.
- Pausa lo que no está en pantalla. Carga las bibliotecas de animación de forma diferida.
- Prueba en un teléfono Android de gama media, no solo en la computadora.

## Accesibilidad del movimiento

- **Respeta `prefers-reduced-motion`.** Quien pide menos movimiento recibe una versión sin desplazamientos ni escalados: aparición por opacidad o nada. No es opcional.
- Lo que se mueve solo durante más de cinco segundos necesita un control para pausarlo.
- Nada parpadea más de tres veces por segundo.
- Paralaje, giros y acercamientos grandes pueden causar mareo: se desactivan con movimiento reducido.
- El video de fondo va sin sonido, con control de pausa y con una imagen fija como alternativa.
- No secuestres el desplazamiento: la página debe moverse a la velocidad que la persona espera.

Base recomendada en CSS:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Escalera de técnicas

Usa el peldaño más bajo que logre el efecto. Cada peldaño añade peso y mantenimiento.

1. **Transiciones y animaciones de CSS.**
2. **Animaciones de CSS ligadas al desplazamiento** (`animation-timeline`). Estado a noviembre de 2026: disponibles en los tres motores principales desde hace muy poco. Úsalas como mejora progresiva con `@supports` y con una alternativa para navegadores anteriores.
3. **API de transiciones de vista.** Dentro de una misma página está disponible en todos los navegadores principales desde finales de 2025. Entre páginas distintas, verifica el soporte vigente y úsala solo como mejora progresiva.
4. **API de animaciones web** de JavaScript, para control fino sin bibliotecas.
5. **Bibliotecas de animación** para secuencias, texto y efectos complejos. Verifica la licencia vigente y el peso antes de elegir.
6. **Formatos vectoriales animados** para ilustraciones.
7. **WebGL y 3D,** solo cuando es la pieza central del sitio y hay presupuesto y plazo.

## En apps móviles

Usa las herramientas de animación nativas del framework y las convenciones de la plataforma. Respeta el ajuste de "reducir movimiento" del sistema. La vibración de respuesta, con moderación.

## Lista de comprobación

- [ ] Cada animación cumple una función.
- [ ] El contenido principal se ve sin esperar animaciones ni JavaScript.
- [ ] Solo se animan desplazamiento, escala, rotación y opacidad.
- [ ] Existe la versión de movimiento reducido y se probó.
- [ ] Nada se mueve solo más de cinco segundos sin control de pausa.
- [ ] Probado en un teléfono de gama media.
- [ ] Las métricas de rendimiento no empeoraron (ver `rendimiento.md`).
- [ ] El usuario vio el movimiento real y lo aprobó.

## Fuentes para verificar

- developer.mozilla.org: animaciones de CSS, `animation-timeline`, View Transitions API.
- web.dev/baseline: estado de cada función en navegadores.
- W3C, WCAG 2.2, criterios 2.2.2, 2.3.1 y 2.3.3.
