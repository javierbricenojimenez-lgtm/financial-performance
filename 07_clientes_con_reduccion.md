# Comparación de los 29 clientes con reducción de Cajas archivo pack

> Nota de versión: documento intermedio conservado para trazabilidad. Los pasos pendientes reflejan su fecha de elaboración. El estado actual está en INFORME_FINAL.md y AUDITORIA_CONSISTENCIA.md.

Fuente: ventas_analiticas de la base sintética local. Cohorte: clientes cuyas unidades netas del producto 17 de septiembre son menores a las de agosto. Frecuencia histórica: meses distintos con documentos de VENTA del producto entre enero y agosto. Actividad restante: documentos de VENTA de otros productos en septiembre.

## Resultados comprobados con SQL

- 24 clientes pasaron a cero packs netos: caída de 295 packs. Se verificó que ninguno registró ventas brutas ni devoluciones del producto en septiembre: el cero no resulta de cancelaciones.
- Otros 5 clientes redujeron su compra neta de 110 a 65 packs: caída de 45.
- Los 29 clientes registraron ventas de otros productos en septiembre. No hay abandono total observado en esta cohorte durante ese mes.
- Su frecuencia histórica del producto va de 1 a 7 meses de compra sobre los 8 meses enero-agosto. Ninguno compró el producto en los 8 meses. Esto describe compras intermitentes, sin demostrar que la caída de septiembre sea normal.
- Empresa Ficticia 019 compró 52 packs brutos y devolvió 26 en septiembre; su compra neta fue 26, frente a 35 en agosto. Por tanto, menor compra neta no siempre significa menos compra bruta: las devoluciones importan. Falta comparar sus devoluciones de agosto para descomponer el cambio.

Las caídas de compra neta de esta cohorte, antes de compensarlas con aumentos de otros clientes, suman 340 packs. Otros clientes compensan 146 packs y la caída neta de todo el producto es 194. No confundir esta suma de reducciones con una caída de ventas brutas antes de devoluciones.

## Ejemplos

| Cliente ficticio | Agosto neto | Septiembre neto | Meses de compra ene-ago | Documentos de venta de otros productos en septiembre |
|---|---:|---:|---:|---:|
| 017 | 50 | 0 | 6 | 25 |
| 024 | 22 | 0 | 4 | 23 |
| 027 | 20 | 0 | 3 | 8 |
| 006 | 32 | 17 | 4 | 20 |
| 019 | 35 | 26 | 7 | 19 |

Conclusión limitada: la reducción se concentra en la compra de este producto, mientras se mantiene actividad comercial con los clientes. No se ha probado falta de stock, sustitución, pérdida frente a competidores, menor consumo físico ni acumulación de inventario. Las ventas miden compras a nuestra empresa, no consumo final del cliente. El generador no contiene motivos comerciales individuales.

Próximo paso acotado: separar compras brutas y devoluciones para los cinco clientes con reducción parcial, antes de proponer explicaciones de demanda. Una causa comercial real requeriría evidencia adicional.
