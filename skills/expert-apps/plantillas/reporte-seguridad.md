# Reporte de seguridad: [nombre del proyecto]

> **Documento interno y confidencial.** Nunca se publica, nunca se sube al servidor y no se entrega completo al cliente: contiene detalles que facilitarían un ataque. Para el cliente se usa el resumen de la sección 9.

**Fecha de la auditoría:** [fecha] · **Versión auditada:** [commit] · **Nivel:** [Básico / Reforzado]

## 1. Resumen

**Veredicto:** [APTO PARA PUBLICAR / NO APTO: hay hallazgos críticos o altos abiertos]

| Gravedad | Encontrados | Corregidos | Aceptados | Abiertos |
|---|---|---|---|---|
| Crítica | | | | |
| Alta | | | | |
| Media | | | | |
| Baja | | | | |

[Tres a cinco líneas en lenguaje llano: qué tan sólido quedó, qué fue lo más importante que se encontró y qué decisión le toca al usuario.]

## 2. Alcance

- **Se auditó:** [código, entorno de pruebas, dirección].
- **Marco de referencia:** OWASP Top 10:2025 y los controles de la guía de seguridad del proyecto.
- **Quién auditó:** [experto / revisor independiente / ambos].

## 3. Verificaciones automáticas

Resultado literal de cada herramienta.

| Verificación | Herramienta | Resultado | Fecha |
|---|---|---|---|
| Secretos en código e historial | `buscar_secretos.py --historial` | [PASA / FALLA / No ejecutado] | |
| Dependencias con fallas conocidas | | | |
| Revisión externa del entorno de pruebas | `revisar_sitio.py` | | |
| Análisis estático | | | |
| Revisión externa de producción | `revisar_sitio.py` | [se llena tras publicar] | |

<details>
<summary>Salida completa de las herramientas</summary>

```
[pegar aquí]
```

</details>

## 4. Revisión manual por categoría

| Categoría | Qué se probó | Resultado |
|---|---|---|
| A01 Control de acceso | [por ejemplo: la cuenta A intentó leer y modificar datos de la cuenta B] | [Sin hallazgos / Ver H-1] |
| A02 Configuración | | |
| A03 Cadena de suministro | | |
| A04 Criptografía | | |
| A05 Inyección | | |
| A06 Diseño y lógica del negocio | | |
| A07 Autenticación | | |
| A08 Integridad | | |
| A09 Registro y alertas | | |
| A10 Manejo de errores | | |
| Archivos subidos | | |
| Pagos | | |

## 5. Hallazgos

### H-1 · [título] · Gravedad: [Crítica / Alta / Media / Baja]

- **Qué es:** [...]
- **Dónde:** [archivo y línea, o dirección]
- **Cómo se comprobó:** [pasos]
- **Qué daño permite:** [...]
- **Corrección aplicada:** [...]
- **Nueva prueba:** [fecha y resultado]
- **Estado:** [Corregido / Aceptado por el usuario el (fecha), con corrección prevista para (fecha) / Abierto]

## 6. Controles aplicados

[Lista breve de lo que quedó protegido: cabeceras, sesiones, validación, permisos, respaldos, verificación en dos pasos en las cuentas.]

## 7. Lo que no se probó

Tan importante como lo anterior.

- [qué]: [por qué no, y qué riesgo deja]

## 8. Riesgos que permanecen y recomendaciones

| Riesgo | Recomendación | Responsable | Fecha |
|---|---|---|---|
| | | | |

**¿Conviene una prueba de penetración profesional?** [Sí o no, y por qué.]

## 9. Resumen para el cliente

> Esta sección sí se puede entregar. Sin detalles técnicos explotables. En el idioma del cliente.

Se revisó la seguridad de [el sitio / la aplicación] el [fecha], siguiendo el estándar internacional OWASP.

- **Se verificó:** [lista en lenguaje llano].
- **Resultado:** se encontraron [número] puntos a corregir; [número] quedaron corregidos antes de publicar.
- **Pendiente:** [lo que quede, con fecha].
- **Para mantenerlo seguro:** [actualizaciones, respaldos, verificación en dos pasos].

Ningún sistema conectado a internet es 100 % seguro. Este reporte describe lo que se revisó y cómo quedó en la fecha indicada.
