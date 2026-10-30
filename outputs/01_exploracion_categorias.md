# Exploración 01: margen bruto por categoría

> Nota de versión: documento intermedio conservado para trazabilidad. Los pasos pendientes reflejan su fecha de elaboración. El estado actual está en INFORME_FINAL.md y AUDITORIA_CONSISTENCIA.md.

Fuente: base local sintética financial_performance.sqlite, vista ventas_analiticas y tabla productos. Agosto y septiembre de 2025; importes netos de devoluciones, sin IVA. Consulta reproducible: 03_sql/002_margen_por_categoria.sql.

| Categoría | Margen agosto CLP | Margen septiembre CLP | Variación CLP |
|---|---:|---:|---:|
| Organización | 8531993 | 4041072 | -4490921 |
| Escritura | 6261287 | 3466594 | -2794693 |
| Papel y cuadernos | 5170040 | 3328947 | -1841093 |
| Insumos de impresión | 12849533 | 14659091 | 1809558 |
| Tecnología | 7187147 | 12504296 | 5317149 |
| Total | 40000000 | 38000000 | -2000000 |

Las tres primeras categorías pierden $9.126.707 de margen, compensados por $7.126.707 adicionales de tecnología e impresión. Las variaciones concilian exactamente con la caída de $2.000.000 del margen bruto total.

Tecnología e impresión juntas pasan de $61.484.368 de ingresos sobre $100.000.000 (61,48%) a $87.215.413 sobre $108.000.000 (80,75%). Su margen porcentual combinado pasa de 32,59% a 31,15%, mientras las otras categorías combinadas pasan de 51,83% a 52,14%.

Observación: las ventas se desplazan hacia categorías con menor margen porcentual. La reducción de margen absoluto se concentra en organización, escritura y papel. Esto es compatible con un efecto mezcla desfavorable; todavía no cuantifica por separado precio, volumen, mezcla de productos, descuentos y costo unitario.

Siguiente tarea: descomponer los cambios dentro de las categorías por producto, evitando sumar unidades heterogéneas. Revisar precios efectivos y costos unitarios comparables. Los factores de calibración del generador deben considerarse al interpretar causas.

Los datos son ficticios y fueron diseñados con patrones para aprendizaje. No representan evidencia de una empresa real.
