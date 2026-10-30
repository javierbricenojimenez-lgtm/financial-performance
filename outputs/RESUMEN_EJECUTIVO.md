# Resumen ejecutivo

## Pregunta de negocio

¿Por qué la empresa vendió más en septiembre de 2025, pero terminó con una utilidad operacional menor que en agosto?

## Qué encontramos

Entre agosto y septiembre, los ingresos subieron de $100.000.000 a $108.000.000 (+8%), pero el costo de ventas aumentó de $60.000.000 a $70.000.000. Por eso el margen bruto bajó de $40.000.000 a $38.000.000. Además, los gastos operacionales subieron de $20.000.000 a $21.000.000. El resultado fue una caída de la utilidad operacional de $20.000.000 a $17.000.000 (-$3.000.000).

El análisis por categoría ubicó la mayor pérdida en Organización (-$4.490.921), seguida de Escritura (-$2.794.693) y Papel y cuadernos (-$1.841.093). Tecnología (+$5.317.149) e Insumos de impresión (+$1.809.558) compensaron parte de la caída, pero no alcanzaron para recuperar todo el margen perdido.

Dentro de Organización, el producto con mayor impacto fue Cajas archivo pack: su margen bajó de $2.152.697 a $977.809, una diferencia de -$1.174.888. Las unidades netas pasaron de 487 a 293. Esa reducción se explica por 152 packs menos vendidos en bruto y 42 packs adicionales devueltos.

La comparación por cliente mostró que 29 clientes redujeron o dejaron de comprar este producto, pero siguieron comprando otros productos en septiembre. Por lo tanto, la base permite demostrar dónde cayó el margen y cuánto impactó cada cambio, pero no permite afirmar que la causa haya sido falta de stock, pérdida del cliente o cambio de proveedor. Para eso se necesitan pedidos no atendidos, inventario, motivos de devolución o información del equipo comercial.

Frente al presupuesto de septiembre, la utilidad real fue de $17.000.000 frente a $22.730.000 planificados: una desviación desfavorable de -$5.730.000. En Cajas archivo pack se superó la meta de unidades (293 frente a 257), pero el margen quedó bajo el plan ($977.809 frente a $1.625.334). Esto demuestra que vender más unidades no garantiza cumplir la meta de rentabilidad.

## Conclusión

El problema no fue la falta de ventas totales. La empresa vendió más, pero el crecimiento se produjo con una estructura menos rentable: aumentó el costo de ventas, se deterioró el margen de categorías importantes y subieron los gastos operacionales. La investigación de Cajas archivo pack confirma un caso concreto de pérdida de margen por menor venta bruta y mayor devolución, aunque el motivo comercial final no está demostrado con la información disponible.

La conclusión profesional es separar tres niveles: los datos prueban qué cambió, el análisis cuantifica cuánto impactó y la validación comercial debe explicar por qué ocurrió. No se deben presentar hipótesis como causas confirmadas.

## Recomendaciones

1. Ejecutar un piloto de recompra para los productos prioritarios con clientes activos que redujeron unidades y medir unidades netas y margen.
2. Revisar los descuentos del canal directo mediante un piloto controlado, midiendo margen y respuesta de demanda.
3. Revisar los aumentos de Logística y Marketing y registrar el motivo de cada devolución.

Como referencia, los escenarios simulados estiman una mejora mensual de $628.767 en un escenario prudente y $1.207.535 en un escenario base. Son estimaciones para apoyar la decisión, no resultados ya implementados.

## Método y herramientas

Se utilizó SQL sobre SQLite para comparar meses, categorías, productos, clientes y presupuesto. Python automatizó la generación de datos, las validaciones, la conciliación financiera y los escenarios. El dashboard HTML y la presentación ejecutiva comunican los resultados.

## Límite del caso

Los datos son sintéticos y reproducibles. El proyecto demuestra una metodología completa de análisis y resolución, pero las causas comerciales definitivas deben validarse con fuentes externas.

