-- Exploración: cifras netas de devoluciones, CLP sin IVA.
SELECT p.categoria,
       substr(v.fecha, 1, 7) AS mes,
       SUM(v.ingresos_netos) AS ingresos,
       SUM(v.costo_neto) AS costo_ventas,
       SUM(v.ingresos_netos - v.costo_neto) AS margen_bruto,
       100.0 * SUM(v.ingresos_netos - v.costo_neto)
           / NULLIF(SUM(v.ingresos_netos), 0) AS margen_bruto_pct
FROM ventas_analiticas AS v
JOIN productos AS p USING (producto_id)
WHERE v.fecha >= '2025-08-01' AND v.fecha < '2025-10-01'
GROUP BY p.categoria, substr(v.fecha, 1, 7)
ORDER BY p.categoria, mes;
