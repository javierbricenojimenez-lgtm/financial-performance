# Cajas archivo pack: enero a septiembre de 2025

> Nota de versión: documento intermedio conservado para trazabilidad. Los pasos pendientes reflejan su fecha de elaboración. El estado actual está en INFORME_FINAL.md y AUDITORIA_CONSISTENCIA.md.

Fuente: base sintética local, consulta 03_sql/008_cajas_historial_mensual.sql. Tasas sobre unidades vendidas antes de devoluciones. En este conjunto todas las devoluciones corresponden a ventas del mismo mes.

| Mes | Vendidos brutos | Devueltos | Netos | Tasa devolución |
|---|---:|---:|---:|---:|
| Enero | 251 | 17 | 234 | 6,77% |
| Febrero | 438 | 8 | 430 | 1,83% |
| Marzo | 417 | 9 | 408 | 2,16% |
| Abril | 460 | 0 | 460 | 0,00% |
| Mayo | 494 | 31 | 463 | 6,28% |
| Junio | 482 | 23 | 459 | 4,77% |
| Julio | 466 | 10 | 456 | 2,15% |
| Agosto | 487 | 0 | 487 | 0,00% |
| Septiembre | 335 | 42 | 293 | 12,54% |

Validación aritmética: en los nueve meses, vendidos menos devueltos coincide con netos. Agosto y septiembre concilian con los resultados anteriores.

Observaciones: septiembre tiene la segunda menor venta bruta y neta de los nueve meses, detrás de enero. Presenta la mayor cantidad y tasa de devolución del período. Agosto no tiene la mayor venta bruta (mayo tiene 494), pero sí la mayor venta neta, con cero devoluciones. Por ello comparar solo contra agosto combina una base neta alta con devoluciones excepcionalmente bajas dentro de esta muestra.

Promedio descriptivo enero-agosto: 436,875 packs brutos y 424,625 netos por mes. No constituye un valor esperado ajustado por días hábiles, estacionalidad o cartera. Nueve meses de un solo año no permiten asegurar normalidad estadística o estacionalidad. Las señales orientan la investigación, no prueban falta de stock ni defectos.

Siguiente paso propuesto: localizar clientes, documentos y fechas de los 42 packs devueltos en septiembre. Los motivos de devolución no existen en la base: deben quedar como información pendiente, sin inventar causas. Mantener en paralelo la caída de venta bruta, responsable de 152 de los 194 packs netos de reducción frente a agosto.
