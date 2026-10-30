# Financial Performance Intelligence

**Diagnóstico de rentabilidad, control presupuestario y escenarios de decisión.**

## Enfoque y herramientas

El proyecto transforma una pregunta de gerencia en un análisis reproducible: definir hipótesis, validar datos, localizar cambios por categoría, producto y cliente, cuantificar efectos y proponer acciones. SQL agrega la evidencia financiera; Python automatiza controles y descomposición; un dashboard interactivo y una presentación ejecutiva comunican los resultados.

## Decisión y resultado

Los ingresos suben de $100M a $108M, pero la utilidad operacional baja de $20M a $17M. El costo de ventas sube $10M y los gastos $1M. El margen bruto disminuye $2M. La utilidad operacional es posterior a depreciación y no equivale a EBITDA.

## Descomposición de la caída

| Factor | Efecto CLP aproximado |
|---|---|
| Volumen valorado a precios base | $17.008.740 |
| Mezcla de productos | $-5.566.679 |
| Precio de lista medio | $-33.605.285 |
| Descuento medio por unidad | $-916.565 |
| Costo unitario | $21.079.789 |
| Gastos operacionales | $-1.000.000 |

La suma sin redondear es exactamente -$3.000.000. El anexo define el orden y las fórmulas. Las cifras unitarias también reflejan calibración del generador.

## Categorías

| Categoría | Margen agosto | Margen septiembre | Cambio |
|---|---|---|---|
| Organización | $8.531.993 | $4.041.072 | $-4.490.921 |
| Escritura | $6.261.287 | $3.466.594 | $-2.794.693 |
| Papel y cuadernos | $5.170.040 | $3.328.947 | $-1.841.093 |
| Insumos de impresión | $12.849.533 | $14.659.091 | $1.809.558 |
| Tecnología | $7.187.147 | $12.504.296 | $5.317.149 |

Organización, Escritura y Papel pierden margen absoluto. Tecnología e Impresión compensan parte de esa caída. La venta se desplaza hacia categorías con menor margen porcentual. Esto concilia la localización del cambio, sin sumar los cambios por categoría otra vez al puente.

## Productos prioritarios: 81.3% de contribuciones negativas

| Producto | Cambio de margen |
|---|---|
| Cajas archivo pack | $-1.174.888 |
| Archivadores pack | $-990.853 |
| Marcadores caja | $-964.283 |
| Carpetas pack | $-841.162 |
| Organizador | $-634.856 |
| Resma oficio | $-551.962 |
| Papel fotográfico | $-542.682 |
| Plumones caja | $-521.601 |
| Bandeja escritorio | $-490.044 |
| Correctores caja | $-453.380 |
| Destacadores caja | $-379.284 |
| Otros productos con contribución negativa | $-1.739.541 |
| Compensaciones de productos con mayor margen | $7.284.536 |

## Gastos operacionales

| Cuenta | Agosto | Septiembre | Aumento / disminución |
|---|---|---|---|
| Logística | $2.800.000 | $3.673.300 | $873.300 |
| Marketing | $1.800.000 | $2.361.407 | $561.407 |
| Depreciación | $1.000.000 | $971.772 | $-28.228 |
| Servicios | $1.800.000 | $1.749.189 | $-50.811 |
| Arriendo | $3.000.000 | $2.915.317 | $-84.683 |
| Remuneraciones | $9.600.000 | $9.329.015 | $-270.985 |

## Presupuesto frente a real

### 2025-08

| Indicador | Plan | Real | Real − plan |
|---|---|---|---|
| ingresos | $102.000.000 | $100.000.000 | $-2.000.000 |
| costos | $60.690.000 | $60.000.000 | $-690.000 |
| gastos | $19.800.000 | $20.000.000 | $200.000 |
| utilidad | $21.510.000 | $20.000.000 | $-1.510.000 |

### 2025-09

| Indicador | Plan | Real | Real − plan |
|---|---|---|---|
| ingresos | $106.000.000 | $108.000.000 | $2.000.000 |
| costos | $63.070.000 | $70.000.000 | $6.930.000 |
| gastos | $20.200.000 | $21.000.000 | $800.000 |
| utilidad | $22.730.000 | $17.000.000 | $-5.730.000 |

## Cajas archivo pack frente a presupuesto: enero a septiembre

| Mes | Packs reales / plan | Margen real | Margen plan | Desviación de margen |
|---|---|---|---|---|
| 2025-01 | 234 / 194 | $1.064.207 | $1.226.666 | $-162.459 |
| 2025-02 | 430 / 184 | $1.848.230 | $1.165.334 | $682.896 |
| 2025-03 | 408 / 232 | $1.843.961 | $1.472.000 | $371.961 |
| 2025-04 | 460 / 218 | $2.116.732 | $1.380.000 | $736.732 |
| 2025-05 | 463 / 228 | $1.942.880 | $1.441.334 | $501.546 |
| 2025-06 | 459 / 225 | $2.017.282 | $1.426.000 | $591.282 |
| 2025-07 | 456 / 235 | $2.173.870 | $1.487.334 | $686.536 |
| 2025-08 | 487 / 246 | $2.152.697 | $1.564.000 | $588.697 |
| 2025-09 | 293 / 257 | $977.809 | $1.625.334 | $-647.525 |

El producto supera en septiembre el plan de unidades netas (293 frente a 257), pero queda bajo el margen planificado. La caída mensual frente a agosto y la desviación frente al presupuesto responden a referencias distintas: no confundirlas. El presupuesto no existe por cliente, por lo que no se inventa una asignación de metas individuales.

### Comparación de Cajas archivo pack por canal

| Mes | Canal | Packs real / plan | Margen real | Margen plan |
|---|---|---|---|---|
| 2025-08 | DIRECTO | 288 / 160 | $1.259.574 | $1.016.600 |
| 2025-08 | ONLINE | 199 / 86 | $893.123 | $547.400 |
| 2025-09 | DIRECTO | 212 / 167 | $696.637 | $1.056.467 |
| 2025-09 | ONLINE | 81 / 90 | $281.172 | $568.867 |

### Clientes con mayor caída de margen de este producto

| Cliente ficticio | Packs agosto / septiembre | Margen agosto | Margen septiembre | Cambio |
|---|---|---|---|---|
| Empresa Ficticia 017 | 50 / 0 | $219.301 | $0 | $-219.301 |
| Empresa Ficticia 024 | 22 / 0 | $100.447 | $0 | $-100.447 |
| Empresa Ficticia 027 | 20 / 0 | $89.518 | $0 | $-89.518 |
| Empresa Ficticia 004 | 17 / 0 | $77.617 | $0 | $-77.617 |
| Empresa Ficticia 011 | 19 / 0 | $76.504 | $0 | $-76.504 |
| Empresa Ficticia 006 | 32 / 17 | $128.850 | $55.907 | $-72.943 |
| Empresa Ficticia 072 | 16 / 0 | $71.973 | $0 | $-71.973 |
| Empresa Ficticia 015 | 25 / 14 | $114.143 | $44.083 | $-70.060 |

La suma de cambios de todos los clientes concilia exactamente con -$1.174.888 del producto. Hay clientes que compensan parte de la caída; el detalle completo está en resultados_finales.json y en el dashboard.

## Investigación de Cajas archivo pack

Su margen cae $1.174.888. Las unidades netas bajan de 487 a 293: 152 packs menos de venta bruta y 42 packs adicionales devueltos. Los 29 clientes con reducción siguen comprando otros productos. Las tres devoluciones de septiembre revierten $145.397 de margen ya incluido en el neto. Septiembre tiene la segunda menor venta bruta de enero-septiembre y la mayor tasa de devolución (12,54%). El historial no demuestra normalidad estadística ni causas de no compra.

## Acciones propuestas

1. Comercial: piloto de recompra de productos prioritarios con clientes activos que redujeron unidades. Revisar necesidad y disponibilidad antes de ofrecer incentivos. Esfuerzo medio. Riesgo: recompra no recurrente o canibalización. Medir unidades netas y margen por producto, no solo facturación.

2. Comercial y Finanzas: revisar autorización de descuentos en canal directo. Esfuerzo medio. Riesgo: una reducción de descuentos puede afectar la demanda. Evaluar con piloto, margen unitario y retención. No confundir los efectos de calibración con una política comercial real.

3. Operaciones y Finanzas: revisar el incremento de Logística y Marketing y registrar causas de devoluciones. Esfuerzo bajo/medio. Riesgo: recortes que deterioren servicio o ventas. Aprobar ahorro después de identificar partidas evitables. La reducción de devoluciones no añade un beneficio independiente a estos escenarios.

## Escenarios de un mes equivalente a septiembre

| Escenario | Volumen | Descuentos | Gastos | Costo supuesto de ejecución | Mejora neta | Utilidad simulada |
|---|---|---|---|---|---|---|
| Prudente | $230.867 | $426.165 | $71.735 | $100.000 | $628.767 | $17.628.767 |
| Base | $461.734 | $852.330 | $143.471 | $250.000 | $1.207.535 | $18.207.535 |

Prudente/base recuperan 5%/10% de la brecha de unidades seleccionadas, reducen descuentos en 0,5/1 punto de lista directa y ahorran 5%/10% del incremento de Logística y Marketing. Se mantienen los demás factores. Todos son supuestos, no mejoras obtenidas. El anexo explica bases, interacción omitida y seguimiento.

## Entrega y límites

La versión analítica cierra con informe, anexo, dashboard local de tres vistas, resultados estructurados y consultas reproducibles. El dashboard es HTML autónomo, no un archivo Power BI. La implementación nativa en Power BI queda como adaptación tecnológica posterior. La presentación ejecutiva acompaña el informe. No se publica en GitHub durante esta entrega.

Nota metodológica: el caso utiliza datos sintéticos documentados. No contamos con evidencia externa para explicar motivos de no compra o devolución. El proyecto entrega un diagnóstico financiero verificado, hipótesis pendientes y propuestas de decisión. La fase de implementación y medición empresarial queda diseñada, no ejecutada.
