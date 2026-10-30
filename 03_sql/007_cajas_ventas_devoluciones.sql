SELECT substr(fecha,1,7) AS mes,
 SUM(CASE WHEN tipo_operacion='VENTA' THEN cantidad ELSE 0 END) AS packs_brutos,
 SUM(CASE WHEN tipo_operacion='DEVOLUCION' THEN cantidad ELSE 0 END) AS packs_devueltos,
 SUM(unidades_netas) AS packs_netos
FROM ventas_analiticas
WHERE producto_id=17 AND fecha >= '2025-08-01' AND fecha < '2025-10-01'
GROUP BY substr(fecha,1,7)
ORDER BY mes;
