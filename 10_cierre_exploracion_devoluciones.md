# Cierre de exploración: devoluciones de Cajas archivo pack

> Nota de versión: documento intermedio conservado para trazabilidad. Los pasos pendientes reflejan su fecha de elaboración. El estado actual está en INFORME_FINAL.md y AUDITORIA_CONSISTENCIA.md.

Caso sintético. Fuente: consulta 03_sql/009_cajas_devoluciones_septiembre.sql sobre la base local. CLP sin IVA.

| Cliente ficticio | Fecha devolución | Documento | Packs | Margen bruto revertido |
|---|---|---|---:|---:|
| 029 | 2025-09-10 | NC-09-00892 | 11 | 37714 |
| 019 | 2025-09-12 | NC-09-00543 | 26 | 89142 |
| 076 | 2025-09-29 | NC-09-00444 | 5 | 18541 |
| Total | | | 42 | 145397 |

Ingresos revertidos: $273051. Costos revertidos: $127654. Margen bruto revertido: $145397. Estos importes ya están incluidos en el neto de septiembre; no sumarlos nuevamente al puente de variación anterior. Los 42 packs concilian con el historial mensual.

Hallazgo: tres documentos de tres clientes explican todas las devoluciones del producto en septiembre. La base no contiene motivo ni información de calidad o stock. No atribuirlas a fallas de producto u operaciones sin evidencia.

Acción propuesta para un caso real: revisar los tres documentos con Comercial/Operaciones y solicitar motivo registrado, antes de proponer una corrección específica. En este proyecto se conserva como pendiente de evidencia, sin simular una causa descubierta.

Se cierra esta rama de exploración documental para avanzar al diagnóstico financiero completo según 00_gestion/alcance_cierre_v1.md. El detalle de pérdida por ingreso unitario y la descomposición global siguen pendientes.
