# Auditoría de consistencia financiera

## Resultado

El recálculo independiente desde las tablas originales de SQLite coincide con los resultados financieros, el presupuesto, el detalle por producto y cliente, los escenarios, los datos embebidos del dashboard y las siete tablas numéricas nativas de la presentación. También se contrastaron las tablas de las diez notas intermedias.

Se verificaron las 9870 líneas de venta y devolución y sus importes generados. Los márgenes e identidades financieras se calculan sin redondear y los importes finales se presentan en pesos. Los gráficos y resúmenes pueden mostrar millones o porcentajes redondeados, con unidad explícita.

## Conciliaciones clave

| Comprobación | Resultado respaldado por la base |
|---|---|
| Ingresos agosto / septiembre | $100000000 / $108000000 |
| Margen bruto agosto / septiembre | $40000000 / $38000000 |
| Gastos agosto / septiembre | $20000000 / $21000000 |
| Utilidad operacional agosto / septiembre | $20000000 / $17000000 |
| Cambio de utilidad | -$3000000, conciliado exactamente |
| Utilidad septiembre presupuestada / real | $22730000 / $17000000 |
| Desviación de utilidad frente al plan | -$5730000 |
| Packs netos agosto / septiembre | 487 / 293 |
| Menor venta bruta / mayores devoluciones | 152 / 42 packs |
| Cambio de margen de Cajas archivo pack | -$1174888 |
| Margen de packs septiembre: plan / real | $1625334 / $977809 |
| Desviación de margen del producto | -$647525 |
| Clientes con reducción de packs y otras compras | 29 |
| Mejora neta de escenario prudente / base | $628767 / $1207535 por mes simulado |

## Correcciones realizadas

- Una nota intermedia mostraba 52,13% para el margen combinado de Papel, Escritura y Organización en septiembre. El cociente exacto es 52,1377355...%, que redondea a **52,14%**. Se corrigió.
- Se aclaró que los 340 packs de reducciones de determinados clientes son caídas de compra neta antes de compensaciones de otros clientes. No son la caída de ventas brutas del producto, que es 152 packs.
- Las notas de trabajo se identifican como documentos históricos. Sus frases de «siguiente paso» describen el momento de elaboración, no el estado actual de la entrega final.

## Trazabilidad

Fuente de verdad: tablas ventas, gastos, productos, clientes, presupuesto_comercial y presupuesto_gastos de financial_performance.sqlite. El auditor calcula desde las tablas base y no utiliza las vistas para reconstruir los importes.

Auditor reproducible: 04_python/auditar_consistencia.py. Evidencia detallada: AUDITORIA_CONSISTENCIA.json. La huella de la base se registra en esa evidencia. La comprobación incluye las cifras de las tablas de PowerPoint extraídas directamente del archivo, no solo de su imagen.

## Interpretación y límites

Real del caso, presupuesto y escenario son referencias diferentes, identificadas en los entregables. No existe presupuesto por cliente. El cumplimiento de unidades no garantiza cumplimiento de margen. Una reducción de compra de un producto no prueba pérdida del cliente. Las devoluciones ya están descontadas y no se agregan dos veces a los efectos financieros.

Los escenarios se recomputan desde bases financieras y supuestos explícitos, pero no constituyen resultados observados. La auditoría confirma consistencia con la base entregada, no la validez de motivos comerciales que esa base no contiene ni una garantía sobre escenarios futuros. La revisión de seguridad es una comprobación separada.
