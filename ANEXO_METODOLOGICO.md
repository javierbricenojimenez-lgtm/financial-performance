# Método, límites y reproducción

SQL agrega los importes con signo por producto y mes. Python verifica las identidades con fracciones exactas, sin redondeo intermedio. Las tablas de fuentes guardan magnitudes positivas; las vistas aplican el signo una sola vez.

## Puente financiero

Para cada producto: Q = unidades netas; P = ingreso neto / Q; C = costo neto / Q; L = importe de lista neto / Q; D = descuento neto / Q. P=L-D. Agosto es 0 y septiembre 1. Todos los productos tienen Q positiva en ambos meses.

Índice de cantidad V = sum(Q1*P0) / sum(Q0*P0). Es una cantidad valorada a precios base, no una suma física de packs y unidades.

- Volumen = (V-1)*margen0.
- Mezcla = sum((Q1-V*Q0)*(P0-C0)).
- Precio de lista medio = sum(Q1*(L1-L0)).
- Descuentos = -sum(Q1*(D1-D0)).
- Costo unitario = -sum(Q1*(C1-C0)).
- Gastos = -(gastos1-gastos0).

La suma concilia exactamente con la variación de utilidad. El reparto es secuencial, depende del orden y de las ponderaciones. Los importes unitarios son medias ponderadas netas y pueden reflejar composición por cliente/canal. Las devoluciones ya forman parte de Q y de los importes: no añadir sus efectos otra vez al puente.

## Fuente sintética y alcance causal

El generador cambia mezcla, descuentos y algunos costos, y calibra ingresos y costos mensuales por separado para reproducir los estados financieros del caso. Por tanto, los cambios de precios y costos observados también reflejan esa calibración. No atribuir toda reducción de precio a una promoción real, ni ahorro de costo a una negociación. No existen datos de stock, compras, CRM, causas de devolución ni competencia. Las consultas describen y descomponen resultados, no identifican causas comerciales externas.

## Presupuesto

Agregar el real y el plan por mes/producto/canal, o por mes/cuenta/centro, antes de unir. No duplicar plan al relacionarlo con líneas. La desviación es real menos plan. Ingreso y utilidad positivos son favorables en el contexto de este caso; costos y gastos positivos son desfavorables. El plan es sintético e independiente del real.

## Escenarios y seguimiento

1. Recuperación de 5%/10% de los packs/unidades netos perdidos, por producto con contribución negativa al margen. Valorar cada producto a su margen unitario de septiembre y después sumar pesos, sin sumar cantidades heterogéneas.
2. Reducción de descuentos equivalente a 0,5/1 punto porcentual del importe de lista neto del canal directo en septiembre, solo sobre ventas existentes. Mantener cantidades, costo y devoluciones. No aplicar el beneficio de descuento a unidades recuperadas: se omite la interacción para evitar duplicación.
3. Ahorro de 5%/10% del incremento positivo de Logística y Marketing. Mantener los otros gastos.

Restar un costo de ejecución supuesto de $100000/$250000 por mes en prudente/base. Son supuestos ilustrativos, no cotizaciones ni pronósticos validados. No se estima elasticidad. Los escenarios se evalúan como un mes equivalente a septiembre, no como acumulado anual. Validar viabilidad, costos y reacción de demanda antes de actuar.

Seguimiento propuesto: Finanzas concilia margen y utilidad mensualmente; Comercial revisa precio efectivo, descuento sobre lista, compra por producto y cohortes de clientes; Operaciones registra unidades devueltas, motivo y costo. Comparar con una base aprobada, controlar estacionalidad y usar un piloto para evaluar acciones. Ninguna acción se ha implementado en una empresa real.

## Reproducción

Python >=3.11 y SQLite >=3.37, sin dependencias externas para datos y análisis. Desde la raíz ejecutar `python 04_python/generar_datos.py` y después `python 04_python/cerrar_analisis.py`. Abrir outputs/dashboard.html localmente. El generador restablece la base original; no usar la base generada como fuente editable. Las presentaciones se actualizan aparte al cambiar resultados.
