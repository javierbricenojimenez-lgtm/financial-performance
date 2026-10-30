"""Contraste independiente de entregables contra tablas base, sin usar vistas."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
import sqlite3,json,re,zipfile,hashlib,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'

def main():
 c=sqlite3.connect((OUT/'financial_performance.sqlite').as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
 data=json.loads((OUT/'resultados_finales.json').read_text(encoding='utf-8'))
 checks=[]
 def check(name,ok):
  checks.append(dict(control=name,resultado='OK' if ok else 'ERROR'))
  if not ok: raise AssertionError(name)
 products={r['producto_id']:dict(r) for r in c.execute('SELECT * FROM productos')}
 names={r['cliente_id']:r['nombre'] for r in c.execute('SELECT * FROM clientes')}
 pm=defaultdict(lambda:dict(unidades=0,ingresos=0,costos=0,bruto=0,descuentos=0,vendidos=0,devueltos=0))
 clients=defaultdict(lambda:dict(unidades=0,margen=0,brutos=0,devueltos=0)); client_activity=defaultdict(set)
 for r in c.execute('SELECT * FROM ventas'):
  month=r['fecha'][:7];pid=r['producto_id'];sgn=1 if r['tipo_operacion']=='VENTA' else -1
  gross=r['cantidad']*r['precio_lista_unitario']; net=gross-r['descuento_importe']; cost=r['costo_ventas_importe']
  check('Línea '+str(r['linea_id'])+': ingreso generado',net==r['ingreso_neto_importe'])
  p=pm[pid,month]
  for k,value in dict(unidades=r['cantidad'],ingresos=net,costos=cost,bruto=gross,descuentos=r['descuento_importe']).items():p[k]+=sgn*value
  p['vendidos' if sgn==1 else 'devueltos']+=r['cantidad']
  q=clients[r['cliente_id'],pid,month];q['unidades']+=sgn*r['cantidad'];q['margen']+=sgn*(net-cost);q['brutos' if sgn==1 else 'devueltos']+=r['cantidad']
  if sgn==1:client_activity[r['cliente_id'],month].add(pid)
 em=defaultdict(int); am=defaultdict(int)
 for r in c.execute('SELECT * FROM gastos'):
  val=r['importe']*(1 if r['tipo_movimiento']=='GASTO' else -1);em[r['fecha'][:7]]+=val;am[r['cuenta'],r['fecha'][:7]]+=val
 plan=defaultdict(lambda:dict(unidades=0,ingresos=0,costos=0)); plan_channel={}
 for r in c.execute('SELECT * FROM presupuesto_comercial'):
  p=plan[r['producto_id'],r['mes'][:7]]
  for k,col in [('unidades','unidades_netas'),('ingresos','ingresos_netos'),('costos','costo_ventas')]:p[k]+=r[col]
  plan_channel[r['producto_id'],r['mes'][:7],r['canal']]=dict(r)
 pe=defaultdict(int)
 for r in c.execute('SELECT * FROM presupuesto_gastos'):pe[r['mes'][:7]]+=r['importe']
 months=[f'2025-{i:02d}' for i in range(1,10)]
 for row in data['monthly']:
  m=row['mes']; rev=sum(pm[p,m]['ingresos'] for p in products);cost=sum(pm[p,m]['costos'] for p in products)
  check('Estado de resultados '+m, all(row[k]==v for k,v in dict(ingresos=rev,costo_ventas=cost,margen_bruto=rev-cost,gastos=em[m],utilidad_operacional=rev-cost-em[m]).items()))
  check('Ratio operacional '+m,abs(row['margen_operacional']-float(F(rev-cost-em[m],rev)))<1e-12)
 for p in data['products']:
  for col,m in [('agosto','2025-08'),('septiembre','2025-09')]:
   check('Producto '+str(p['id'])+' '+m,all(p[col][k]==pm[p['id'],m][k] for k in ['unidades','ingresos','costos','bruto','descuentos']))
  a,b=pm[p['id'],'2025-08'],pm[p['id'],'2025-09']
  check('Margen producto '+str(p['id']),p['delta']==b['ingresos']-b['costos']-a['ingresos']+a['costos'])
 for r in data['categories']:
  ids=[p for p in products if products[p]['categoria']==r['categoria']]
  for col,m in [('agosto','2025-08'),('septiembre','2025-09')]:
   check('Categoría '+r['categoria']+' '+m,r['margen_'+col]==sum(pm[p,m]['ingresos']-pm[p,m]['costos'] for p in ids) and r['ingresos_'+col]==sum(pm[p,m]['ingresos'] for p in ids))
 for r in data['accounts']:check('Gastos '+r['cuenta'],r['agosto']==am[r['cuenta'],'2025-08'] and r['septiembre']==am[r['cuenta'],'2025-09'] and r['delta']==r['septiembre']-r['agosto'])
 for r in data['bva']:
  m=r['mes'];rev=sum(plan[p,m]['ingresos'] for p in products);cost=sum(plan[p,m]['costos'] for p in products)
  check('Presupuesto '+m,r['presupuesto']==dict(ingresos=rev,costos=cost,gastos=pe[m],utilidad=rev-cost-pe[m]))
  check('Real en presupuesto '+m,r['real']==dict(ingresos=sum(pm[p,m]['ingresos'] for p in products),costos=sum(pm[p,m]['costos'] for p in products),gastos=em[m],utilidad=sum(pm[p,m]['ingresos']-pm[p,m]['costos'] for p in products)-em[m]))
 for r in data['case_months']:
  m=r['mes'];p=pm[17,m]
  check('Packs reales y devoluciones '+m,all(r[k]==p[k] for k in ['unidades','ingresos','costos','vendidos','devueltos']) and r['margen']==p['ingresos']-p['costos'] and p['unidades']==p['vendidos']-p['devueltos'])
  check('Packs presupuesto '+m,all(r['plan'][k]==plan[17,m][k] for k in ['unidades','ingresos','costos']) and r['plan']['margen']==plan[17,m]['ingresos']-plan[17,m]['costos'])
 for r in data['client_comparison']:
  cid=next(k for k,v in names.items() if v==r['cliente']); a,b=clients[cid,17,'2025-08'],clients[cid,17,'2025-09']
  check('Cliente '+str(cid),r['unidades_agosto']==a['unidades'] and r['unidades_septiembre']==b['unidades'] and r['margen_agosto']==a['margen'] and r['margen_septiembre']==b['margen'] and r['delta']==b['margen']-a['margen'])
 lower=[cid for cid in names if clients[cid,17,'2025-08']['unidades']>clients[cid,17,'2025-09']['unidades']]
 check('29 clientes con reducción y actividad en otros productos',len(lower)==29 and all(client_activity[cid,'2025-09']-{17} for cid in lower))
 check('Clientes concilian con margen del producto',sum(r['delta'] for r in data['client_comparison'])==-1174888)
 # Puente exacto recalculado desde tablas base.
 a={p:pm[p,'2025-08'] for p in products};b={p:pm[p,'2025-09'] for p in products}
 P=lambda x,p:F(x[p]['ingresos'],x[p]['unidades'])
 C=lambda x,p:F(x[p]['costos'],x[p]['unidades'])
 m0=sum(a[p]['ingresos']-a[p]['costos'] for p in products)
 idx=sum(b[p]['unidades']*P(a,p) for p in products)/sum(a[p]['ingresos'] for p in products)
 bridge=dict(volumen=(idx-1)*m0,mezcla=sum((b[p]['unidades']-idx*a[p]['unidades'])*(P(a,p)-C(a,p)) for p in products),precio_lista=sum(b[p]['unidades']*(F(b[p]['bruto'],b[p]['unidades'])-F(a[p]['bruto'],a[p]['unidades'])) for p in products),descuentos=sum(-b[p]['unidades']*(F(b[p]['descuentos'],b[p]['unidades'])-F(a[p]['descuentos'],a[p]['unidades'])) for p in products),costo_unitario=sum(-b[p]['unidades']*(C(b,p)-C(a,p)) for p in products),gastos_operacionales=F(em['2025-08']-em['2025-09']))
 check('Puente exacto de utilidad',sum(bridge.values())==-3000000)
 check('Puente JSON coincide con recálculo independiente',all(abs(data['bridge'][k]-float(v))<1e-6 for k,v in bridge.items()))
 recover=sum(max(0,a[p]['unidades']-b[p]['unidades'])*(P(b,p)-C(b,p)) for p in products if b[p]['ingresos']-b[p]['costos']<a[p]['ingresos']-a[p]['costos'])
 gross_direct=sum((1 if r['tipo_operacion']=='VENTA' else -1)*r['cantidad']*r['precio_lista_unitario'] for r in c.execute("SELECT * FROM ventas WHERE fecha>='2025-09-01' AND canal='DIRECTO'"))
 extra=sum(max(0,am[k,'2025-09']-am[k,'2025-08']) for k in ['Logística','Marketing'])
 for s in data['scenarios']:
  v=round(recover*F(str(s['recuperacion_packs_pct']))/100);d=round(gross_direct*F(str(s['reduccion_descuento_pp']))/100);g=round(extra*F(str(s['ahorro_incremento_gastos_pct']))/100)
  check('Escenario '+s['nombre'],s['volumen']==v and s['descuentos']==d and s['gastos']==g and s['impacto_neto']==v+d+g-s['costo_ejecucion'] and s['utilidad_simulada']==17000000+s['impacto_neto'])
 # El contenido del dashboard debe ser exactamente el mismo que los resultados auditados.
 page=(OUT/'dashboard.html').read_text(encoding='utf-8')
 embedded=json.loads(re.search(r'const D=(.*?);\nconst money',page,re.S).group(1))
 check('Datos embebidos del dashboard idénticos al conjunto auditado',embedded==data)
 # Tablas del informe: comprobar TODOS los valores mostrados contra resultados auditados.
 def money(n):return '$'+f'{round(n):,}'.replace(',','.')
 text=(OUT/'INFORME_FINAL.md').read_text(encoding='utf-8')
 def hasrow(values):return '| '+' | '.join(str(v) for v in values)+' |' in text
 for r in data['categories']:check('Informe categoría '+r['categoria'],hasrow([r['categoria'],money(r['margen_agosto']),money(r['margen_septiembre']),money(r['delta'])]))
 for r in data['accounts']:check('Informe gasto '+r['cuenta'],hasrow([r['cuenta'],money(r['agosto']),money(r['septiembre']),money(r['delta'])]))
 for r in data['bva'][-2:]:
  for k in ['ingresos','costos','gastos','utilidad']:check('Informe presupuesto '+r['mes']+' '+k,hasrow([k,money(r['presupuesto'][k]),money(r['real'][k]),money(r['real'][k]-r['presupuesto'][k])]))
 for r in data['case_months']:check('Informe packs '+r['mes'],hasrow([r['mes'],str(r['unidades'])+' / '+str(r['plan']['unidades']),money(r['margen']),money(r['plan']['margen']),money(r['margen']-r['plan']['margen'])]))
 for r in data['scenarios']:check('Informe escenario '+r['nombre'],hasrow([r['nombre'],money(r['volumen']),money(r['descuentos']),money(r['gastos']),money(r['costo_ejecucion']),money(r['impacto_neto']),money(r['utilidad_simulada'])]))
 # Presentación: leer tablas nativas OOXML, sin depender de previews ni del constructor.
 ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
 with zipfile.ZipFile(OUT/'presentacion_ejecutiva.pptx') as z:
  tables=[]
  for i in range(1,10):
   root=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
   tables.append([])
   native=[]
   for tab in root.findall('.//a:tbl',ns):native.append([[''.join(cell.findall('.//a:t',ns)[j].text or '' for j in range(len(cell.findall('.//a:t',ns)))) for cell in row.findall('a:tc',ns)] for row in tab.findall('a:tr',ns)])
   tables[-1]=native
  fmt=lambda n:f'{n:,}'.replace(',','.')
  mm=lambda n:format(n/1e6,'.2f').rstrip('0').rstrip('.').replace('.',',')
  expected={
   1:[['Indicador','Agosto','Septiembre'],['Ingresos','$100 M','$108 M'],['Margen bruto','$40 M','$38 M'],['Utilidad operacional','$20 M','$17 M']],
   2:[['Factor contable','Efecto'],['Mayores ingresos','+$8 M'],['Mayor costo de ventas','−$10 M'],['Mayores gastos operacionales','−$1 M'],['Cambio de utilidad','−$3 M']],
   3:[['Categoría','Cambio de margen M$']]+[[r['categoria'],mm(r['delta'])] for r in sorted(data['categories'],key=lambda x:x['delta'])],
   4:[['Indicador','Agosto','Septiembre'],['Packs vendidos antes de devoluciones','487','335'],['Packs devueltos','0','42'],['Packs netos','487','293'],['Margen bruto','$2.152.697','$977.809']],
   5:[['Cajas archivo pack, septiembre','Plan','Real'],['Packs netos','257','293'],['Ingresos','3.533.334','1.868.352'],['Margen bruto','1.625.334','977.809']],
   6:[['Empresa, septiembre M$','Plan','Real','Desviación']]+[[k,mm(data['bva'][-1]['presupuesto'][k]),mm(data['bva'][-1]['real'][k]),mm(data['bva'][-1]['real'][k]-data['bva'][-1]['presupuesto'][k])] for k in ['ingresos','costos','gastos','utilidad']],
   7:[['Un mes equivalente a septiembre','Prudente','Base'],['Recuperar unidades perdidas','5 %','10 %'],['Reducir descuento directo sobre lista','0,5 pp','1 pp'],['Ahorrar incremento Logística / Marketing','5 %','10 %'],['Costo supuesto de ejecución','$100.000','$250.000'],['Mejora neta estimada']+[money(r['impacto_neto']) for r in data['scenarios']]]}
  for i,rows in expected.items():check('Tabla completa de presentación '+str(i),len(tables[i-1])==1 and tables[i-1][0]==rows)
  check('Presentación sin macros y con 9 diapositivas',not any('vbaProject' in n for n in z.namelist()) and len([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)])==9)
 # Contrastar las tablas de las notas históricas, no solo el informe final.
 def rows_of(filename):
  lines=(OUT/filename).read_text(encoding='utf-8').splitlines()
  rr=[[v.strip() for v in line.strip().strip('|').split('|')] for line in lines if line.startswith('|')]
  return [row for row in rr[1:] if not all(re.fullmatch(r':?-+:?',v) for v in row)]
 for row in rows_of('01_exploracion_categorias.md'):
  if row[0]=='Total':vals=[40000000,38000000,-2000000]
  else:
   r=next(r for r in data['categories'] if r['categoria']==row[0]);vals=[r['margen_agosto'],r['margen_septiembre'],r['delta']]
  check('Nota 01 '+row[0],list(map(int,row[1:]))==vals)
 for row in rows_of('02_organizacion_productos.md'):
  if row[0]=='Total':vals=[8531993,4041072,-4490921]
  else:
   r=next(p for p in data['products'] if p['nombre']==row[0]);vals=[r['margen_agosto'],r['margen_septiembre'],r['delta']]
  check('Nota 02 '+row[0],list(map(int,row[1:]))==vals)
 case_a,case_b=pm[17,'2025-08'],pm[17,'2025-09']
 metric_values=[(case_a['unidades'],case_b['unidades']),(case_a['ingresos'],case_b['ingresos']),(case_a['costos'],case_b['costos']),(case_a['ingresos']-case_a['costos'],case_b['ingresos']-case_b['costos']),(round(P(a,17)),round(P(b,17))),(round(C(a,17)),round(C(b,17)))]
 for row,vals in zip(rows_of('03_cajas_archivo_comparacion.md'),metric_values):check('Nota 03 '+row[0],list(map(int,row[1:]))==list(vals))
 effect_values=[(case_b['unidades']-case_a['unidades'])*(P(a,17)-C(a,17)),case_b['unidades']*(P(b,17)-P(a,17)),-case_b['unidades']*(C(b,17)-C(a,17)),F(-1174888)]
 for row,val in zip(rows_of('04_puente_cajas_archivo.md'),effect_values):check('Nota 04 '+row[0],int(row[-1])==round(val))
 groups=[[],[],[],[],[]]
 for cid in names:
  aa,bb=clients[cid,17,'2025-08']['unidades'],clients[cid,17,'2025-09']['unidades']
  if not aa and not bb:continue
  group=0 if aa>0 and bb==0 else 1 if aa>bb else 2 if aa==bb else 3 if aa>0 else 4
  groups[group].append((aa,bb))
 totals=[]
 for group in groups:totals.append([len(group),sum(x[0] for x in group),sum(x[1] for x in group),sum(x[1]-x[0] for x in group)])
 totals.append([sum(x[i] for x in totals) for i in range(4)])
 for row,vals in zip(rows_of('05_cajas_clientes.md'),totals):check('Nota 05 '+row[0],list(map(int,row[1:]))==vals)
 sales=[dict(r) for r in c.execute('SELECT * FROM ventas')]
 for row,m in zip(rows_of('06_cliente_017_historial.md'),months):
  rr=[r for r in sales if r['cliente_id']==17 and r['fecha'].startswith(m)]
  docs=len({r['documento_id'] for r in rr if r['tipo_operacion']=='VENTA'})
  revenue=sum((r['cantidad']*r['precio_lista_unitario']-r['descuento_importe'])*(1 if r['tipo_operacion']=='VENTA' else -1) for r in rr)
  check('Nota 06 '+m,list(map(int,row[1:]))==[docs,revenue,clients[17,17,m]['unidades']])
 for row in rows_of('07_clientes_con_reduccion.md'):
  cid=int(row[0]);frequency=len({r['fecha'][:7] for r in sales if r['cliente_id']==cid and r['producto_id']==17 and r['tipo_operacion']=='VENTA' and r['fecha']<'2025-09-01'})
  other_docs=len({r['documento_id'] for r in sales if r['cliente_id']==cid and r['producto_id']!=17 and r['tipo_operacion']=='VENTA' and r['fecha']>='2025-09-01'})
  check('Nota 07 '+row[0],list(map(int,row[1:]))==[clients[cid,17,'2025-08']['unidades'],clients[cid,17,'2025-09']['unidades'],frequency,other_docs])
 for row,key in zip(rows_of('08_cajas_ventas_devoluciones.md'),['vendidos','devueltos','unidades']):check('Nota 08 '+key,list(map(int,row[1:]))==[case_a[key],case_b[key],case_b[key]-case_a[key]])
 for row,m in zip(rows_of('09_cajas_historial_mensual.md'),months):
  r=pm[17,m];rate=round(100*r['devueltos']/r['vendidos'],2)
  check('Nota 09 '+m,list(map(int,row[1:4]))==[r['vendidos'],r['devueltos'],r['unidades']] and abs(float(row[4].replace('%','').replace(',','.'))-rate)<1e-9)
 returned=[r for r in sales if r['producto_id']==17 and r['tipo_operacion']=='DEVOLUCION' and r['fecha']>='2025-09-01']
 for row in rows_of('10_cierre_exploracion_devoluciones.md'):
  if row[0]=='Total':check('Nota 10 total',int(row[3])==sum(r['cantidad'] for r in returned) and int(row[4])==sum(r['ingreso_neto_importe']-r['costo_ventas_importe'] for r in returned))
  else:
   r=next(r for r in returned if r['documento_id']==row[2]);check('Nota 10 documento '+row[2],int(row[0])==r['cliente_id'] and row[1]==r['fecha'] and int(row[3])==r['cantidad'] and int(row[4])==r['ingreso_neto_importe']-r['costo_ventas_importe'])
 # Ratio corregido: redondear solo al mostrar, nunca truncar.
 low=[p for p in products if products[p]['categoria'] not in ['Tecnología','Insumos de impresión']]
 for m,col in [('2025-08','agosto'),('2025-09','septiembre')]:
  ratio=100*sum(pm[p,m]['ingresos']-pm[p,m]['costos'] for p in low)/sum(pm[p,m]['ingresos'] for p in low)
  formatted=format(ratio,'.2f').replace('.',',')+'%'
  check('Ratio categorías restantes '+m,formatted in (OUT/'01_exploracion_categorias.md').read_text(encoding='utf-8'))
 c.close()
 # No afirmar controles sobre archivos que no fueron contrastados.
 summary=dict(estado='OK',controles=len(checks),lineas_verificadas=9870,sha256_base=hashlib.sha256((OUT/'financial_performance.sqlite').read_bytes()).hexdigest(),verificaciones=checks,alcance='Tablas base frente a resultados estructurados, estados mensuales, presupuesto, productos, clientes, cuentas, puente, escenarios, datos del dashboard, tablas del informe y 7 tablas nativas de la presentación. Redondeo explícito en visuales. No certifica causas comerciales ni realización futura de escenarios.')
 (OUT/'AUDITORIA_CONSISTENCIA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:summary[k] for k in ['estado','controles','lineas_verificadas']},ensure_ascii=False))

if __name__=='__main__':main()
