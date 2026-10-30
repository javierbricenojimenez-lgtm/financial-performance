-- Una fila por producto y mes: no promediar precios de líneas sin ponderar.
SELECT p.producto_id,p.nombre,p.categoria,substr(v.fecha,1,7) mes,
 SUM(v.unidades_netas) unidades,
 SUM(v.ingresos_netos) ingresos,
 SUM(v.costo_neto) costos,
 SUM(v.signo*v.cantidad*v.precio_lista_unitario) bruto,
 SUM(v.signo*v.descuento_importe) descuentos
FROM ventas_analiticas v JOIN productos p USING(producto_id)
WHERE v.fecha >= '2025-08-01' AND v.fecha < '2025-10-01'
GROUP BY p.producto_id,p.nombre,p.categoria,substr(v.fecha,1,7)
ORDER BY p.producto_id,mes;

-- Gastos reales: reversos descontados.
SELECT substr(fecha,1,7) mes,cuenta,centro_costo,
 SUM(CASE WHEN tipo_movimiento='GASTO' THEN importe ELSE -importe END) importe
FROM gastos GROUP BY mes,cuenta,centro_costo;

-- Presupuesto agregado ANTES de combinarlo con los reales.
WITH comercial AS (
 SELECT substr(mes,1,7) mes,SUM(ingresos_netos) ingresos,SUM(costo_ventas) costos
 FROM presupuesto_comercial GROUP BY substr(mes,1,7)
), gastos AS (
 SELECT substr(mes,1,7) mes,SUM(importe) gastos
 FROM presupuesto_gastos GROUP BY substr(mes,1,7)
)
SELECT comercial.*,gastos.gastos,ingresos-costos-gastos.gastos utilidad
FROM comercial JOIN gastos USING(mes) ORDER BY mes;
