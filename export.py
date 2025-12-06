import tkinter as tk
from tkinter import messagebox
from docx import Document
from datetime import date
import shutil
import os
import zipfile
import json
import sys

from replacements.global_replacements import global_replacements
from replacements.single_acussed_replacements import single_acussed_replacements
from replacements.several_acusseds_replacements import several_acusseds_replacements
from replacements.decision_replacements import decision_replacements
from replacements.tribunals_replacements import tribunals_replacements

import data

def export(self):
    today_date = date.today()

    group_folders_names = ["ENTRADA",
                          "OFICIOS (GRUPALES)",
                          "BOLETAS (GRUPALES)"]

    month_names = ["", "enero", "febrero", "marzo",
                   "abril", "mayo", "junio",
                   "julio", "agosto", "septiembre",
                   "octubre", "noviembre", "diciembre"]

    IND_DAY = date(1811, 7, 5)
    ind_year_diff = today_date.year - IND_DAY.year
    FED_DAY = date(1859, 2, 20)
    fed_year_diff = today_date.year - FED_DAY.year
    REV_DAY = date(1999, 2, 2)
    rev_year_diff = today_date.year - REV_DAY.year

    year_diffs = {
        "ind": ind_year_diff,
        "fed": fed_year_diff,
        "rev": rev_year_diff
    }

    if (today_date.month,
        today_date.day) < (IND_DAY.month,
                           IND_DAY.day):
        ind_year_diff -= 1
    if (today_date.month,
        today_date.day) < (FED_DAY.month,
                           FED_DAY.day):
        fed_year_diff -= 1
    if (today_date.month,
        today_date.day) < (REV_DAY.month,
                           REV_DAY.day):
        rev_year_diff -= 1

    # Deshabilitar EXPORTAR mientras se crea el expediente
    self.export_button.config(state=tk.DISABLED)

    # Crear la carpeta Rhino en la carpeta Documentos si no existe
    user_documents = os.path.join(
        os.path.expanduser("~"),
        "Documents"
    )
    rhino_folder = os.path.join(
        user_documents,
        "Rhino"
    )
    os.makedirs(
        rhino_folder,
        exist_ok=True
    )

    # Extraer el archivo MODELS.zip en la carpeta Rhino
    try:
        user_desktop = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )
        zip_path = os.path.join(
            user_desktop,
            "MODELS.zip"
        )
        with zipfile.ZipFile(
            zip_path,
            'r'
        ) as zip_ref:
            zip_ref.extractall(rhino_folder)
    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "Archivo MODELS.zip no encontrado en el escritorio"
        )
        shutil.rmtree(rhino_folder)
        sys.exit()
    except zipfile.BadZipFile:
        messagebox.showerror(
            "Error",
            "Archivo MODELS.zip está dañado o no es un archivo zip válido"
        )
        shutil.rmtree(rhino_folder)
        sys.exit()

    # Crear carpeta del expediente en el escritorio
    expedient_name = str(today_date.year)+ "-" + data.exp_number
    expedient_folder = os.path.join(
        user_desktop,
        expedient_name
    )
    os.makedirs(
        expedient_folder,
        exist_ok=True
    )

    # Crear carpeta DECISIÓN en la carpeta del expediente
    ticket_folder = os.path.join(
        expedient_folder,
        "DECISIÓN"
    )
    os.makedirs(
        ticket_folder,
        exist_ok=True
    )

    # Copiar la carpeta ENTRADA a la carpeta del expediente
    decision_src = os.path.join(
        rhino_folder,
        "MODELS",
        "ENTRADA"
    )
    decision_dst = os.path.join(
        expedient_folder,
        "ENTRADA"
    )
    shutil.copytree(
        decision_src,
        decision_dst
    )

    # Copiar la carpeta OFICIOS (GRUPALES) a la carpeta del expediente
    offices_src = os.path.join(
        rhino_folder,
        "MODELS",
        "OFICIOS (GRUPALES)"
    )
    offices_dst = os.path.join(
        expedient_folder,
        "OFICIOS (GRUPALES)"
    )
    shutil.copytree(
        offices_src,
        offices_dst
    )

    # Copiar la carpeta BOLETAS (GRUPALES) a la carpeta del expediente
    tickets_src = os.path.join(
        rhino_folder,
        "MODELS",
        "BOLETAS (GRUPALES)"
    )
    tickets_dst = os.path.join(
        expedient_folder,
        "BOLETAS (GRUPALES)"
    )
    shutil.copytree(
        tickets_src,
        tickets_dst
    )

    # Crear carpetas para cada imputado en la carpeta DECISIÓN
    for i in range(data.n_acusseds):
        acussed_name = (data.acusseds_data[i]["name"]
                        .strip()
                        .upper()
                        .replace(" ", "_"))
        ticket_src = os.path.join(
            rhino_folder,
            "MODELS",
            "DECISIÓN"
        )
        # Prefijo con número y guión: "0 - NOMBRE"
        ticket_dst = os.path.join(
            ticket_folder,
            str(i)
            + " - "
            + acussed_name
        )
        shutil.copytree(
            ticket_src,
            ticket_dst
        )

    # Cargar metadata.json desde la carpeta del ejecutable / main.py
    if getattr(sys, 'frozen', False):
        # Cuando se ejecuta como ejecutable, usar la carpeta del ejecutable
        app_dir = os.path.dirname(sys.executable)
    else:
        # Cuando se ejecuta como script, usar la carpeta del archivo actual
        app_dir = os.path.dirname(os.path.abspath(__file__))

    metadata_path = os.path.join(
        app_dir,
        "metadata.json"
    )
    encodings = ["utf-8",
                 "utf-8-sig",
                 "cp1252",
                 "latin-1"]
    metadata = None

    try:
        for enc in encodings:
            try:
                with open(
                    metadata_path,
                    'r',
                    encoding=enc
                ) as f:
                    metadata = json.load(f)
                break
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError as e:
                messagebox.showerror(
                    "Error",
                    "metadata.json inválido: "
                    + e
                )
                sys.exit()
    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "metadata.json no encontrado en: "
            + metadata_path
        )
        shutil.rmtree(rhino_folder)
        sys.exit()

    if metadata is None:
        messagebox.showerror(
            "Error",
            "No se pudo leer metadata.json con las codificaciones probadas: "
            + encodings
        )
        shutil.rmtree(rhino_folder)
        sys.exit()

    prison_metadata = metadata["prisons"]

    if data.trib == "CONTROL 1":
        trib_metadata = metadata["tribs"]["first"]
    elif data.trib == "CONTROL 2":
        trib_metadata = metadata["tribs"]["second"]
    elif data.trib == "CONTROL 3":
        trib_metadata = metadata["tribs"]["third"]
    elif data.trib == "CONTROL 4":
        trib_metadata = metadata["tribs"]["fourth"]
    elif data.trib == "CONTROL 5":
        trib_metadata = metadata["tribs"]["fifth"]

    for current_patch, directories, files in os.walk(expedient_folder):
        for file in files:
            if file.endswith(".docx") and not file.startswith('~'):
                doc_path = os.path.join(
                    current_patch,
                    file
                )
                doc = Document(doc_path)
                for para in doc.paragraphs:
                    for run in para.runs:
                        # Saltar fotos o imágenes
                        if run.element.xpath("./w:drawing"):
                            continue

                        global_replacements(
                            self,
                            file,
                            run,
                            trib_metadata,
                            month_names,
                            today_date,
                            year_diffs
                        )

                        if (any(i in current_patch for
                                i in group_folders_names) and
                                (data.n_acusseds == 1)):
                            single_acussed_replacements(
                                self,
                                file,
                                run,
                        )

                        if (any(i in current_patch for
                                i in group_folders_names) and
                                (data.n_acusseds > 1)):
                            several_acusseds_replacements(
                                self,
                                file,
                                run,
                        )
                        
                        if "DECISIÓN" in current_patch:
                            decision_replacements(
                                self,
                                current_patch,
                                run,
                                prison_metadata,
                            )

                        tribunals_replacements(
                            self,
                            run,
                            trib_metadata,
                        )
                doc.save(doc_path)
    shutil.rmtree(rhino_folder)
    messagebox.showinfo(
        "Éxito",
        "Expediente creado en el escritorio."
    )
    sys.exit()
