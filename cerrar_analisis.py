"""Diagnóstico y entregables. Solo biblioteca estándar. Base en lectura."""
from pathlib import Path
from fractions import Fraction as F
import sqlite3, json, html, hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'
def pesos(v): return '$'+f'{round(v):,}'.replace(',','.')
def mm(v): return f'{float(v)/1e6:.3f}'.replace('.',',')
def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(str(x) for x in r)+' |' for r in rows)
def query(c,sql): return [dict(r) for r in c.execute(sql)]

def main():
    c=sqlite3.connect((OUT/'financial_performance.sqlite').as_uri()+'?mode=ro',uri=True)
    c.row_factory=sqlite3.Row
    sql=(ROOT/'03_sql/010_diagnostico_final.sql').read_text(encoding='utf-8').split(';')[0]
    detail=query(c,sql)
    assert len(detail)==60
    monthly=query(c,'SELECT * FROM estado_resultados_mensual ORDER BY mes')
    products=[]
    for pid in range(1,31):
        a,b=[r for r in detail if r['producto_id']==pid]
        q0,q1=a['unidades'],b['unidades']
        assert q0>0 and q1>0
        p0,p1=F(a['ingresos'],q0),F(b['ingresos'],q1)
        k0,k1=F(a['costos'],q0),F(b['costos'],q1)
        l0,l1=F(a['bruto'],q0),F(b['bruto'],q1)
        d0,d1=F(a['descuentos'],q0),F(b['descuentos'],q1)
        effects=dict(volumen=(q1-q0)*(p0-k0),lista=q1*(l1-l0),descuentos=-q1*(d1-d0),costo=-q1*(k1-k0))
        delta=b['ingresos']-b['costos']-a['ingresos']+a['costos']
        assert sum(effects.values())==delta
        products.append(dict(id=pid,nombre=a['nombre'],categoria=a['categoria'],agosto=a,septiembre=b,
            margen_agosto=a['ingresos']-a['costos'],margen_septiembre=b['ingresos']-b['costos'],delta=delta,
            efectos={k:float(v) for k,v in effects.items()}))
    # Índice de cantidad valorada a precios efectivos de agosto. Evita sumar unidades heterogéneas.
    base_sales=sum(r['ingresos'] for r in detail if r['mes']=='2025-08')
    base_margin=sum(p['margen_agosto'] for p in products)
    counter=sum(F(p['septiembre']['unidades']*p['agosto']['ingresos'],p['agosto']['unidades']) for p in products)
    index=counter/base_sales
    volume=(index-1)*base_margin
    mix=sum((p['septiembre']['unidades']-index*p['agosto']['unidades'])*F(p['margen_agosto'],p['agosto']['unidades']) for p in products)
    list_effect=sum(F(p['septiembre']['unidades'])*(F(p['septiembre']['bruto'],p['septiembre']['unidades'])-F(p['agosto']['bruto'],p['agosto']['unidades'])) for p in products)
    discount_effect=sum(-F(p['septiembre']['unidades'])*(F(p['septiembre']['descuentos'],p['septiembre']['unidades'])-F(p['agosto']['descuentos'],p['agosto']['unidades'])) for p in products)
    cost_effect=sum(-F(p['septiembre']['unidades'])*(F(p['septiembre']['costos'],p['septiembre']['unidades'])-F(p['agosto']['costos'],p['agosto']['unidades'])) for p in products)
    bridge=dict(volumen=volume,mezcla=mix,precio_lista=list_effect,descuentos=discount_effect,costo_unitario=cost_effect)
    assert sum(bridge.values())==-2000000
    expenses=query(c,"SELECT cuenta,substr(fecha,1,7) mes,SUM(CASE WHEN tipo_movimiento='GASTO' THEN importe ELSE -importe END) importe FROM gastos WHERE fecha>='2025-08-01' GROUP BY cuenta,mes ORDER BY cuenta,mes")
    accounts=[]
    for name in sorted({r['cuenta'] for r in expenses}):
        a,b=[r['importe'] for r in expenses if r['cuenta']==name]
        accounts.append(dict(cuenta=name,agosto=a,septiembre=b,delta=b-a))
    assert sum(r['delta'] for r in accounts)==1000000
    bridge['gastos_operacionales']=F(-1000000)
    assert sum(bridge.values())==-3000000
    categories=[]
    for cat in sorted({p['categoria'] for p in products}):
        ps=[p for p in products if p['categoria']==cat]
        categories.append(dict(categoria=cat,ingresos_agosto=sum(p['agosto']['ingresos'] for p in ps),ingresos_septiembre=sum(p['septiembre']['ingresos'] for p in ps),margen_agosto=sum(p['margen_agosto'] for p in ps),margen_septiembre=sum(p['margen_septiembre'] for p in ps),delta=sum(p['delta'] for p in ps)))
    budget=query(c,"WITH v AS (SELECT substr(mes,1,7) mes,SUM(ingresos_netos) ingresos,SUM(costo_ventas) costos FROM presupuesto_comercial GROUP BY 1),g AS (SELECT substr(mes,1,7) mes,SUM(importe) gastos FROM presupuesto_gastos GROUP BY 1) SELECT v.*,g.gastos,ingresos-costos-g.gastos utilidad FROM v JOIN g USING(mes) ORDER BY mes")
    bva=[]
    for m in monthly:
        plan=next(b for b in budget if b['mes']==m['mes'])
        bva.append(dict(mes=m['mes'],real=dict(ingresos=m['ingresos'],costos=m['costo_ventas'],gastos=m['gastos'],utilidad=m['utilidad_operacional']),presupuesto={k:plan[k] for k in ['ingresos','costos','gastos','utilidad']}))
    # Priorizar 80% del total de contribuciones negativas, mostrando siempre el resto.
    negative=sorted([p for p in products if p['delta']<0],key=lambda p:p['delta'])
    loss=-sum(p['delta'] for p in negative)
    chosen=[]; covered=0
    for p in negative:
        if covered>=loss*0.8: break
        chosen.append(p); covered-=p['delta']
    # Escenarios aditivos sobre bases distintas. Unidades recuperadas valoradas al margen de septiembre.
    recover=sum(F(max(0,p['agosto']['unidades']-p['septiembre']['unidades'])*p['margen_septiembre'],p['septiembre']['unidades']) for p in products if p['delta']<0)
    gross_direct=c.execute("SELECT SUM(signo*cantidad*precio_lista_unitario) FROM ventas_analiticas WHERE fecha>='2025-09-01' AND canal='DIRECTO'").fetchone()[0]
    extra=sum(max(0,a['delta']) for a in accounts if a['cuenta'] in ['Logística','Marketing'])
    scenarios=[]
    for name,recovery,disc,save,impl in [('Prudente',F(5,100),F(5,1000),F(5,100),100000),('Base',F(10,100),F(1,100),F(10,100),250000)]:
        v=round(recover*recovery); d=round(gross_direct*disc); g=round(extra*save)
        benefit=v+d+g-impl
        scenarios.append(dict(nombre=name,recuperacion_packs_pct=float(recovery*100),reduccion_descuento_pp=float(disc*100),ahorro_incremento_gastos_pct=float(save*100),volumen=v,descuentos=d,gastos=g,costo_ejecucion=impl,impacto_neto=benefit,utilidad_simulada=17000000+benefit))
    case_months=query(c,"SELECT substr(v.fecha,1,7) mes,SUM(v.unidades_netas) unidades,SUM(v.ingresos_netos) ingresos,SUM(v.costo_neto) costos,SUM(CASE WHEN tipo_operacion='VENTA' THEN cantidad ELSE 0 END) vendidos,SUM(CASE WHEN tipo_operacion='DEVOLUCION' THEN cantidad ELSE 0 END) devueltos FROM ventas_analiticas v WHERE producto_id=17 GROUP BY 1 ORDER BY 1")
    case_plan=query(c,"SELECT substr(mes,1,7) mes,SUM(unidades_netas) unidades,SUM(ingresos_netos) ingresos,SUM(costo_ventas) costos FROM presupuesto_comercial WHERE producto_id=17 GROUP BY 1 ORDER BY 1")
    for r in case_months:
        r['margen']=r['ingresos']-r['costos']; r['plan']=next(p for p in case_plan if p['mes']==r['mes']); r['plan']['margen']=r['plan']['ingresos']-r['plan']['costos']
    client_case=query(c,"SELECT cl.nombre cliente,substr(v.fecha,1,7) mes,SUM(v.unidades_netas) unidades,SUM(v.ingresos_netos-v.costo_neto) margen FROM ventas_analiticas v JOIN clientes cl USING(cliente_id) WHERE producto_id=17 AND v.fecha>='2025-08-01' GROUP BY cl.nombre,mes ORDER BY cl.nombre,mes")
    client_comparison=[]
    for name in sorted({r['cliente'] for r in client_case}):
        a=next((r for r in client_case if r['cliente']==name and r['mes']=='2025-08'),dict(unidades=0,margen=0))
        b=next((r for r in client_case if r['cliente']==name and r['mes']=='2025-09'),dict(unidades=0,margen=0))
        client_comparison.append(dict(cliente=name,unidades_agosto=a['unidades'],unidades_septiembre=b['unidades'],margen_agosto=a['margen'],margen_septiembre=b['margen'],delta=b['margen']-a['margen']))
    assert sum(r['delta'] for r in client_comparison)==-1174888
    case_channels=query(c,"SELECT substr(fecha,1,7) mes,canal,SUM(unidades_netas) unidades,SUM(ingresos_netos) ingresos,SUM(ingresos_netos-costo_neto) margen FROM ventas_analiticas WHERE producto_id=17 AND fecha>='2025-08-01' GROUP BY 1,2 ORDER BY 1,2")
    for r in case_channels:
        p=c.execute('SELECT unidades_netas,ingresos_netos,ingresos_netos-costo_ventas FROM presupuesto_comercial WHERE producto_id=17 AND mes=? AND canal=?',(r['mes']+'-01',r['canal'])).fetchone()
        r['plan_unidades'],r['plan_ingresos'],r['plan_margen']=p
    data=dict(monthly=monthly,products=products,categories=categories,accounts=accounts,bva=bva,bridge={k:float(v) for k,v in bridge.items()},scenarios=scenarios,prioridad=[p['nombre'] for p in chosen],cobertura=covered/loss,case_months=case_months,client_comparison=client_comparison,case_channels=case_channels,scenario_bases=dict(volumen=float(recover),lista_directa=gross_direct,gastos=extra))
    (OUT/'resultados_finales.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'ANEXO_METODOLOGICO.md').write_text('''# Método, límites y reproducción

SQL agrega los importes con signo por producto y mes. Python verifica las identidades con fracciones exactas, sin redondeo intermedio. Las tablas de fuentes guardan magnitudes positivas; las vistas aplican el signo una sola vez.

## Puente financiero

Para cada producto: Q = unidades netas; P = ingreso neto / Q; C = costo neto / Q; L = importe de lista neto / Q; D = descuento neto / Q. P=L-D. Agosto es 0 y septiembre 1. Todos los productos tienen Q positiva en ambos meses.

Índice de cantidad V = sum(Q1*P0) / sum(Q0*P0). Es una cantidad valorada a precios base, no una suma física de packs y unidades.

- Volumen = (V-1)*margen0.
- Mezcla = sum((Q1-V*Q0)*(P0-C0)).
- Precio de lista medio = sum(Q1*(L1-L0)).
- Descuentos = -sum(Q1*(D1-D0)).
- Costo unitario = -sum(Q1*(C1-C0)).
- Gastos = -(gastos1-gastos0).

La suma concilia exactamente con la variación de utilidad. El reparto es secuencial, depende del orden y de las ponderaciones. Los importes unitarios son medias ponderadas netas y pueden reflejar composición por cliente/canal. Las devoluciones ya forman parte de Q y de los importes: no añadir sus efectos otra vez al puente.

## Fuente sintética y alcance causal

El generador cambia mezcla, descuentos y algunos costos, y calibra ingresos y costos mensuales por separado para reproducir los estados financieros del caso. Por tanto, los cambios de precios y costos observados también reflejan esa calibración. No atribuir toda reducción de precio a una promoción real, ni ahorro de costo a una negociación. No existen datos de stock, compras, CRM, causas de devolución ni competencia. Las consultas describen y descomponen resultados, no identifican causas comerciales externas.

## Presupuesto

Agregar el real y el plan por mes/producto/canal, o por mes/cuenta/centro, antes de unir. No duplicar plan al relacionarlo con líneas. La desviación es real menos plan. Ingreso y utilidad positivos son favorables en el contexto de este caso; costos y gastos positivos son desfavorables. El plan es sintético e independiente del real.

## Escenarios y seguimiento

1. Recuperación de 5%/10% de los packs/unidades netos perdidos, por producto con contribución negativa al margen. Valorar cada producto a su margen unitario de septiembre y después sumar pesos, sin sumar cantidades heterogéneas.
2. Reducción de descuentos equivalente a 0,5/1 punto porcentual del importe de lista neto del canal directo en septiembre, solo sobre ventas existentes. Mantener cantidades, costo y devoluciones. No aplicar el beneficio de descuento a unidades recuperadas: se omite la interacción para evitar duplicación.
3. Ahorro de 5%/10% del incremento positivo de Logística y Marketing. Mantener los otros gastos.

Restar un costo de ejecución supuesto de $100000/$250000 por mes en prudente/base. Son supuestos ilustrativos, no cotizaciones ni pronósticos validados. No se estima elasticidad. Los escenarios se evalúan como un mes equivalente a septiembre, no como acumulado anual. Validar viabilidad, costos y reacción de demanda antes de actuar.

Seguimiento propuesto: Finanzas concilia margen y utilidad mensualmente; Comercial revisa precio efectivo, descuento sobre lista, compra por producto y cohortes de clientes; Operaciones registra unidades devueltas, motivo y costo. Comparar con una base aprobada, controlar estacionalidad y usar un piloto para evaluar acciones. Ninguna acción se ha implementado en una empresa real.

## Reproducción

Python >=3.11 y SQLite >=3.37, sin dependencias externas para datos y análisis. Desde la raíz ejecutar `python 04_python/generar_datos.py` y después `python 04_python/cerrar_analisis.py`. Abrir outputs/dashboard.html localmente. El generador restablece la base original; no usar la base generada como fuente editable. Las presentaciones se actualizan aparte al cambiar resultados.
''',encoding='utf-8')
    bridge_names={'volumen':'Volumen valorado a precios base','mezcla':'Mezcla de productos','precio_lista':'Precio de lista medio','descuentos':'Descuento medio por unidad','costo_unitario':'Costo unitario','gastos_operacionales':'Gastos operacionales'}
    lines=['# Financial Performance Intelligence','', '**Diagnóstico de rentabilidad, control presupuestario y escenarios de decisión.**','',
        '## Enfoque y herramientas','', 'El proyecto transforma una pregunta de gerencia en un análisis reproducible: definir hipótesis, validar datos, localizar cambios por categoría, producto y cliente, cuantificar efectos y proponer acciones. SQL agrega la evidencia financiera; Python automatiza controles y descomposición; un dashboard interactivo y una presentación ejecutiva comunican los resultados.','',
        '## Decisión y resultado','', 'Los ingresos suben de $100M a $108M, pero la utilidad operacional baja de $20M a $17M. El costo de ventas sube $10M y los gastos $1M. El margen bruto disminuye $2M. La utilidad operacional es posterior a depreciación y no equivale a EBITDA.','',
        '## Descomposición de la caída','',table(['Factor','Efecto CLP aproximado'],[(bridge_names[k],pesos(v)) for k,v in bridge.items()]),'',
        'La suma sin redondear es exactamente -$3.000.000. El anexo define el orden y las fórmulas. Las cifras unitarias también reflejan calibración del generador.','',
        '## Categorías','',table(['Categoría','Margen agosto','Margen septiembre','Cambio'],[(r['categoria'],pesos(r['margen_agosto']),pesos(r['margen_septiembre']),pesos(r['delta'])) for r in sorted(categories,key=lambda r:r['delta'])]),'',
        'Organización, Escritura y Papel pierden margen absoluto. Tecnología e Impresión compensan parte de esa caída. La venta se desplaza hacia categorías con menor margen porcentual. Esto concilia la localización del cambio, sin sumar los cambios por categoría otra vez al puente.','',
        f'## Productos prioritarios: {covered/loss:.1%} de contribuciones negativas','',
        table(['Producto','Cambio de margen'],[(p['nombre'],pesos(p['delta'])) for p in chosen]+[('Otros productos con contribución negativa',pesos(-(loss-covered))),('Compensaciones de productos con mayor margen',pesos(sum(p['delta'] for p in products if p['delta']>0)))]),'',
        '## Gastos operacionales','',table(['Cuenta','Agosto','Septiembre','Aumento / disminución'],[(a['cuenta'],pesos(a['agosto']),pesos(a['septiembre']),pesos(a['delta'])) for a in sorted(accounts,key=lambda a:-a['delta'])]),'',
        '## Presupuesto frente a real','']
    for b in bva[-2:]:
        lines += ['### '+b['mes'],'',table(['Indicador','Plan','Real','Real − plan'],[(k,pesos(b['presupuesto'][k]),pesos(b['real'][k]),pesos(b['real'][k]-b['presupuesto'][k])) for k in ['ingresos','costos','gastos','utilidad']]),'']
    lines += ['## Cajas archivo pack frente a presupuesto: enero a septiembre','',table(['Mes','Packs reales / plan','Margen real','Margen plan','Desviación de margen'],[(r['mes'],str(r['unidades'])+' / '+str(r['plan']['unidades']),pesos(r['margen']),pesos(r['plan']['margen']),pesos(r['margen']-r['plan']['margen'])) for r in case_months]),'',
        'El producto supera en septiembre el plan de unidades netas (293 frente a 257), pero queda bajo el margen planificado. La caída mensual frente a agosto y la desviación frente al presupuesto responden a referencias distintas: no confundirlas. El presupuesto no existe por cliente, por lo que no se inventa una asignación de metas individuales.','',
        '### Comparación de Cajas archivo pack por canal','',table(['Mes','Canal','Packs real / plan','Margen real','Margen plan'],[(r['mes'],r['canal'],str(r['unidades'])+' / '+str(r['plan_unidades']),pesos(r['margen']),pesos(r['plan_margen'])) for r in case_channels]),'',
        '### Clientes con mayor caída de margen de este producto','',table(['Cliente ficticio','Packs agosto / septiembre','Margen agosto','Margen septiembre','Cambio'],[(r['cliente'],str(r['unidades_agosto'])+' / '+str(r['unidades_septiembre']),pesos(r['margen_agosto']),pesos(r['margen_septiembre']),pesos(r['delta'])) for r in sorted(client_comparison,key=lambda r:r['delta'])[:8]]),'',
        'La suma de cambios de todos los clientes concilia exactamente con -$1.174.888 del producto. Hay clientes que compensan parte de la caída; el detalle completo está en resultados_finales.json y en el dashboard.','',
        '## Investigación de Cajas archivo pack','',
        'Su margen cae $1.174.888. Las unidades netas bajan de 487 a 293: 152 packs menos de venta bruta y 42 packs adicionales devueltos. Los 29 clientes con reducción siguen comprando otros productos. Las tres devoluciones de septiembre revierten $145.397 de margen ya incluido en el neto. Septiembre tiene la segunda menor venta bruta de enero-septiembre y la mayor tasa de devolución (12,54%). El historial no demuestra normalidad estadística ni causas de no compra.','',
        '## Acciones propuestas','',
        '1. Comercial: piloto de recompra de productos prioritarios con clientes activos que redujeron unidades. Revisar necesidad y disponibilidad antes de ofrecer incentivos. Esfuerzo medio. Riesgo: recompra no recurrente o canibalización. Medir unidades netas y margen por producto, no solo facturación.','',
        '2. Comercial y Finanzas: revisar autorización de descuentos en canal directo. Esfuerzo medio. Riesgo: una reducción de descuentos puede afectar la demanda. Evaluar con piloto, margen unitario y retención. No confundir los efectos de calibración con una política comercial real.','',
        '3. Operaciones y Finanzas: revisar el incremento de Logística y Marketing y registrar causas de devoluciones. Esfuerzo bajo/medio. Riesgo: recortes que deterioren servicio o ventas. Aprobar ahorro después de identificar partidas evitables. La reducción de devoluciones no añade un beneficio independiente a estos escenarios.','',
        '## Escenarios de un mes equivalente a septiembre','',
        table(['Escenario','Volumen','Descuentos','Gastos','Costo supuesto de ejecución','Mejora neta','Utilidad simulada'],[(s['nombre'],pesos(s['volumen']),pesos(s['descuentos']),pesos(s['gastos']),pesos(s['costo_ejecucion']),pesos(s['impacto_neto']),pesos(s['utilidad_simulada'])) for s in scenarios]),'',
        'Prudente/base recuperan 5%/10% de la brecha de unidades seleccionadas, reducen descuentos en 0,5/1 punto de lista directa y ahorran 5%/10% del incremento de Logística y Marketing. Se mantienen los demás factores. Todos son supuestos, no mejoras obtenidas. El anexo explica bases, interacción omitida y seguimiento.','',
        '## Entrega y límites','',
        'La versión analítica cierra con informe, anexo, dashboard local de tres vistas, resultados estructurados y consultas reproducibles. El dashboard es HTML autónomo, no un archivo Power BI. La implementación nativa en Power BI queda como adaptación tecnológica posterior. La presentación ejecutiva acompaña el informe. No se publica en GitHub durante esta entrega.','',
        'Nota metodológica: el caso utiliza datos sintéticos documentados. No contamos con evidencia externa para explicar motivos de no compra o devolución. El proyecto entrega un diagnóstico financiero verificado, hipótesis pendientes y propuestas de decisión. La fase de implementación y medición empresarial queda diseñada, no ejecutada.']
    (OUT/'INFORME_FINAL.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    build_dashboard(data)
    audit=dict(estado='OK',controles=['60 agregados producto-mes','Identidad por cada producto con aritmética exacta','Puente margen -2000000 exacto','Puente utilidad -3000000 exacto','Cuentas de gasto +1000000','Presupuesto agregado antes de comparación'],sha256_bd=hashlib.sha256((OUT/'financial_performance.sqlite').read_bytes()).hexdigest())
    (OUT/'validacion_cierre.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(puente=data['bridge'],gastos=accounts,presupuesto=bva[-2:],escenarios=scenarios,cobertura=data['cobertura']),ensure_ascii=True,indent=2))
    c.close()


def build_dashboard(data):
    template=(ROOT/'04_python/dashboard_template.html').read_text(encoding='utf-8')
    (OUT/'dashboard.html').write_text(template.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')

if __name__=='__main__': main()
