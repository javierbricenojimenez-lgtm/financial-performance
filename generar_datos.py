"""Caso 100% sintético. Python estándar; ejecutar desde cualquier directorio."""
import calendar
import datetime as dt
import hashlib
import json
import math
import random
import sqlite3
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 20251029
TARGETS = [
    (78000000, 45240000, 18000000), (74000000, 42920000, 18000000),
    (98000000, 56840000, 19000000), (88000000, 51920000, 18500000),
    (92000000, 54280000, 19000000), (90000000, 54000000, 19500000),
    (95000000, 57000000, 19500000), (100000000, 60000000, 20000000),
    (108000000, 70000000, 21000000),
]
CATEGORIES = ['Papel y cuadernos', 'Escritura', 'Organización', 'Tecnología', 'Insumos de impresión']
NAMES = [
 ['Resma carta', 'Resma oficio', 'Resma A4', 'Cuaderno ejecutivo', 'Block notas', 'Papel fotográfico'],
 ['Bolígrafos caja', 'Lápices caja', 'Marcadores caja', 'Destacadores caja', 'Correctores caja', 'Plumones caja'],
 ['Archivadores pack', 'Carpetas pack', 'Bandeja escritorio', 'Organizador', 'Cajas archivo pack', 'Separadores pack'],
 ['Mouse', 'Teclado', 'Hub USB', 'Webcam', 'Audífonos', 'Disco externo'],
 ['Tóner A', 'Tóner B', 'Cartucho negro', 'Cartucho color', 'Tinta botella', 'Kit mantenimiento'],
]
PRICES = [[4800,5200,4900,6500,2200,8900], [4200,3500,7800,6900,5400,8200],
          [12500,9800,6500,11500,14500,4800], [9500,14500,18500,32000,22000,65000],
          [39000,45000,18500,24500,12500,58000]]
ACCOUNTS = ['Remuneraciones','Arriendo','Logística','Marketing','Servicios','Depreciación']
CENTERS = ['Administración','Comercial','Operaciones']
TABLES = ['productos','clientes','calendario','ventas','gastos','presupuesto_comercial','presupuesto_gastos']


def allocate(total, weights):
    """Reparte pesos enteros con suma exacta mediante restos mayores."""
    raw = [total * w / sum(weights) for w in weights]
    result = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: (-(raw[i]-result[i]), i))[:total-sum(result)]:
        result[i] += 1
    return result


def build():
    rng = random.Random(SEED)
    data = {t: [] for t in TABLES}
    base_price = {}
    for cat in range(5):
        for j in range(6):
            pid = cat*6+j+1
            data['productos'].append(dict(producto_id=pid,nombre=NAMES[cat][j],categoria=CATEGORIES[cat],unidad_medida='pack' if cat in (1,2) else 'unidad'))
            base_price[pid] = PRICES[cat][j]
    regions = ['Metropolitana','Valparaíso','Biobío','Maule','La Araucanía','Los Lagos']
    for i in range(1,101):
        data['clientes'].append(dict(cliente_id=i,nombre=f'Empresa Ficticia {i:03d}',
            segmento='Mediana' if i <= 25 else 'Pequeña',region=regions[(i-1)%6]))
    day = dt.date(2025,1,1)
    while day <= dt.date(2025,9,30):
        data['calendario'].append(dict(fecha=str(day),mes=str(day.replace(day=1)),anio=2025,numero_mes=day.month,trimestre=(day.month-1)//3+1))
        day += dt.timedelta(days=1)
    calibration = []
    line_id = 0
    for month, (target_rev,target_cost,target_exp) in enumerate(TARGETS,1):
        n = [920,880,1160,1020,1080,1050,1100,1150,1250][month-1]
        days = [d['fecha'] for d in data['calendario'] if d['numero_mes']==month and dt.date.fromisoformat(d['fecha']).weekday()<5]
        # Volúmenes, categorías y perfiles se generan antes de calibrar los totales.
        cat_weights = [30,23,20,12,15] if month < 9 else [23,17,15,20,25]
        rows = []
        for _ in range(n):
            cat = rng.choices(range(5),weights=cat_weights)[0]
            pid = cat*6+rng.randint(1,6)
            cid = rng.choices(range(1,101),weights=[3 if i<=25 else 1 for i in range(1,101)])[0]
            channel = 'DIRECTO' if rng.random() < (0.85 if cid<=25 else 0.52) else 'ONLINE'
            qty = rng.randint(5,28) if cid<=25 else rng.randint(1,12)
            price = base_price[pid] * (1+0.003*(month-1))
            discount = rng.choice([0,0.02,0.04,0.06]) + (0.04 if cid<=25 else 0)
            if month==9 and channel=='DIRECTO':
                discount += 0.035
            cost_ratio = [0.55,0.46,0.50,0.72,0.69][cat]
            cost_increase = 1 + (0.06 if month==9 and cat==4 else 0) + 0.002*(month-1)
            rows.append(dict(pid=pid,cid=cid,channel=channel,qty=qty,price=price,discount=discount,
                raw_rev=qty*price*(1-discount),raw_cost=qty*base_price[pid]*cost_ratio*cost_increase,
                date=rng.choice(days)))
        returned = set(rng.sample(range(n),round(n*(0.025 if month<9 else 0.04))))
        kept = [i for i in range(n) if i not in returned]
        rev_factor = target_rev / sum(rows[i]['raw_rev'] for i in kept)
        cost_factor = target_cost / sum(rows[i]['raw_cost'] for i in kept)
        revs = allocate(target_rev,[rows[i]['raw_rev'] for i in kept])
        costs = allocate(target_cost,[rows[i]['raw_cost'] for i in kept])
        assigned = dict(zip(kept,zip(revs,costs)))
        calibration.append(dict(mes=f'2025-{month:02d}',factor_ingresos=rev_factor,factor_costos=cost_factor))
        for i, row in enumerate(rows):
            net,cost = assigned.get(i,(round(row['raw_rev']*rev_factor),round(row['raw_cost']*cost_factor)))
            price = math.ceil(net / (row['qty']*(1-row['discount'])))
            line_id += 1
            original = dict(linea_id=line_id,documento_id=f'FV-{month:02d}-{i+1:05d}',numero_linea=1,
                tipo_operacion='VENTA',linea_original_id=None,fecha=row['date'],producto_id=row['pid'],
                cliente_id=row['cid'],canal=row['channel'],cantidad=row['qty'],precio_lista_unitario=price,
                descuento_importe=row['qty']*price-net,costo_ventas_importe=cost)
            data['ventas'].append(original)
            if i in returned:
                line_id += 1
                last = calendar.monthrange(2025,month)[1]
                return_date = min(dt.date.fromisoformat(row['date'])+dt.timedelta(days=rng.randint(1,7)),dt.date(2025,month,last))
                data['ventas'].append(dict(original,linea_id=line_id,documento_id=f'NC-{month:02d}-{i+1:05d}',
                    tipo_operacion='DEVOLUCION',linea_original_id=original['linea_id'],fecha=str(return_date)))
        # 18 combinaciones de gastos, cada una distribuida en tres movimientos.
        weights = []
        for a in range(6):
            for c in range(3):
                weights.append([48,15,14,9,9,5][a]*[0.40,0.25,0.35][c]*(1.35 if month==9 and a in (2,3) else 1))
        for idx,total in enumerate(allocate(target_exp,weights)):
            for part,amount in enumerate(allocate(total,[0.5,0.3,0.2]),1):
                mid = len(data['gastos'])+1
                data['gastos'].append(dict(movimiento_id=mid,fecha=f'2025-{month:02d}-{[5,15,25][part-1]:02d}',
                    documento_id=f'GO-{mid:05d}',cuenta=ACCOUNTS[idx//3],centro_costo=CENTERS[idx%3],tipo_movimiento='GASTO',importe=amount))
        # Presupuesto independiente: crecimiento planificado, mezcla estable y costos de referencia.
        plan_rev = [80000000,76000000,96000000,90000000,94000000,93000000,97000000,102000000,106000000][month-1]
        combos = [(pid,channel) for pid in range(1,31) for channel in ('DIRECTO','ONLINE')]
        plan_weights = [([30,23,20,12,15][(pid-1)//6]/6)*(0.65 if ch=='DIRECTO' else 0.35) for pid,ch in combos]
        plan_revs = allocate(plan_rev,plan_weights)
        for (pid,ch),revenue in zip(combos,plan_revs):
            data['presupuesto_comercial'].append(dict(mes=f'2025-{month:02d}-01',producto_id=pid,canal=ch,
                unidades_netas=round(revenue/(base_price[pid]*0.95)),ingresos_netos=revenue,
                costo_ventas=round(revenue*[0.58,0.50,0.54,0.75,0.72][(pid-1)//6])))
        pexp = [18200000,18200000,18800000,18800000,19000000,19200000,19500000,19800000,20200000][month-1]
        for idx,amount in enumerate(allocate(pexp,[a*c for a in [48,15,14,9,9,5] for c in [0.4,0.25,0.35]])):
            data['presupuesto_gastos'].append(dict(mes=f'2025-{month:02d}-01',cuenta=ACCOUNTS[idx//3],centro_costo=CENTERS[idx%3],importe=amount))
    return data,calibration


def load(path,data):
    con = sqlite3.connect(path)
    con.executescript((ROOT/'03_sql/001_esquema.sql').read_text(encoding='utf-8'))
    for table,rows in data.items():
        cols = list(rows[0])
        con.executemany(f'INSERT INTO {table} ({",".join(cols)}) VALUES ({",".join("?" for _ in cols)})',
                        [tuple(r[k] for k in cols) for r in rows])
    con.executescript('''
    CREATE VIEW ventas_analiticas AS
    SELECT v.*, CASE WHEN tipo_operacion='VENTA' THEN 1 ELSE -1 END AS signo,
      CASE WHEN tipo_operacion='VENTA' THEN cantidad ELSE -cantidad END AS unidades_netas,
      CASE WHEN tipo_operacion='VENTA' THEN ingreso_neto_importe ELSE -ingreso_neto_importe END AS ingresos_netos,
      CASE WHEN tipo_operacion='VENTA' THEN costo_ventas_importe ELSE -costo_ventas_importe END AS costo_neto
    FROM ventas v;
    CREATE VIEW estado_resultados_mensual AS
    WITH v AS (SELECT substr(fecha,1,7) mes, SUM(ingresos_netos) ingresos,
       SUM(costo_neto) costo_ventas FROM ventas_analiticas GROUP BY 1),
    g AS (SELECT substr(fecha,1,7) mes,
       SUM(CASE WHEN tipo_movimiento='GASTO' THEN importe ELSE -importe END) gastos
       FROM gastos GROUP BY 1)
    SELECT v.mes, ingresos, costo_ventas, ingresos-costo_ventas margen_bruto,
       gastos, ingresos-costo_ventas-gastos utilidad_operacional,
       1.0*(ingresos-costo_ventas-gastos)/NULLIF(ingresos,0) margen_operacional
    FROM v JOIN g USING(mes);
    ''')
    con.commit()
    return con


def validate(con,data):
    checks = []
    def check(name,condition):
        checks.append(dict(control=name,resultado='OK' if condition else 'ERROR'))
        if not condition:
            raise AssertionError(name)
    check('Integridad SQLite',con.execute('pragma integrity_check').fetchone()[0]=='ok')
    check('Claves externas',not con.execute('pragma foreign_key_check').fetchall())
    dates = [r['fecha'] for r in data['calendario']]
    expected = [str(dt.date(2025,1,1)+dt.timedelta(days=i)) for i in range(273)]
    check('Calendario completo y coherente',dates==expected and all(r['mes']==r['fecha'][:7]+'-01' and r['numero_mes']==int(r['fecha'][5:7]) and r['trimestre']==(r['numero_mes']-1)//3+1 for r in data['calendario']))
    originals = {r['linea_id']:r for r in data['ventas'] if r['tipo_operacion']=='VENTA'}
    returns = [r for r in data['ventas'] if r['tipo_operacion']=='DEVOLUCION']
    keys = ['producto_id','cliente_id','canal','cantidad','precio_lista_unitario','descuento_importe','costo_ventas_importe']
    check('Devoluciones con referencia, identidad y valor correctos',all(r['linea_original_id'] in originals and all(r[k]==originals[r['linea_original_id']][k] for k in keys) and r['fecha']>=originals[r['linea_original_id']]['fecha'] for r in returns))
    check('Sin devoluciones acumuladas excesivas',len({r['linea_original_id'] for r in returns})==len(returns))
    check('Documentos consistentes',not con.execute('''SELECT documento_id FROM ventas GROUP BY documento_id HAVING count(DISTINCT fecha)>1 OR count(DISTINCT cliente_id)>1 OR count(DISTINCT canal)>1 OR count(DISTINCT tipo_operacion)>1''').fetchall())
    check('Catálogos y cobertura',len(data['productos'])==30 and len(data['clientes'])==100 and len(data['presupuesto_comercial'])==540 and len(data['presupuesto_gastos'])==162 and {r['cuenta'] for r in data['gastos']}==set(ACCOUNTS) and {r['centro_costo'] for r in data['gastos']}==set(CENTERS))
    results = con.execute('SELECT mes,ingresos,costo_ventas,gastos,utilidad_operacional FROM estado_resultados_mensual ORDER BY mes').fetchall()
    check('Conciliación exacta de nueve meses',len(results)==9 and all(tuple(row[1:4])==target for row,target in zip(results,TARGETS)))
    # Recalcular desde los registros fuente, sin usar las vistas ni sus signos calculados.
    manual = {}
    for month in range(1,10):
        prefix = f'2025-{month:02d}'
        vs = [r for r in data['ventas'] if r['fecha'].startswith(prefix)]
        revenue = sum((r['cantidad']*r['precio_lista_unitario']-r['descuento_importe'])*(1 if r['tipo_operacion']=='VENTA' else -1) for r in vs)
        cost = sum(r['costo_ventas_importe']*(1 if r['tipo_operacion']=='VENTA' else -1) for r in vs)
        expense = sum(r['importe']*(1 if r['tipo_movimiento']=='GASTO' else -1) for r in data['gastos'] if r['fecha'].startswith(prefix))
        manual[prefix] = (revenue,cost,expense,revenue-cost-expense)
    check('Recálculo independiente Python frente a SQL',all(tuple(r[1:])==manual[r[0]] for r in results))
    check('Todos los productos y clientes con actividad',con.execute('select count(distinct producto_id),count(distinct cliente_id) from ventas').fetchone()==(30,100))
    check('Sin costos superiores al ingreso en líneas de venta',con.execute("select count(*) from ventas where tipo_operacion='VENTA' and costo_ventas_importe>ingreso_neto_importe").fetchone()[0]==0)
    return checks,results


def main():
    raw = ROOT/'01_datos_originales'
    out = ROOT/'outputs'
    raw.mkdir(exist_ok=True)
    out.mkdir(exist_ok=True)
    data,calibration = build()
    payload = json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    again,_ = build()
    assert data==again, 'Generación no reproducible'
    digest = hashlib.sha256(payload).hexdigest()
    # Validar en memoria antes de publicar el archivo definitivo.
    con = load(':memory:',data)
    checks,results = validate(con,data)
    checks.append(dict(control='Reproducibilidad con semilla fija',resultado='OK'))
    destination = sqlite3.connect(out/'financial_performance.sqlite')
    con.backup(destination)
    destination.close()
    con.close()
    (raw/'datos_sinteticos.json').write_bytes(payload)
    manifest = dict(tipo='DATOS SINTÉTICOS — NO REPRESENTAN UNA EMPRESA REAL',semilla=SEED,
        periodo='2025-01-01 a 2025-09-30',moneda='CLP sin IVA',sha256_fuente=digest,
        filas={t:len(rows) for t,rows in data.items()},calibracion_mensual=calibration,
        controles=checks)
    (out/'manifiesto_validacion.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    report = ['# Datos sintéticos: generación y validación','',
        '**Caso ficticio, no evidencia de una empresa real.**','',
        f'Semilla: {SEED}. Período: enero a septiembre de 2025. Importes en CLP sin IVA.', '',
        '## Contenido','', '| Tabla | Filas |','|---|---:|']
    report += [f'| {t} | {len(rows):,} |' for t,rows in data.items()]
    report += ['', '## Estado de resultados (millones de CLP)','',
        '| Mes | Ingresos | Costos | Gastos | Utilidad operacional |','|---|---:|---:|---:|---:|']
    report += [f'| {r[0]} | {r[1]/1e6:.2f} | {r[2]/1e6:.2f} | {r[3]/1e6:.2f} | {r[4]/1e6:.2f} |' for r in results]
    report += ['', '## Controles','']+[f'- {c["resultado"]}: {c["control"]}.' for c in checks]
    report += ['', '## Cómo se construyó el caso','',
        'Las ventas se distribuyen en días hábiles sin ajustar feriados. Los clientes medianos compran más unidades y usan con mayor frecuencia el canal directo. Se utilizan 30 productos en cinco categorías, precios distintos, descuentos y costos por categoría.', '',
        'Septiembre tiene mayor peso de tecnología e impresión, descuentos adicionales en venta directa, mayor costo relativo de impresión y más devoluciones. Logística y marketing tienen mayor peso en gastos. Son señales introducidas deliberadamente para practicar análisis; no son hallazgos descubiertos.', '',
        'Los importes se calibran mensualmente a los estados de resultados del caso: ingresos y costos se escalan por separado sobre las ventas no devueltas y se distribuyen con restos mayores para cuadrar exactamente al peso. El precio de lista y descuento se reconstruyen desde el ingreso asignado. Esto modifica los precios y costos observados entre meses: cualquier descomposición posterior debe considerar la calibración, no atribuir toda la variación a las señales iniciales. Los factores se publican en el manifiesto.', '',
        'El presupuesto se genera con parámetros planificados independientes, sin copiar el real. Todas las devoluciones son completas, una por venta seleccionada y dentro del mismo mes. Cada documento tiene una línea: es una simplificación. No se simulan devoluciones parciales, gastos reversados, compras, stock ni proveedores. La región corresponde al domicilio del cliente; no es una sucursal.', '',
        'La fuente inicial está limpia para construir primero un diagnóstico financiero confiable. Más adelante podrá crearse una copia separada con errores deliberados para practicar limpieza, conservando esta referencia.', '',
        '## Uso','',
        'Abrir financial_performance.sqlite con un explorador SQLite. Consultar ventas_analiticas para importes con signo y estado_resultados_mensual para la conciliación. Las tablas originales guardan importes positivos; no sumar devoluciones como ingresos.', '',
        'Para regenerar, ejecutar 04_python/generar_datos.py con Python 3.11 o posterior y SQLite 3.37 o posterior. Solo utiliza la biblioteca estándar. La regeneración reemplaza exclusivamente los archivos generados por este script; no editar la base generada como fuente maestra.', '',
        f'SHA-256 de la fuente JSON: `{digest}`.', '',
        'Este documento describe la generación de datos, no el estado del proyecto completo. Los escenarios y recomendaciones, cuando estén generados, se consultan en INFORME_FINAL.md. Los datos no demuestran una mejora económica real.']
    (out/'LEEME_DATOS.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    with zipfile.ZipFile(out/'datos_financieros_sinteticos.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in [out/'financial_performance.sqlite',out/'LEEME_DATOS.md',out/'manifiesto_validacion.json',raw/'datos_sinteticos.json',Path(__file__),ROOT/'03_sql/001_esquema.sql',ROOT/'00_gestion/diccionario_datos.md',ROOT/'00_gestion/reglas_validacion.md']:
            z.write(p,p.relative_to(ROOT))
    print(json.dumps(dict(filas=manifest['filas'],controles=len(checks),resultado='OK',sha256=digest),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
