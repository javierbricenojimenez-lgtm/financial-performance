# Financial Performance Intelligence

**¿Por qué una empresa vende más, pero gana menos?**

Investigación de rentabilidad con SQL y Python: del estado de resultados al margen por producto y cliente, con presupuesto, escenarios de decisión y dashboard ejecutivo.

## Qué demuestra este proyecto

- Traducir una pregunta de gerencia en hipótesis, datos e indicadores.
- Localizar y cuantificar una caída de utilidad de $3 millones, conciliando ingresos, costos y gastos.
- Investigar productos y clientes sin confundir ventas brutas, devoluciones y ventas netas.
- Detectar que cumplir una meta de unidades no garantiza cumplir la de margen.
- Evaluar propuestas con supuestos explícitos y comunicar decisiones mediante dashboard e informe.

SQL organiza la evidencia; Python automatiza la generación, validación y descomposición financiera; el dashboard permite explorar resultados; la presentación comunica hallazgos y acciones. El caso utiliza datos sintéticos documentados.

Proyecto de aprendizaje y portafolio con datos sintéticos. Estado: versión analítica 1 terminada y verificada. Repositorio público publicado en GitHub; la implementación empresarial queda pendiente.

## Entrega final

- [Informe ejecutivo](outputs/INFORME_FINAL.md).
- [Dashboard local de tres vistas](outputs/dashboard.html): en GitHub usa **Download raw file**, guarda exactamente `dashboard.html` y ábrelo con Chrome o Edge. GitHub no ejecuta HTML directamente; no confundas este archivo con la base SQLite, el ZIP o la presentación.
- [Presentación editable de nueve diapositivas](outputs/presentacion_ejecutiva.pptx).
- [Método y límites](outputs/ANEXO_METODOLOGICO.md).
- [Guion de exposición](outputs/GUIA_PRESENTACION.md).
- [Auditoría de consistencia contra la base](outputs/AUDITORIA_CONSISTENCIA.md).
- [Revisión previa de publicación](outputs/REVISION_PUBLICACION.json).
- [Paquete final](outputs/proyecto_financial_performance_v1.zip).

La utilidad operacional cae $3M frente a agosto y $5,73M frente al presupuesto de septiembre. Cajas archivo pack supera su plan de unidades, pero queda bajo su margen previsto. No existe presupuesto por cliente. Las hipótesis de comportamiento comercial requieren datos externos.

## Reproducir datos y análisis

Requiere Python >=3.11 y SQLite >=3.37. No necesita paquetes externos para estos dos pasos:

```text
python 04_python/generar_datos.py
python 04_python/cerrar_analisis.py
python 04_python/auditar_consistencia.py
```

Los scripts reemplazan sus salidas generadas. El segundo crea el informe, anexo, resultados JSON y dashboard desde la base local. Las consultas 002 a 010 documentan las investigaciones intermedias. La presentación usa los resultados de la entrega final y debe actualizarse aparte si se regeneran datos con otra configuración. El constructor está en 04_python/presentacion.mjs y requiere el runtime Artifact Tool de Codex.

## Alcance tecnológico y límites

La entrega utiliza SQL, Python, dashboard HTML autónomo y PowerPoint editable. No incluye archivo PBIX ni libro Excel: la adaptación nativa a Power BI o Excel queda fuera de esta versión. Tampoco afirma mejoras implementadas o causas comerciales que los datos no permitan demostrar.

La generación calibra los totales financieros mensuales y modifica los precios y costos observados. El anexo describe sus efectos y limita la interpretación causal. Este repositorio demuestra metodología y reproducibilidad en un caso sintético.

## Problema

Explicar por qué los ingresos aumentaron de $100 a $108 millones mientras la utilidad operacional disminuyó de $20 a $17 millones entre agosto y septiembre de 2025. Apoyar decisiones sobre precios, descuentos, mezcla, costos y gastos.

## Alcance

Empresa comercial ficticia de productos de oficina en Chile; enero a septiembre de 2025; CLP sin IVA; canales directo y online. Propuesta inicial: 30 productos, 100 clientes y aproximadamente 10.000 líneas de operaciones. Estas cantidades son parámetros de diseño, no datos observados.

| Meta de conciliación (CLP) | Agosto | Septiembre |
|---|---:|---:|
| Ingreso neto | 100000000 | 108000000 |
| Costo de ventas | 60000000 | 70000000 |
| Gastos operacionales | 20000000 | 21000000 |
| Utilidad operacional | 20000000 | 17000000 |

## Documentación

- `00_gestion/diccionario_datos.md`: campos, granularidad y relaciones.
- `00_gestion/reglas_validacion.md`: reglas y condiciones para cargar datos.
- `03_sql/001_esquema.sql`: estructura SQLite, sin datos.
- `04_python/generar_datos.py`: generador reproducible, carga y controles.
- `01_datos_originales/datos_sinteticos.json`: fuente sintética inicial.
- `outputs/financial_performance.sqlite`: base poblada, con vistas de consulta.
- `outputs/LEEME_DATOS.md`: resumen, reglas y limitaciones del conjunto.
- `outputs/manifiesto_validacion.json`: conteos, semilla, huella y controles.
- `outputs/proyecto_financial_performance_v1.zip`: paquete auditado de datos y documentación.

## Secuencia de trabajo

1. Diseño de datos: documentado en esta versión.
2. Crear generador reproducible y datos sintéticos, documentando los efectos introducidos.
3. Cargar datos y ejecutar controles de calidad y conciliación.
4. Analizar hipótesis con SQL y verificar los cálculos.
5. Preparar dashboard, escenarios e informe ejecutivo.

## Decisiones de diseño

- Importes enteros en pesos; descuentos como importe, no porcentaje.
- Cantidades enteras; cada producto tiene una unidad de venta fija.
- Ventas y devoluciones almacenan magnitudes positivas. El tipo de operación determina el signo analítico.
- Cada devolución identifica la línea original y revierte su precio neto y costo proporcionalmente.
- El presupuesto es mensual, versión inicial fija, sin detalle por cliente.
- No se incluyen compras ni proveedores: no se atribuirán cambios de costo a proveedores sin incorporar evidencia adicional.
- SQLite será la base local. Las salidas para Power BI se prepararán después de validar los datos.

