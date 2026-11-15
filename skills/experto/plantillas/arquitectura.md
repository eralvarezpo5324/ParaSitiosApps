# Arquitectura: [nombre del proyecto]

> Documento interno. Nunca se publica ni se sube al servidor.
> Cada decisión lleva su porqué en una línea.

## 1. Resumen en lenguaje llano

[Tres o cuatro líneas que el usuario pueda repetir a su cliente: qué se usará, dónde vivirá, cuánto cuesta al mes y qué queda a su cargo.]

## 2. Hosting

| Dato | Valor |
|---|---|
| Tipo y proveedor | |
| Versión de PHP / soporte de Node | |
| Acceso por SSH | |
| Base de datos | |
| Tareas programadas | |
| Certificado SSL | |
| Método de publicación | |
| Límites conocidos | |

## 3. Decisiones de tecnología

| Qué | Elección y versión | Por qué | Alternativa descartada |
|---|---|---|---|
| Generación de páginas | | | |
| Lógica de servidor | | | |
| Base de datos | | | |
| Cuentas e inicio de sesión | | | |
| Correo | | | |
| Pagos | | | |
| Analítica | | | |

**Versiones verificadas contra la documentación oficial el:** [fecha]

## 4. Modelo de datos

| Entidad | Campos principales | Dueño del registro | Clasificación |
|---|---|---|---|
| | | | [Público / Interno / Personal / Sensible] |

## 5. Inventario de datos personales

| Dato | Para qué | Dónde se guarda | Quién accede | Cuánto tiempo | Proveedor que interviene |
|---|---|---|---|---|---|
| | | | | | |

## 6. Quién puede hacer qué

| Acción | Anónimo | Usuario | Administrador |
|---|---|---|---|
| | | | |

## 7. Modelo de amenazas

**Nivel de seguridad:** [Básico / Reforzado]. **Motivo:** [...]

| Amenaza o caso de abuso | Impacto | Control que la evita | Cómo se probará |
|---|---|---|---|
| | [Alto / Medio / Bajo] | | |

## 8. Entornos

| Entorno | Dirección | Visible a buscadores | Protección |
|---|---|---|---|
| Pruebas | | No | Contraseña |
| Producción | | Sí | |

## 9. Estructura del repositorio

```
[árbol de carpetas]
```

**Carpeta que se publica:** [ruta]. Todo lo demás se queda fuera del servidor público.

## 10. Plan por hitos

| Hito | Qué entrega, de punta a punta | Riesgo principal |
|---|---|---|
| 0 | Esqueleto publicado en el hosting real con HTTPS | El hosting no soporta lo previsto |
| 1 | | |

## 11. Costos recurrentes

| Concepto | Importe aproximado | Quién lo paga |
|---|---|---|
| | | |

## 12. Riesgos aceptados

- [riesgo]: [por qué se acepta y quién lo aprobó]
