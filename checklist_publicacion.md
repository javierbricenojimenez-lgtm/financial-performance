# Puerta de revisión antes de publicar proyectos

Aplicar a cada entrega y repetir si cambian archivos, datos, formatos o destino. No equivale a garantía absoluta ni sustituye la revisión del repositorio y su historial.

## 1. Definir qué se comparte

Preparar una selección explícita de entregables, documentación y código. Excluir carpetas temporales, perfiles de navegador, capturas internas, cachés, credenciales y archivos de configuración privados. Revisar el contenido real del ZIP, no solo el .gitignore.

## 2. Privacidad y derecho de uso

Confirmar origen y permisos de los datos. Revisar nombres, correos, teléfonos, identificadores personales, datos laborales y comerciales. En esta entrega, la fuente coincide con el generador sintético y todos los clientes tienen nombres ficticios. No incluir datos reales de un empleador sin autorización.

## 3. Secretos y metadatos

Buscar tokens, claves privadas, contraseñas, cadenas de conexión y rutas personales. Revisar autor, última persona que modificó, notas, comentarios, propiedades y capturas de documentos. Si aparece una credencial real, retirarla del paquete y revocarla; borrarla del archivo actual no elimina su presencia en el historial.

## 4. Formatos y contenido activo

- SQLite: inventariar tablas, vistas y triggers; revisar esquema y valores. No cargar extensiones de procedencia desconocida.
- Excel, cuando exista: revisar todas las hojas, incluidas ocultas, comentarios, nombres definidos, vínculos, conexiones externas, Power Query, objetos incrustados y VBA. Preferir .xlsx sin macros cuando no sean necesarias. En CSV/Excel, tratar como texto los campos no confiables que puedan interpretarse como fórmulas.
- PowerPoint: revisar relaciones externas, metadatos, notas, macros, ActiveX y objetos incrustados.
- HTML: revisar scripts, llamadas de red, formularios, enlaces y ausencia de secretos. El dashboard de esta entrega funciona localmente y no carga scripts externos ni hace llamadas de red explícitas.

## 5. Calidad y viabilidad

Conciliar resultados, verificar filtros y escenarios, comprobar que no existan dependencias de rutas privadas y documentar requisitos. Distinguir mejoras estimadas de resultados implementados. Acompañar datos de instrucciones y límites.

## 6. Revisión del destino antes de subir

Revisar repositorio exacto, visibilidad, archivos preparados para commit, identidad y correo del autor de Git, y el historial que se expondrá. Usar correo privado de GitHub si así lo prefiere el usuario. No depender de .gitignore para archivos ya versionados. No subir el directorio general de Proyectos.

## 7. Comprobar después de publicar

Inspeccionar el repositorio como visitante, verificar archivos descargables, documentación y ausencia de material interno. Conservar un inventario y huella del paquete revisado. Si se detecta una exposición, detener distribución y ejecutar la corrección correspondiente.

## Resultado actual

Publicación aún no realizada. `04_python/revisar_publicacion.py` ejecuta controles estáticos del paquete local y guarda `outputs/REVISION_PUBLICACION.json`. La revisión de identidad Git, permisos, visibilidad e historial se completa cuando se prepare el repositorio. Esta entrega no incluye Excel. Las revisiones específicas de Excel se aplicarán si se agrega uno.
