SELECT cl.nombre AS cliente,v.fecha,v.documento_id,v.cantidad AS packs,
 v.ingreso_neto_importe AS ingreso_revertido,
 v.costo_ventas_importe AS costo_revertido,
 v.ingreso_neto_importe-v.costo_ventas_importe AS margen_revertido,
 o.fecha AS fecha_venta
FROM ventas v
JOIN clientes cl USING(cliente_id)
JOIN ventas o ON o.linea_id=v.linea_original_id
WHERE v.producto_id=17 AND v.tipo_operacion='DEVOLUCION'
 AND v.fecha >= '2025-09-01' AND v.fecha < '2025-10-01'
ORDER BY v.fecha;
