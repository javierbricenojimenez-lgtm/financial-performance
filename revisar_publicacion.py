"""Revisión estática del paquete propuesto. No publica ni muestra valores sensibles."""
from pathlib import Path
import zipfile, sqlite3, json, re, hashlib, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'
def main():
    checks=[]
    def add(name,passed,detail=''):
        checks.append(dict(control=name,resultado='OK' if passed else 'REVISAR',detalle=detail))
    package=OUT/'proyecto_financial_performance_v1.zip'
    with zipfile.ZipFile(package) as z:
        names=z.namelist()
        add('Integridad ZIP',z.testzip() is None)
        add('Sin rutas absolutas ni traversal en ZIP',all(not n.startswith(('/','\\')) and ':' not in n and '..' not in Path(n).parts for n in names))
        add('Sin carpetas internas o archivos de credenciales',not any(any(part.lower() in ['work','node_modules','.git','.aws','.codex','.agents'] for part in Path(n).parts) or Path(n).name.lower() in ['.env','id_rsa','id_ed25519','credentials','credentials.json'] or Path(n).suffix.lower() in ['.pem','.key','.p12','.pfx'] for n in names))
        patterns={
          'Llaves privadas':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
          'Tokens con formato conocido':r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|sk-proj-[A-Za-z0-9_-]{20,})',
          'Rutas personales de Windows':r'[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+',
          'Correos electrónicos':r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
          'Credenciales literales asignadas':r'''(?i)(?:password|api_key|access_token|client_secret)\s*[:=]\s*["'][^"']{8,}["']''',
        }
        textfiles=[n for n in names if Path(n).suffix.lower() in ['.md','.py','.sql','.mjs','.html','.json'] or n.endswith('.gitignore')]
        for label,pattern in patterns.items():
            findings=[n for n in textfiles if re.search(pattern,z.read(n).decode('utf-8',errors='replace'))]
            add(label+' en archivos de texto',not findings,'Archivos que requieren revisión: '+str(len(findings)))
    db=sqlite3.connect((OUT/'financial_performance.sqlite').as_uri()+'?mode=ro',uri=True)
    add('Integridad SQLite',db.execute('PRAGMA integrity_check').fetchone()[0]=='ok')
    clients=db.execute('SELECT nombre FROM clientes').fetchall()
    add('Todos los nombres de clientes siguen el patrón ficticio',len(clients)==100 and all(re.fullmatch('Empresa Ficticia [0-9]{3}',r[0]) for r in clients))
    schema=db.execute("SELECT name,type,sql FROM sqlite_master WHERE sql IS NOT NULL").fetchall()
    add('Sin triggers ni tablas virtuales en la base',all(r[1]!='trigger' and 'CREATE VIRTUAL TABLE' not in r[2].upper() for r in schema))
    add('Sin instrucciones de conexión externa en esquema',all(not re.search(r'(?i)load_extension|https?://|file:|ATTACH\s+DATABASE',r[2]) for r in schema))
    db.close()
    raw=json.loads((ROOT/'01_datos_originales/datos_sinteticos.json').read_text(encoding='utf-8'))
    from generar_datos import build
    rebuilt,_=build()
    add('Fuente idéntica al generador sintético reproducible',raw==rebuilt)
    with zipfile.ZipFile(OUT/'presentacion_ejecutiva.pptx') as p:
        nn=p.namelist()
        add('Presentación sin macros, ActiveX u objetos OLE',not any(re.search('(?i)vbaProject|activeX|embeddings/',n) for n in nn))
        external=[]; personal=[]
        for n in nn:
            if n.endswith('.rels'):
                root=ET.fromstring(p.read(n))
                external += [n for rel in root if rel.attrib.get('TargetMode')=='External']
            if n.endswith('.xml'):
                t=p.read(n).decode('utf-8',errors='replace')
                if re.search(patterns['Rutas personales de Windows'],t) or re.search(patterns['Correos electrónicos'],t):personal.append(n)
        add('Presentación sin relaciones externas',not external)
        add('Presentación sin rutas personales ni correos detectados',not personal)
        meta={}
        if 'docProps/core.xml' in nn:
            for e in ET.fromstring(p.read('docProps/core.xml')):
                if e.tag.split('}')[-1] in ['creator','lastModifiedBy']:
                    meta[e.tag.split('}')[-1]]=e.text or ''
        # Solo permitir campos de autor vacíos o del generador, sin datos de una persona.
        add('Autoría de metadatos sin nombre personal',all(v in ['', 'OpenAI','Artifact Tool','artifact-tool'] for v in meta.values()),'Campos de autor revisados: '+str(len(meta)))
    html=(OUT/'dashboard.html').read_text(encoding='utf-8')
    add('Dashboard sin scripts externos ni llamadas de red explícitas',not re.search(r'(?i)<script[^>]+src\s*=|fetch\s*\(|XMLHttpRequest|WebSocket|https?://',html))
    add('No se distribuyen Excel ni libros con macros',not any(Path(n).suffix.lower() in ['.xlsx','.xls','.xlsm','.xlsb'] for n in names))
    result=dict(estado='APTO_PARA_REVISION_FINAL' if all(c['resultado']=='OK' for c in checks) else 'REQUIERE_REVISION',sha256_paquete=hashlib.sha256(package.read_bytes()).hexdigest(),archivos=len(names),controles=checks,limite='Revisión estática del paquete local, no certificación de seguridad ni análisis antimalware. No incluye identidad Git/GitHub, permisos del repositorio, configuración de publicación ni historial de futuros commits.')
    (OUT/'REVISION_PUBLICACION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True,indent=2))
if __name__=='__main__':main()
