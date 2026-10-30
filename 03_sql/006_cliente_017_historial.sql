-- Historial del cliente con mayor reducción de packs.
SELECT substr(fecha,1,7) AS mes,
 COUNT(DISTINCT CASE WHEN tipo_operacion='VENTA' THEN documento_id END) AS documentos_venta,
 SUM(ingresos_netos) AS ingresos_totales,
 SUM(CASE WHEN producto_id=17 AND tipo_operacion='VENTA' THEN cantidad ELSE 0 END) AS packs_vendidos,
 SUM(CASE WHEN producto_id=17 AND tipo_operacion='DEVOLUCION' THEN cantidad ELSE 0 END) AS packs_devueltos,
 SUM(CASE WHEN producto_id=17 THEN unidades_netas ELSE 0 END) AS packs_netos
FROM ventas_analiticas
WHERE cliente_id=17
GROUP BY substr(fecha,1,7)
ORDER BY mes;

-- Actividad por categoría en los meses comparados.
SELECT substr(v.fecha,1,7) AS mes,p.categoria,
 SUM(v.ingresos_netos) AS ingresos,
 COUNT(DISTINCT CASE WHEN v.tipo_operacion='VENTA' THEN v.documento_id END) AS documentos_venta
FROM ventas_analiticas v JOIN productos p USING(producto_id)
WHERE v.cliente_id=17 AND v.fecha>='2025-08-01' AND v.fecha<'2025-10-01'
GROUP BY substr(v.fecha,1,7),p.categoria
ORDER BY mes,p.categoria;
