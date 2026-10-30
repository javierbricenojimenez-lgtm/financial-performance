# Financial Performance Intelligence

## ¿Por qué una empresa vende más, pero gana menos?

Análisis de rentabilidad y control de gestión con SQL y Python, desde el estado de resultados hasta los productos y clientes que explican el cambio.

### Problema

Los ingresos aumentaron 8%, pero la utilidad operacional cayó 15%. La decisión que apoya el proyecto es dónde concentrar la revisión comercial y de gastos para mejorar la rentabilidad.

### Cómo lo abordé

Definí preguntas e indicadores, diseñé una base relacional y automaticé controles de calidad. Construí consultas SQL para comparar meses, presupuesto, categorías, productos y clientes. Con Python separé los efectos financieros y comprobé que conciliaran con la caída de $3 millones. Convertí los hallazgos en recomendaciones y escenarios de decisión.

### Hallazgos que cambian la decisión

- El crecimiento de ingresos no se tradujo en mayor utilidad: el margen bruto cayó $2M y los gastos aumentaron $1M.
- Septiembre quedó $5,73M por debajo de la utilidad presupuestada, pese a superar el plan de ingresos.
- Cajas archivo pack superó su meta de unidades, pero quedó $647525 bajo su margen presupuestado.
- Los clientes con menor compra de este producto mantuvieron compras de otros productos. Esto permite enfocar la investigación sin concluir erróneamente que se perdió al cliente.

### Herramientas y entregables

**SQL y SQLite:** modelo relacional, consultas de diagnóstico y comparación presupuestaria.

**Python:** generación reproducible, validaciones, descomposición financiera y escenarios.

**Dashboard interactivo local:** exploración de rentabilidad, presupuesto y sensibilidad de escenarios.

**Informe y PowerPoint:** hallazgos, prioridades, riesgos y evidencia necesaria para decidir.

### Propuesta de solución

Piloto de recompra en productos prioritarios, revisión controlada de descuentos y revisión de incrementos de Logística y Marketing. Los escenarios estiman una mejora neta mensual de $0,63M a $1,21M, incorporando costos de ejecución supuestos. Se propone medir margen, compra neta y devoluciones durante el piloto.

### Aporte profesional

El proyecto demuestra cómo convertir una pregunta de gerencia en evidencia financiera verificable y una propuesta de acción. Incluye trazabilidad de cálculos, control de doble conteo, interpretación de límites y comunicación para quien debe decidir.

Nota metodológica: caso de portafolio con datos sintéticos documentados. Los escenarios son estimaciones, no ahorros implementados. El anexo explica la calibración de los datos y sus límites causales.
