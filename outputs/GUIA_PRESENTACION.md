# Guion de exposición — 8 a 10 minutos

## 1. Problema y decisión

«Investigué por qué una empresa aumentaba sus ingresos 8%, mientras su utilidad operacional caía 15%. Usé SQL y Python para rastrear el cambio desde el estado de resultados hasta productos y clientes, conciliar su impacto y evaluar acciones. Entregué un dashboard y una presentación para apoyar decisiones de gerencia».

Presentar el origen sintético de los datos como contexto metodológico, sin convertirlo en el mensaje central. El aporte es la investigación, su validación y la propuesta de decisión. No atribuir implementación ni ahorros obtenidos.

## Mensaje de portafolio

«Desarrollé un análisis de rentabilidad de principio a fin: modelé una base financiera, construí consultas SQL, automaticé validaciones con Python y descompuse una caída de $3 millones en utilidad operacional. Identifiqué diferencias entre crecimiento comercial y rentabilidad, contrasté el resultado con el presupuesto y diseñé escenarios con mejoras netas estimadas de $0,63 a $1,21 millones por mes. Comuniqué los resultados en un dashboard interactivo y una presentación ejecutiva. El caso utiliza datos sintéticos documentados».

Mostrar el estado de resultados. Aclarar unidades, período y datos ficticios. Utilidad operacional incluye depreciación y no es EBITDA.

## 2. Diagnóstico global

Explicar el puente +$8M de ingresos, -$10M por costo de ventas y -$1M por gastos: -$3M de utilidad. Mostrar que las categorías no se comportan igual: Organización pierde $4,49M de margen, pero Tecnología compensa $5,32M y otras categorías también cambian. No sumar esa localización otra vez como un efecto adicional.

## 3. Investigación de un producto

«Bajé de categoría a producto y después a cliente. Cajas archivo pack pierde $1,175M de margen. Sus unidades netas caen de 487 a 293: 152 menos de venta bruta y 42 adicionales devueltos. Los clientes con reducción siguen comprando otros productos. Eso no prueba pérdida del cliente ni explica su motivo».

Mostrar el historial enero-septiembre. Septiembre es el segundo mes con menor venta bruta y tiene la mayor tasa de devolución. Agosto tiene la mayor venta neta. No afirmar estacionalidad o anomalía estadística a partir de nueve meses.

## 4. Presupuesto

Empresa: utilidad de septiembre $17M frente a $22,73M previstos, desviación desfavorable de $5,73M. Las ventas superan el plan $2M, pero el costo de ventas supera el plan $6,93M y los gastos $0,8M.

Producto: 293 packs frente a 257 planificados, pero margen $977809 frente a $1625334. Cumplir volumen no garantiza cumplir rentabilidad. Los clientes no tienen presupuesto individual en la fuente.

## 5. Propuestas y escenarios

Piloto de recompra en productos prioritarios, revisión controlada de descuentos directos y revisión de incrementos de Logística/Marketing. Mostrar escenario prudente y base: mejoras netas aproximadas de $0,629M y $1,208M por mes equivalente a septiembre. Incluyen costos de ejecución supuestos, no garantizan recuperar los $3M y no se han implementado.

## 6. Método y límites

SQL para agregar, Python para descomponer y conciliar, dashboard local para explorar y presentación para comunicar. Datos calibrados: los cambios de precios/costos incluyen efectos del generador. La descomposición es contable y depende del método. No afirmar que prueba descuentos comerciales reales, negociación con proveedores o fallas de stock.

## Preguntas de entrevista

- ¿Por qué netos? Para descontar devoluciones una sola vez de cantidades, ingresos y costos.
- ¿Cómo validaste? Claves, calendario, devoluciones, reproducción por semilla, recálculo independiente Python/SQL y puente exacto.
- ¿Por qué no presupuesto por cliente? Porque no existe esa granularidad en la fuente; asignarlo sin regla sería inventar metas.
- ¿Qué falta para explicar motivos? CRM, pedidos no atendidos, disponibilidad de stock y causas registradas de devolución.
- ¿Qué significa mejora? Es un escenario sujeto a supuestos y riesgos, no un resultado logrado en una empresa.
- ¿Hay Power BI? Esta entrega tiene un dashboard HTML local. No se presenta como un PBIX.

## Orden de revisión

Abrir primero INFORME_FINAL.md, luego dashboard.html y finalmente presentacion_ejecutiva.pptx. La base SQLite y el anexo permiten auditar los resultados. Publicar en GitHub en una etapa posterior, tras revisar título, descripción y archivos finales.
