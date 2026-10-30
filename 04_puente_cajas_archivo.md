# Puente del margen: Cajas archivo pack

> Nota de versión: documento intermedio conservado para trazabilidad. Los pasos pendientes reflejan su fecha de elaboración. El estado actual está en INFORME_FINAL.md y AUDITORIA_CONSISTENCIA.md.

Datos sintéticos, CLP netos de devoluciones y sin IVA. Fuente: indicadores de 03_cajas_archivo_comparacion.md y consulta 03_sql/004_cajas_archivo_comparacion.sql.

Método secuencial volumen → ingreso unitario → costo unitario. Definir Q como packs netos, P como ingresos netos/Q y C como costos netos/Q. Subíndice 0: agosto; 1: septiembre. Usar cocientes sin redondear en los cálculos.

| Efecto | Fórmula | CLP redondeados |
|---|---|---:|
| Volumen | (Q1-Q0) × (P0-C0) | -857543 |
| Ingreso unitario | Q1 × (P1-P0) | -616829 |
| Costo unitario | -Q1 × (C1-C0) | 299484 |
| Total | Q1(P1-C1)-Q0(P0-C0) | -1174888 |

El volumen se evalúa al margen unitario de agosto; los cambios unitarios se evalúan con los packs de septiembre. La suma exacta fue verificada con aritmética racional en Python y coincide con la variación del margen bruto. Los importes redondeados también suman exactamente.

Interpretación: menos packs reducen el margen; menor ingreso por pack también lo reduce; menor costo por pack compensa parte de ambas pérdidas. El reparto depende del orden del método porque existen interacciones; no es una atribución causal única. Ingreso unitario no equivale a utilidad unitaria.

Pendiente: revisar precios de lista, descuentos y distribución por cliente/canal para explicar el cambio del ingreso unitario. El generador calibra ingresos y costos por mes: estas cifras explican matemáticamente el caso sintético y no prueban causas externas ni una mejora real.
