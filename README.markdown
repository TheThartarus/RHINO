# README (es)

# Descripción
- Este programa facilita la creación de la boletería de los expedientes de guardia (diseñado para el Circuito Judicial Penal de los Valles del Tuy). Genera una estructura de carpetas y documentos a partir de plantillas (MODELS.zip) y rellena los .docx con los datos ingresados desde la interfaz gráfica.

# Requisitos
- Python 3.8+ (probado con Python 3.x).
- Dependencias Python:
  - docx
  - tkinter
  - datetime
  - shutil
  - os
  - zipfile
  - json
  - sys
  - re
- Tener un archivo MODELS.zip en el Escritorio con la estructura esperada (carpeta MODELS y subcarpetas ENTRADA, BOLETERÍA, OFICIOS (GRUPALES), etc.).
- metadata.json debe estar en la raíz del proyecto (ya incluido en el repo).

# Flujo de uso:
  1. Abrir la app (`main.RhinoApp`).
  2. Seleccionar Tribunal, Fiscalía y número de imputados.
  3. Presionar ACEPTAR para completar datos (se abren formularios: `gui.sections.exp_data_fields.exp_data_fields` → `gui.sections.assis_data_fields.assis_data_fields` → `gui.sections.imp_data_fields.imp_data_fields`).
  4. Una vez registrados los imputados, el botón EXPORTAR (llama a `export.export`) crea la carpeta en el Escritorio y procesa los .docx con metadata y los datos ingresados.

# Salida generada
- Se crea una carpeta en el Escritorio con nombre YEAR-<número_expediente> (ej. 2025-123) que contiene:
  - ENTRADA (documentos procesados)
  - OFICIOS (GRUPALES)
  - BOLETERÍA (carpetas por imputado, cada una con documentos procesados)
- También se usa la carpeta "Rhino" en Documentos como área temporal donde se extrae MODELS.zip.

Notas técnicas y consideraciones
- La función de export utiliza distintas codificaciones al leer metadata.json para tolerancia a BOM y codificaciones comunes.
- La búsqueda del índice del imputado para los documentos de BOLETERÍA se realiza ascendiendo la jerarquía de carpetas buscando el patrón "N - NOMBRE". Si no se puede determinar, el proceso aborta mostrando un error.
- Los reemplazos de texto en los .docx son realizados por run dentro de párrafos; imágenes/drawings se saltan.
- La interfaz usa variables Tkinter (`StringVar`) definidas en `database.Database` para compartir estado entre ventanas.

# Licencia
- El proyecto está bajo GNU GPL v3: COPYING.

# Contacto
- davidcanchica69@gmail.com.