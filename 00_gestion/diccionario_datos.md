# Diccionario de datos — versión 1

Todos los campos son obligatorios salvo los indicados como opcionales. PK significa identificador único; FK, referencia a otra tabla. Fechas: texto ISO `AAAA-MM-DD`. Importes: enteros CLP sin IVA. No se utilizan números decimales binarios para almacenar dinero.

## productos
Una fila por producto. La categoría permanece fija durante el período del caso.

| Campo | Tipo | Regla |
|---|---|---|
| producto_id | INTEGER, PK | Positivo |
| nombre | TEXT | No vacío |
| categoria | TEXT | No vacía; catálogo de 5 categorías documentado al generar datos |
| unidad_medida | TEXT | Unidad comercial fija, por ejemplo unidad, caja o paquete |

## clientes
Una fila por empresa ficticia. El segmento y la región permanecen fijos durante el caso.

| Campo | Tipo | Regla |
|---|---|---|
| cliente_id | INTEGER, PK | Positivo |
| nombre | TEXT | Nombre ficticio no vacío |
| segmento | TEXT | No vacío; catálogo documentado al generar datos |
| region | TEXT | No vacía |

## calendario
Una fila por día entre 2025-01-01 y 2025-09-30, sin huecos.

| Campo | Tipo | Regla |
|---|---|---|
| fecha | TEXT, PK | Fecha válida |
| mes | TEXT | Primer día del mes; también clave de agrupación mensual |
| anio | INTEGER | 2025 |
| numero_mes | INTEGER | 1 a 9 |
| trimestre | INTEGER | 1 a 3 |

## ventas
Una fila por producto dentro de un documento de venta o devolución. Un documento puede contener varias líneas. No se mezclan ventas y devoluciones en un mismo documento.

| Campo | Tipo | Regla |
|---|---|---|
| linea_id | INTEGER, PK | Positivo |
| documento_id | TEXT | No vacío |
| numero_linea | INTEGER | Positivo; único dentro del documento |
| tipo_operacion | TEXT | VENTA o DEVOLUCION |
| linea_original_id | INTEGER, FK ventas | Opcional solo para VENTA; obligatorio para DEVOLUCION |
| fecha | TEXT, FK calendario | Día de operación |
| producto_id | INTEGER, FK productos | Producto existente |
| cliente_id | INTEGER, FK clientes | Cliente existente |
| canal | TEXT | DIRECTO u ONLINE |
| cantidad | INTEGER | Mayor que cero, incluso en devoluciones |
| precio_lista_unitario | INTEGER | Mayor que cero |
| descuento_importe | INTEGER | Entre cero e importe bruto |
| ingreso_neto_importe | INTEGER | Generado: cantidad × precio de lista − descuento |
| costo_ventas_importe | INTEGER | Cero o positivo; costo total de la línea |

El precio efectivo unitario y costo unitario se calculan dividiendo los importes de la línea por cantidad; no se almacenan duplicados. No se suman unidades de productos con unidades de medida distintas para inferir volumen agregado.

## gastos
Una fila por movimiento de gasto o reverso. Los reversos permiten corregir importes sin borrar movimientos.

| Campo | Tipo | Regla |
|---|---|---|
| movimiento_id | INTEGER, PK | Positivo |
| fecha | TEXT, FK calendario | Día del registro contable |
| documento_id | TEXT | Referencia ficticia no vacía |
| cuenta | TEXT | Cuenta operacional del catálogo compartido con presupuesto |
| centro_costo | TEXT | Centro del catálogo compartido con presupuesto |
| tipo_movimiento | TEXT | GASTO o REVERSO |
| importe | INTEGER | Mayor que cero; el signo se aplica al consultar |

## presupuesto_comercial
Una fila por mes, producto y canal. Presupuesto inicial fijo; ingresos y costos corresponden a montos netos previstos, después de devoluciones esperadas.

| Campo | Tipo | Regla |
|---|---|---|
| mes | TEXT, FK calendario.fecha | Primer día del mes |
| producto_id | INTEGER, FK productos | Producto existente |
| canal | TEXT | DIRECTO u ONLINE |
| unidades_netas | INTEGER | Cero o positivo |
| ingresos_netos | INTEGER | Cero o positivo |
| costo_ventas | INTEGER | Cero o positivo |

PK compuesta: mes, producto_id, canal. No unir cada venta directamente al presupuesto: primero agregar las ventas a esta granularidad.

## presupuesto_gastos
Una fila por mes, cuenta y centro de costo.

| Campo | Tipo | Regla |
|---|---|---|
| mes | TEXT, FK calendario.fecha | Primer día del mes |
| cuenta | TEXT | Mismo catálogo que gastos |
| centro_costo | TEXT | Mismo catálogo que gastos |
| importe | INTEGER | Cero o positivo |

PK compuesta: mes, cuenta, centro_costo. Agregar gastos al mismo nivel antes de comparar.
