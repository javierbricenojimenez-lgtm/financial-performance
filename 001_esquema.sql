-- SQLite >= 3.37. Ejecutar sobre una base nueva.
PRAGMA foreign_keys = ON;
BEGIN;
CREATE TABLE productos (
 producto_id INTEGER PRIMARY KEY CHECK(producto_id > 0),
 nombre TEXT NOT NULL CHECK(length(trim(nombre)) > 0),
 categoria TEXT NOT NULL CHECK(length(trim(categoria)) > 0),
 unidad_medida TEXT NOT NULL CHECK(length(trim(unidad_medida)) > 0)
) STRICT;
CREATE TABLE clientes (
 cliente_id INTEGER PRIMARY KEY CHECK(cliente_id > 0),
 nombre TEXT NOT NULL CHECK(length(trim(nombre)) > 0),
 segmento TEXT NOT NULL CHECK(length(trim(segmento)) > 0),
 region TEXT NOT NULL CHECK(length(trim(region)) > 0)
) STRICT;
CREATE TABLE calendario (
 fecha TEXT PRIMARY KEY NOT NULL CHECK(fecha BETWEEN '2025-01-01' AND '2025-09-30'),
 mes TEXT NOT NULL CHECK(length(mes) = 10 AND substr(mes,9,2) = '01'),
 anio INTEGER NOT NULL CHECK(anio = 2025),
 numero_mes INTEGER NOT NULL CHECK(numero_mes BETWEEN 1 AND 9),
 trimestre INTEGER NOT NULL CHECK(trimestre BETWEEN 1 AND 3)
) STRICT;
CREATE TABLE ventas (
 linea_id INTEGER PRIMARY KEY CHECK(linea_id > 0),
 documento_id TEXT NOT NULL CHECK(length(trim(documento_id)) > 0),
 numero_linea INTEGER NOT NULL CHECK(numero_linea > 0),
 tipo_operacion TEXT NOT NULL CHECK(tipo_operacion IN ('VENTA','DEVOLUCION')),
 linea_original_id INTEGER REFERENCES ventas(linea_id),
 fecha TEXT NOT NULL REFERENCES calendario(fecha),
 producto_id INTEGER NOT NULL REFERENCES productos(producto_id),
 cliente_id INTEGER NOT NULL REFERENCES clientes(cliente_id),
 canal TEXT NOT NULL CHECK(canal IN ('DIRECTO','ONLINE')),
 cantidad INTEGER NOT NULL CHECK(cantidad > 0),
 precio_lista_unitario INTEGER NOT NULL CHECK(precio_lista_unitario > 0),
 descuento_importe INTEGER NOT NULL CHECK(descuento_importe BETWEEN 0 AND cantidad * precio_lista_unitario),
 ingreso_neto_importe INTEGER GENERATED ALWAYS AS (cantidad * precio_lista_unitario - descuento_importe) STORED,
 costo_ventas_importe INTEGER NOT NULL CHECK(costo_ventas_importe >= 0),
 UNIQUE(documento_id, numero_linea),
 CHECK((tipo_operacion = 'VENTA' AND linea_original_id IS NULL) OR
       (tipo_operacion = 'DEVOLUCION' AND linea_original_id IS NOT NULL AND linea_original_id <> linea_id))
) STRICT;
CREATE TABLE gastos (
 movimiento_id INTEGER PRIMARY KEY CHECK(movimiento_id > 0),
 fecha TEXT NOT NULL REFERENCES calendario(fecha),
 documento_id TEXT NOT NULL CHECK(length(trim(documento_id)) > 0),
 cuenta TEXT NOT NULL CHECK(length(trim(cuenta)) > 0),
 centro_costo TEXT NOT NULL CHECK(length(trim(centro_costo)) > 0),
 tipo_movimiento TEXT NOT NULL CHECK(tipo_movimiento IN ('GASTO','REVERSO')),
 importe INTEGER NOT NULL CHECK(importe > 0)
) STRICT;
CREATE TABLE presupuesto_comercial (
 mes TEXT NOT NULL REFERENCES calendario(fecha) CHECK(substr(mes,9,2) = '01'),
 producto_id INTEGER NOT NULL REFERENCES productos(producto_id),
 canal TEXT NOT NULL CHECK(canal IN ('DIRECTO','ONLINE')),
 unidades_netas INTEGER NOT NULL CHECK(unidades_netas >= 0),
 ingresos_netos INTEGER NOT NULL CHECK(ingresos_netos >= 0),
 costo_ventas INTEGER NOT NULL CHECK(costo_ventas >= 0),
 PRIMARY KEY(mes, producto_id, canal)
) STRICT;
CREATE TABLE presupuesto_gastos (
 mes TEXT NOT NULL REFERENCES calendario(fecha) CHECK(substr(mes,9,2) = '01'),
 cuenta TEXT NOT NULL CHECK(length(trim(cuenta)) > 0),
 centro_costo TEXT NOT NULL CHECK(length(trim(centro_costo)) > 0),
 importe INTEGER NOT NULL CHECK(importe >= 0),
 PRIMARY KEY(mes, cuenta, centro_costo)
) STRICT;
CREATE INDEX idx_ventas_fecha_producto ON ventas(fecha, producto_id);
CREATE INDEX idx_ventas_original ON ventas(linea_original_id);
CREATE INDEX idx_gastos_fecha ON gastos(fecha);
COMMIT;
