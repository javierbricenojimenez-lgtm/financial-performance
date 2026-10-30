# Empresa Ficticia 017: comportamiento observado

> Nota de versión: documento intermedio conservado para trazabilidad. Los pasos pendientes reflejan su fecha de elaboración. El estado actual está en INFORME_FINAL.md y AUDITORIA_CONSISTENCIA.md.

Fuente: base sintética local; consulta 03_sql/006_cliente_017_historial.sql. Enero a septiembre de 2025, CLP sin IVA.

| Mes | Documentos de venta, todos los productos | Ingresos netos, todos los productos | Cajas archivo pack, packs netos |
|---|---:|---:|---:|
| Enero | 15 | 1774330 | 0 |
| Febrero | 17 | 2079445 | 8 |
| Marzo | 22 | 3528162 | 0 |
| Abril | 20 | 1582687 | 17 |
| Mayo | 16 | 1715327 | 27 |
| Junio | 19 | 1981001 | 26 |
| Julio | 27 | 3065653 | 39 |
| Agosto | 16 | 2752156 | 50 |
| Septiembre | 25 | 2364373 | 0 |

Comprobaciones: el cliente siguió comprando en septiembre (25 documentos de venta). Tiene actividad en las cinco categorías. En Organización registra cuatro documentos de venta e ingresos netos de $198595 en septiembre, frente a $581540 en agosto. Para Cajas archivo pack no existen ventas ni devoluciones en septiembre: el cero no procede de cancelaciones.

Interpretación: no hay abandono total observado en septiembre; hay ausencia de compra de este producto. En enero y marzo tampoco compró este producto, así que su historial no implica recompra mensual garantizada. Agosto muestra la mayor cantidad mensual del producto para este cliente dentro del período. No basta para afirmar sobrecompra, inventario acumulado, sustitución o falta de stock.

Límite: no hay CRM, inventarios, pedidos no atendidos ni motivos de no compra. El conjunto sintético fue generado con variabilidad aleatoria y cambio de mezcla; no contiene una causa comercial documentada para este cliente. No fabricar una explicación causal a partir del patrón.

Siguiente paso posible: revisar el historial de los otros 23 clientes con compra neta cero en septiembre para determinar si el patrón es generalizado. Para probar motivos comerciales serían necesarias fuentes adicionales, que en este caso solo podrían incorporarse como supuestos sintéticos explícitos.
