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
- Tener el archivo MODELS.zip (por separado) en el Escritorio con la estructura esperada (carpeta MODELS y subcarpetas ENTRADA, BOLETERÍA, OFICIOS (GRUPALES), etc.).
- Tener el archivo metadata.json (por separado) en la carpeta raíz del proyecto.

# Flujo de uso:
  1. Abrir la app (`main.RhinoApp`).
  2. Seleccionar Tribunal, Fiscalía y número de imputados.
  3. Presionar ACEPTAR para completar datos (se abren formularios: `gui.sections.exp_data_fields.exp_data_fields` → `gui.sections.assis_data_fields.assis_data_fields` → `gui.sections.imp_data_fields.imp_data_fields`).
  4. Una vez registrados los imputados, el botón EXPORTAR (llama a `export.export`) crea la carpeta en el Escritorio y procesa los .docx utilizando los metadatos suministrados y los datos ingresados.

# Salida generada
- Se crea una carpeta en el Escritorio con el año y número de expediente (ej. 2025-000123) que contiene:
  - ENTRADA
  - DECISIÓN
  - OFICIOS (GRUPALES)
  - BOLETAS (GRUPALES)
- También se usa la carpeta "Rhino" en Documentos como área temporal donde se extrae MODELS.zip.

# Licencia
- El proyecto está bajo GNU GPL v3: COPYING.

# Contacto
- davidcanchica69@gmail.com.