WITH compras AS (
 SELECT cl.cliente_id, cl.nombre,
 SUM(CASE WHEN substr(v.fecha,1,7)='2025-08' THEN v.unidades_netas ELSE 0 END) agosto,
 SUM(CASE WHEN substr(v.fecha,1,7)='2025-09' THEN v.unidades_netas ELSE 0 END) septiembre
 FROM ventas_analiticas v
 JOIN productos p USING(producto_id)
 JOIN clientes cl USING(cliente_id)
 WHERE p.nombre='Cajas archivo pack'
 AND v.fecha >= '2025-08-01' AND v.fecha < '2025-10-01'
 GROUP BY cl.cliente_id,cl.nombre
)
SELECT *, septiembre-agosto diferencia
FROM compras
WHERE agosto <> 0 OR septiembre <> 0
ORDER BY diferencia,cliente_id;
