# Datos sintéticos: generación y validación

**Caso ficticio, no evidencia de una empresa real.**

Semilla: 20251029. Período: enero a septiembre de 2025. Importes en CLP sin IVA.

## Contenido

| Tabla | Filas |
|---|---:|
| productos | 30 |
| clientes | 100 |
| calendario | 273 |
| ventas | 9,870 |
| gastos | 486 |
| presupuesto_comercial | 540 |
| presupuesto_gastos | 162 |

## Estado de resultados (millones de CLP)

| Mes | Ingresos | Costos | Gastos | Utilidad operacional |
|---|---:|---:|---:|---:|
| 2025-01 | 78.00 | 45.24 | 18.00 | 14.76 |
| 2025-02 | 74.00 | 42.92 | 18.00 | 13.08 |
| 2025-03 | 98.00 | 56.84 | 19.00 | 22.16 |
| 2025-04 | 88.00 | 51.92 | 18.50 | 17.58 |
| 2025-05 | 92.00 | 54.28 | 19.00 | 18.72 |
| 2025-06 | 90.00 | 54.00 | 19.50 | 16.50 |
| 2025-07 | 95.00 | 57.00 | 19.50 | 18.50 |
| 2025-08 | 100.00 | 60.00 | 20.00 | 20.00 |
| 2025-09 | 108.00 | 70.00 | 21.00 | 17.00 |

## Controles

- OK: Integridad SQLite.
- OK: Claves externas.
- OK: Calendario completo y coherente.
- OK: Devoluciones con referencia, identidad y valor correctos.
- OK: Sin devoluciones acumuladas excesivas.
- OK: Documentos consistentes.
- OK: Catálogos y cobertura.
- OK: Conciliación exacta de nueve meses.
- OK: Recálculo independiente Python frente a SQL.
- OK: Todos los productos y clientes con actividad.
- OK: Sin costos superiores al ingreso en líneas de venta.
- OK: Reproducibilidad con semilla fija.

## Cómo se construyó el caso

Las ventas se distribuyen en días hábiles sin ajustar feriados. Los clientes medianos compran más unidades y usan con mayor frecuencia el canal directo. Se utilizan 30 productos en cinco categorías, precios distintos, descuentos y costos por categoría.

Septiembre tiene mayor peso de tecnología e impresión, descuentos adicionales en venta directa, mayor costo relativo de impresión y más devoluciones. Logística y marketing tienen mayor peso en gastos. Son señales introducidas deliberadamente para practicar análisis; no son hallazgos descubiertos.

Los importes se calibran mensualmente a los estados de resultados del caso: ingresos y costos se escalan por separado sobre las ventas no devueltas y se distribuyen con restos mayores para cuadrar exactamente al peso. El precio de lista y descuento se reconstruyen desde el ingreso asignado. Esto modifica los precios y costos observados entre meses: cualquier descomposición posterior debe considerar la calibración, no atribuir toda la variación a las señales iniciales. Los factores se publican en el manifiesto.

El presupuesto se genera con parámetros planificados independientes, sin copiar el real. Todas las devoluciones son completas, una por venta seleccionada y dentro del mismo mes. Cada documento tiene una línea: es una simplificación. No se simulan devoluciones parciales, gastos reversados, compras, stock ni proveedores. La región corresponde al domicilio del cliente; no es una sucursal.

La fuente inicial está limpia para construir primero un diagnóstico financiero confiable. Más adelante podrá crearse una copia separada con errores deliberados para practicar limpieza, conservando esta referencia.

## Uso

Abrir financial_performance.sqlite con un explorador SQLite. Consultar ventas_analiticas para importes con signo y estado_resultados_mensual para la conciliación. Las tablas originales guardan importes positivos; no sumar devoluciones como ingresos.

Para regenerar, ejecutar 04_python/generar_datos.py con Python 3.11 o posterior y SQLite 3.37 o posterior. Solo utiliza la biblioteca estándar. La regeneración reemplaza exclusivamente los archivos generados por este script; no editar la base generada como fuente maestra.

SHA-256 de la fuente JSON: `1faf5c2403cd33ad3882d7dbbd46f7c7678ecf440f7013d9a34e91608f232162`.

Este documento describe la generación de datos, no el estado del proyecto completo. Los escenarios y recomendaciones se consultan en INFORME_FINAL.md. Los datos no demuestran una mejora económica real.
