# Reglas de negocio y validación

> Registro de diseño. La tabla conserva las tareas planificadas originalmente. Los controles ejecutados están documentados en outputs/manifiesto_validacion.json y outputs/AUDITORIA_CONSISTENCIA.md. Las devoluciones parciales siguen fuera del caso generado.

## Cálculos

- Signo de venta: +1; devolución: −1.
- Ingresos netos = suma(signo × ingreso_neto_importe).
- Costo de ventas = suma(signo × costo_ventas_importe).
- Gastos operacionales = suma(importe de GASTO) − suma(importe de REVERSO).
- Margen bruto = ingresos netos − costo de ventas.
- Utilidad operacional = margen bruto − gastos operacionales.
- Margen porcentual = resultado / ingresos netos. Si los ingresos son cero, devolver nulo, no cero.
- Desviación absoluta = real − presupuesto. Un valor positivo en costos o gastos es desfavorable; en ingresos o utilidad es favorable, evaluado dentro del contexto.
- Desviación relativa = (real − presupuesto) / presupuesto. Con presupuesto cero, devolver nulo y mostrar la desviación absoluta.

## Controles al cargar

| Control | Criterio de aceptación | Implementación |
|---|---|---|
| Identificadores y claves | Sin duplicados ni referencias inexistentes | PK, UNIQUE, FK |
| Campos obligatorios | Sin nulos ni nombres vacíos | NOT NULL y CHECK |
| Calendario | 273 fechas válidas, continuas y atributos coherentes | Validación de carga pendiente |
| Importes y cantidades | Magnitudes dentro de límites definidos | CHECK |
| Devolución | Original de tipo VENTA; misma identidad de producto, cliente y canal; fecha igual o posterior | Validación de carga pendiente |
| Cantidad devuelta | Total acumulado no supera la cantidad original | Validación de carga pendiente |
| Valor devuelto | Reversión proporcional del precio neto y costo original | Validación de carga pendiente |
| Redondeo de devolución | Pesos enteros; última devolución completa ajusta el residuo, sin superar el total original | Validación de carga pendiente |
| Documento | Todas sus líneas comparten fecha, cliente, canal y tipo | Validación de carga pendiente |
| Catálogos | Categorías, segmentos, cuentas y centros pertenecen al catálogo documentado | Validación de carga pendiente |
| Presupuesto | Una fila por combinación; cobertura de combinaciones esperadas | PK y validación de carga pendiente |
| Conciliación | Totales de agosto y septiembre coinciden exactamente con README | Validación de carga pendiente |
| Reproducibilidad | Misma semilla y configuración producen idénticos datos | Verificación del generador pendiente |

Las restricciones del esquema no sustituyen los controles entre filas. No se considerará validada la base hasta implementar y ejecutar ambos tipos de controles. Se activarán las claves externas en cada conexión SQLite.

## Interpretación

El puente contable inicial es +8 millones de ingresos −10 millones de costos −1 millón de gastos = −3 millones de utilidad. Todavía no es una explicación causal.

El análisis posterior definirá una descomposición consistente de precio, volumen, mezcla y costo. Devoluciones y gastos tendrán tratamiento explícito. Los desgloses por canal y cliente localizarán efectos; no se sumarán nuevamente al puente.

Los datos son sintéticos. Las causas introducidas por el generador quedarán registradas para evaluar si el análisis las recupera. Los escenarios representan estimaciones y no mejoras obtenidas en una empresa real.
