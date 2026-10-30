// Constructor para Artifact Session. Evidencia nativa editable.
export function build(presentation,D){
 const money=n=>new Intl.NumberFormat('es-CL',{maximumFractionDigits:0}).format(n);
 const million=n=>new Intl.NumberFormat('es-CL',{maximumFractionDigits:2}).format(n/1e6);
 function text(s,str,x,y,w,h,size=25,color='#203346',bold=false){let a=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=str;a.text.style={fontFamily:'Arial',fontSize:size,color,bold};return a;}
 function slide(title){let s=presentation.slides.items.length===1&&presentation.slides.items[0].shapes.items.length===0?presentation.slides.items[0]:presentation.slides.add();s.background.fill='#f8fafb';text(s,title,64,44,1152,100,38,'#132c43',true);text(s,'Caso sintético · CLP sin IVA · Agosto y septiembre de 2025',64,664,1090,30,16,'#536779');s.speakerNotes.text='Fuente: outputs/resultados_finales.json, consultas SQL y base SQLite sintética del proyecto. Método y límites: outputs/ANEXO_METODOLOGICO.md. No hay evidencia causal comercial externa.';return s;}
 function table(s,values,y=174,widths=null){const t=s.tables.add({rows:values.length,columns:values[0].length,left:64,top:y,width:1152,height:values.length*48,values,columnWidths:widths||undefined});for(let r=0;r<values.length;r++)for(let col=0;col<values[0].length;col++){let cell=t.getCell(r,col);cell.text.style={fontFamily:'Arial',fontSize:21,color:r===0?'#ffffff':'#203346',bold:r===0};cell.fill=r===0?'#132c43':r%2?'#ffffff':'#edf3f6';}return t;}
 let s=slide('Ventas +8 %, utilidad operacional −15 %');
 text(s,'Financial Performance Intelligence',64,190,1152,64,44,'#087e83',true);
 text(s,'Problema: explicar por qué la empresa vende más, pero obtiene menos utilidad.',64,290,1070,90,30);
 table(s,[['Indicador','Agosto','Septiembre'],['Ingresos','$100 M','$108 M'],['Margen bruto','$40 M','$38 M'],['Utilidad operacional','$20 M','$17 M']],410,[550,301,301]);
 s=slide('La caída de utilidad concilia exactamente en $3 M');
 table(s,[['Factor contable','Efecto'],['Mayores ingresos','+$8 M'],['Mayor costo de ventas','−$10 M'],['Mayores gastos operacionales','−$1 M'],['Cambio de utilidad','−$3 M']],170,[850,302]);
 text(s,'El puente por volumen, mezcla, precio, descuento y costo está en el anexo. Sus efectos unitarios incluyen calibración sintética.',64,470,1110,115,26);
 s=slide('Organización concentra la mayor pérdida de margen');
 table(s,[['Categoría','Cambio de margen M$'],...D.categories.sort((a,b)=>a.delta-b.delta).map(r=>[r.categoria,million(r.delta)])],165,[850,302]);
 text(s,'Tecnología e Impresión compensan parte de las pérdidas. Los productos prioritarios cubren el 81,3 % de los aportes negativos.',64,490,1110,108,26);
 s=slide('Cajas archivo pack combina menor venta y devoluciones');
 table(s,[['Indicador','Agosto','Septiembre'],['Packs vendidos antes de devoluciones','487','335'],['Packs devueltos','0','42'],['Packs netos','487','293'],['Margen bruto','$2.152.697','$977.809']],165,[650,251,251]);
 text(s,'Los 29 clientes con menor compra neta siguieron comprando otros productos. No hay evidencia de abandono total ni del motivo de no compra.',64,490,1110,108,26);
 s=slide('Más packs que el plan, menos margen que el plan');
 const cr=D.case_months.at(-1);table(s,[['Cajas archivo pack, septiembre','Plan','Real'],['Packs netos',money(cr.plan.unidades),money(cr.unidades)],['Ingresos',money(cr.plan.ingresos),money(cr.ingresos)],['Margen bruto',money(cr.plan.margen),money(cr.margen)]],170,[650,251,251]);
 text(s,'La caída frente a agosto y el incumplimiento del plan son comparaciones distintas. El presupuesto existe por producto y canal, no por cliente.',64,425,1110,100,27);
 s=slide('Septiembre queda $5,73 M bajo la utilidad presupuestada');
 const b=D.bva.at(-1);table(s,[['Empresa, septiembre M$','Plan','Real','Desviación'],...['ingresos','costos','gastos','utilidad'].map(k=>[k,million(b.presupuesto[k]),million(b.real[k]),million(b.real[k]-b.presupuesto[k])])],165,[550,200,200,202]);
 text(s,'Logística aumenta $873.300 y Marketing $561.407 frente a agosto. Otras cuentas compensan parte del aumento y los gastos totales suben $1 M.',64,460,1110,125,26);
 s=slide('Escenarios: mejora neta de $0,63 M a $1,21 M');
 table(s,[['Un mes equivalente a septiembre','Prudente','Base'],['Recuperar unidades perdidas','5 %','10 %'],['Reducir descuento directo sobre lista','0,5 pp','1 pp'],['Ahorrar incremento Logística / Marketing','5 %','10 %'],['Costo supuesto de ejecución','$100.000','$250.000'],['Mejora neta estimada',...D.scenarios.map(x=>'$'+money(x.impacto_neto))]],160,[650,251,251]);
 text(s,'Supuestos ilustrativos, con demanda restante constante. Sin doble conteo entre ventas existentes y recuperadas. No son resultados obtenidos.',64,520,1110,100,25);
 s=slide('Decisiones propuestas y evidencia pendiente');
 text(s,'Comercial: piloto de recompra en productos prioritarios. Medir unidades netas y margen, cuidando canibalización.',64,170,1120,95,28);
 text(s,'Comercial y Finanzas: revisar descuentos mediante piloto. Validar respuesta de demanda antes de extender.',64,285,1120,90,28);
 text(s,'Operaciones y Finanzas: revisar Logística y Marketing y registrar motivos de devolución.',64,395,1120,80,28);
 text(s,'Cierre: diagnóstico financiero conciliado y escenarios reproducibles. Stock, CRM y motivos de devolución quedan como evidencia pendiente. Implementación empresarial y publicación en GitHub quedan para después.',64,510,1120,115,24,'#536779');
 s=slide('Método y herramientas aplicados al problema');
 text(s,'SQL: relacionar ventas, productos y clientes. Comparar meses y presupuesto con reglas de negocio consistentes.',64,170,1120,95,28);
 text(s,'Python: automatizar controles, conciliar resultados y separar los efectos sobre la utilidad.',64,285,1120,90,28);
 text(s,'Dashboard: explorar categorías, productos, clientes y escenarios con indicadores verificables.',64,395,1120,80,28);
 text(s,'Comunicación ejecutiva: convertir los hallazgos en prioridades, escenarios y evidencia necesaria para decidir.',64,510,1120,100,28);
 for(const [i,page] of presentation.slides.items.entries())for(const shape of page.shapes.items){if(String(shape.text).includes('Caso sintético · CLP sin IVA'))shape.text=i===0?'Datos sintéticos documentados · CLP sin IVA · Agosto y septiembre de 2025':'Financial Performance Intelligence · CLP sin IVA · Agosto y septiembre de 2025';}
 return presentation;
}
