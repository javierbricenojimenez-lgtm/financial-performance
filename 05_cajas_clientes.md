# Cajas archivo pack: localización de la caída por cliente

> Nota de versión: documento intermedio conservado para trazabilidad. Los pasos pendientes reflejan su fecha de elaboración. El estado actual está en INFORME_FINAL.md y AUDITORIA_CONSISTENCIA.md.

Base sintética del proyecto. Comparación de packs netos de devoluciones, agosto y septiembre de 2025. Consulta: 03_sql/005_cajas_clientes.sql.

| Grupo | Clientes | Agosto | Septiembre | Cambio |
|---|---:|---:|---:|---:|
| Compra neta positiva en agosto, cero en septiembre | 24 | 295 | 0 | -295 |
| Compra neta positiva en ambos meses, menor en septiembre | 5 | 110 | 65 | -45 |
| Igual compra neta | 1 | 7 | 7 | 0 |
| Mayor compra neta, con compra en ambos meses | 3 | 75 | 100 | 25 |
| Compra neta cero en agosto, positiva en septiembre | 13 | 0 | 121 | 121 |
| Total | 46 | 487 | 293 | -194 |

Conciliación: -295 -45 +25 +121 = -194 packs, igual al cambio total del producto. Los clientes sin compra neta de este producto en septiembre concentran la mayor reducción bruta; las compras de otros clientes compensan parcialmente.

Mayores caídas individuales: Empresa Ficticia 017 (50 a 0), 024 (22 a 0), 027 (20 a 0), 011 (19 a 0). La primera representa 50 de los 194 packs de caída neta, sin implicar una causa comercial identificada.

Precauciones: cero compra neta no prueba ausencia de documentos, ni abandono del cliente, ni pérdida de la relación comercial. Tampoco un comprador de septiembre sin compra neta en agosto es necesariamente cliente nuevo. Revisar ventas brutas y devoluciones, actividad en otros productos e historial anterior antes de interpretar. Los datos no incluyen motivos de no compra, cotizaciones, stock ni CRM: el motivo real no puede probarse solo con este corte.

Siguiente paso: revisar el historial y otras compras de los clientes con mayor reducción, comenzando por Empresa Ficticia 017. Conservar como hipótesis posibles diferencias en frecuencia de compra, sustitución o falta de recompra; no afirmar causalidad.
