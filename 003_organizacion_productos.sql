-- Comparación del margen bruto por producto. CLP netos de devoluciones.
WITH margenes AS (
 SELECT p.producto_id, p.nombre,
 SUM(CASE WHEN substr(v.fecha,1,7)='2025-08'
     THEN v.ingresos_netos-v.costo_neto ELSE 0 END) AS agosto,
 SUM(CASE WHEN substr(v.fecha,1,7)='2025-09'
     THEN v.ingresos_netos-v.costo_neto ELSE 0 END) AS septiembre
 FROM ventas_analiticas v
 JOIN productos p USING(producto_id)
 WHERE p.categoria='Organización'
   AND v.fecha >= '2025-08-01' AND v.fecha < '2025-10-01'
 GROUP BY p.producto_id, p.nombre
)
SELECT *, septiembre-agosto AS diferencia
FROM margenes
ORDER BY diferencia;
