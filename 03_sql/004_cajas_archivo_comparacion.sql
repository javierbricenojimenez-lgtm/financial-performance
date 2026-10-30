-- Promedios ponderados: importes netos / unidades netas.
SELECT substr(v.fecha,1,7) AS mes,
 SUM(v.unidades_netas) AS packs_netos,
 SUM(v.ingresos_netos) AS ingresos,
 SUM(v.costo_neto) AS costos,
 SUM(v.ingresos_netos-v.costo_neto) AS margen,
 1.0*SUM(v.ingresos_netos)/NULLIF(SUM(v.unidades_netas),0) AS ingreso_por_pack,
 1.0*SUM(v.costo_neto)/NULLIF(SUM(v.unidades_netas),0) AS costo_por_pack
FROM ventas_analiticas v
JOIN productos p USING(producto_id)
WHERE p.nombre='Cajas archivo pack'
 AND v.fecha >= '2025-08-01' AND v.fecha < '2025-10-01'
GROUP BY substr(v.fecha,1,7)
ORDER BY mes;
