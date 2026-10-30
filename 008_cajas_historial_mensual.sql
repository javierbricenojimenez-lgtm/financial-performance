-- Serie mensual del producto; unidades netas = ventas - devoluciones.
SELECT substr(v.fecha,1,7) AS mes,
 SUM(CASE WHEN tipo_operacion='VENTA' THEN cantidad ELSE 0 END) AS vendidos,
 SUM(CASE WHEN tipo_operacion='DEVOLUCION' THEN cantidad ELSE 0 END) AS devueltos,
 SUM(unidades_netas) AS netos,
 100.0*SUM(CASE WHEN tipo_operacion='DEVOLUCION' THEN cantidad ELSE 0 END)
 /NULLIF(SUM(CASE WHEN tipo_operacion='VENTA' THEN cantidad ELSE 0 END),0) AS tasa_devolucion
FROM ventas_analiticas v
JOIN productos p USING(producto_id)
WHERE p.nombre='Cajas archivo pack'
GROUP BY substr(v.fecha,1,7)
ORDER BY mes;
