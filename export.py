import tkinter as tk
from tkinter import messagebox
from docx import Document
from docx.shared import Pt
from datetime import date
import shutil
import os
import zipfile
import json
import sys
import re

import data

def export(self):
    today_date = date.today()

    month_names = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
                   "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

    IND_DAY = date(1811, 7, 5)
    ind_year_diff = today_date.year - IND_DAY.year
    FED_DAY = date(1859, 2, 20)
    fed_year_diff = today_date.year - FED_DAY.year
    REV_DAY = date(1999, 2, 2)
    rev_year_diff = today_date.year - REV_DAY.year

    if (today_date.month, today_date.day) < (IND_DAY.month, IND_DAY.day):
        ind_year_diff -= 1
    if (today_date.month, today_date.day) < (FED_DAY.month, FED_DAY.day):
        fed_year_diff -= 1
    if (today_date.month, today_date.day) < (REV_DAY.month, REV_DAY.day):
        rev_year_diff -= 1

    # Deshabilitar EXPORTAR mientras se crea el expediente
    self.export_button.config(state=tk.DISABLED)

    # Crear la carpeta Rhino en la carpeta Documentos si no existe
    user_documents = os.path.join(os.path.expanduser("~"), "Documents")
    rhino_folder = os.path.join(user_documents, "Rhino")
    os.makedirs(rhino_folder, exist_ok=True)

    # Extraer el archivo MODELS.zip en la carpeta Rhino
    try:
        user_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        zip_path = os.path.join(user_desktop, "MODELS.zip")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(rhino_folder)
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo MODELS.zip no encontrado en el escritorio")
        shutil.rmtree(rhino_folder)
        sys.exit()
    except zipfile.BadZipFile:
        messagebox.showerror("Error", "Archivo MODELS.zip está dañado o no es un archivo zip válido")
        shutil.rmtree(rhino_folder)
        sys.exit()

    # Crear carpeta del expediente en el escritorio
    expedient_name = f"{str(today_date.year)}-{data.exp_number}"
    expedient_folder = os.path.join(user_desktop, expedient_name)
    os.makedirs(expedient_folder, exist_ok=True)

    # Crear carpeta DECISIÓN en la carpeta del expediente
    ticket_folder = os.path.join(expedient_folder, "DECISIÓN")
    os.makedirs(ticket_folder, exist_ok=True)

    # Copiar la carpeta ENTRADA a la carpeta del expediente
    decision_src = os.path.join(rhino_folder, "MODELS", "ENTRADA")
    decision_dst = os.path.join(expedient_folder, "ENTRADA")
    shutil.copytree(decision_src, decision_dst)

    # Copiar la carpeta OFICIOS (GRUPALES) a la carpeta del expediente
    offices_src = os.path.join(rhino_folder, "MODELS", "OFICIOS (GRUPALES)")
    offices_dst = os.path.join(expedient_folder, "OFICIOS (GRUPALES)")
    shutil.copytree(offices_src, offices_dst)

    # Copiar la carpeta BOLETAS (GRUPALES) a la carpeta del expediente
    tickets_src = os.path.join(rhino_folder, "MODELS", "BOLETAS (GRUPALES)")
    tickets_dst = os.path.join(expedient_folder, "BOLETAS (GRUPALES)")
    shutil.copytree(tickets_src, tickets_dst)

    # Crear carpetas para cada imputado en la carpeta DECISIÓN
    for i in range(data.n_acusseds):
        acussed_name = data.acusseds_data[i]["name"].strip().upper().replace(" ", "_")
        ticket_src = os.path.join(rhino_folder, "MODELS", "DECISIÓN")
        # Prefijo con número y guión: "0 - NOMBRE"
        ticket_dst = os.path.join(ticket_folder, f"{i} - {acussed_name}")
        shutil.copytree(ticket_src, ticket_dst)

    # Cargar metadata.json desde la carpeta del ejecutable / main.py
    if getattr(sys, 'frozen', False):
        # Cuando se ejecuta como ejecutable (PyInstaller), usar la carpeta del ejecutable
        app_dir = os.path.dirname(sys.executable)
    else:
        # Cuando se ejecuta como script, usar la carpeta del archivo actual
        app_dir = os.path.dirname(os.path.abspath(__file__))

    metadata_path = os.path.join(app_dir, "metadata.json")
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]
    metadata = None

    try:
        for enc in encodings:
            try:
                with open(metadata_path, 'r', encoding=enc) as f:
                    metadata = json.load(f)
                break
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"metadata.json inválido: {e}")
                sys.exit()
    except FileNotFoundError:
        messagebox.showerror("Error", f"metadata.json no encontrado en: {metadata_path}")
        shutil.rmtree(rhino_folder)
        sys.exit()

    if metadata is None:
        messagebox.showerror("Error", f"No se pudo leer metadata.json con las codificaciones probadas: {encodings}")
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

    def formatter(items):
        """
        - Si hay un solo item, se retorna sin cambios
        - Si hay dos items, se une con ' y '
        - Si hay tres o más items, todos menos el último se unen con comas pues el último se une con ' y '
        """
        items = [str(i).strip() for i in items if i is not None and str(i).strip() != ""]
        if not items:
            return ""
        if len(items) == 1:
            return items[0]
        if len(items) == 2:
            return f"{items[0]} y {items[1]}"
        return ", ".join(items[:-1]) + " y " + items[-1]

    for current_patch, directories, files in os.walk(expedient_folder):
        for file in files:
            if file.endswith(".docx") and not file.startswith('~'):
                doc_path = os.path.join(current_patch, file)
                doc = Document(doc_path)
                for para in doc.paragraphs:
                    for run in para.runs:
                        # Saltar fotos o imágenes
                        if run.element.xpath("./w:drawing"):
                            continue

                        # --- Reemplazos globales ---
                        run.font.name = trib_metadata["FONT_NAME"]

                        if "CARÁTULA" in file:
                            pass
                        else:
                            run.font.size = Pt(trib_metadata["FONT_SIZE"])

                        if "EXP_NAME" in run.text:
                            run.text = run.text.replace("EXP_NAME", f"MP21-P-{str(today_date.year)}-{data.exp_number}")
                        if "EXP_LONG_DATE" in run.text:
                            run.text = run.text.replace("EXP_LONG_DATE", f"{today_date.day} de {month_names[today_date.month]} de {today_date.year}")
                        if "YEAR" in run.text:
                            run.text = run.text.replace("YEAR", str(today_date.year))
                        if "DAYS" in run.text:
                            if trib_metadata["judge"]["name"].startswith("LISSETH"):
                                run.text = run.text.replace("DAYS", f"{ind_year_diff + 1}° y {fed_year_diff}°")
                            else:
                                run.text = run.text.replace("DAYS", f"{ind_year_diff + 1}°, {fed_year_diff}° y {rev_year_diff}°")
                        if "EXP_SHORT_DATE" in run.text:
                            run.text = run.text.replace("EXP_SHORT_DATE", f"{today_date.day}/{today_date.month}/{today_date.year}")
                        if "TRB_LONG_NUM_MAYUS" in run.text:
                            run.text = run.text.replace("TRB_LONG_NUM_MAYUS", trib_metadata["TRB_LONG_NUM_MAYUS"])
                        if "TRB_LONG_NUM_MINUS" in run.text:
                            run.text = run.text.replace("TRB_LONG_NUM_MINUS", trib_metadata["TRB_LONG_NUM_MINUS"])
                        if "TRB_SHORT_NUM" in run.text:
                            run.text = run.text.replace("TRB_SHORT_NUM", trib_metadata["TRB_SHORT_NUM"])
                        if "JUDGE_NAME" in run.text:
                            run.text = run.text.replace("JUDGE_NAME", trib_metadata["judge"]["name"])
                        if "JUDGE_INITIALS" in run.text:
                            run.text = run.text.replace("JUDGE_INITIALS", trib_metadata["judge"]["initials"])
                        if "SECRETARY_NAME" in run.text:
                            run.text = run.text.replace("SECRETARY_NAME", trib_metadata["secretary"]["name"])
                        if "SECRETARY_INITIALS" in run.text:
                            run.text = run.text.replace("SECRETARY_INITIALS", trib_metadata["secretary"]["initials"])
                        if trib_metadata["judge"]["gender"] == "F":
                            if "JUEZ" in run.text:
                                run.text = run.text.replace("JUEZ", "JUEZA")
                        if trib_metadata["judge"]["gender"] == "F":
                            if "DR" in run.text:
                                run.text = run.text.replace("DR", "DRA")
                        else:
                            if trib_metadata["judge"]["name"].startswith("ROGER") or trib_metadata["judge"]["name"].startswith("CÉSAR"):
                                run.text = run.text.replace("DR", "ABG")
                        if trib_metadata["secretary"]["gender"] == "F":
                            run.text = run.text.replace("SECRETARIO", "SECRETARIA")
                        if "ASSISTANT_INITIALS" in run.text:
                            run.text = run.text.replace("ASSISTANT_INITIALS", data.assis_firm)
                        if data.fisc == "FLAGRANCIA":
                            if "FIS_NUM_MAYUS" in run.text:
                                run.text = run.text.replace("FIS_NUM_MAYUS", "DE LA SALA DE FLAGRANCIA")
                            if "FIS_NUM_MINUS" in run.text:
                                run.text = run.text.replace("FIS_NUM_MINUS", "de la Sala de Flagrancia")
                        elif data.fisc == "27°":
                            if "FIS_NUM_MAYUS" in run.text:
                                run.text = run.text.replace("FIS_NUM_MAYUS", "VIGÉSIMA SÉPTIMA (27°)")
                            if "FIS_NUM_MINUS" in run.text:
                                run.text = run.text.replace("FIS_NUM_MINUS", "Vigésima Séptima (27°)")
                        elif data.fisc == "26°":
                            if "FIS_NUM_MAYUS" in run.text:
                                run.text = run.text.replace("FIS_NUM_MAYUS", "VIGÉSIMA SEXTA (26°)")
                            if "FIS_NUM_MINUS" in run.text:
                                run.text = run.text.replace("FIS_NUM_MINUS", "Vigésima Sexta (26°)")
                        elif data.fisc == "22°":
                            if "FIS_NUM_MAYUS" in run.text:
                                run.text = run.text.replace("FIS_NUM_MAYUS", "VIGÉSIMA SEGUNDA (22°)")
                            if "FIS_NUM_MINUS" in run.text:
                                run.text = run.text.replace("FIS_NUM_MINUS", "Vigésima Segunda (22°)")
                        else:
                            pass
                        if "IMP_COP" in run.text:
                            if not data.cop_data.strip():
                                pass
                            else:
                                run.text = run.text.replace("IMP_COP", data.cop_data.strip())

                        # --- Reemplazos a ENTRADA, BOLETAS (GRUPALES) y OFICIOS (GRUPALES) ---
                        if (("ENTRADA" in current_patch) or ("BOLETAS (GRUPALES)" in current_patch) or ("OFICIOS (GRUPALES)" in current_patch)) and (data.n_acusseds == 1):
                            if data.acusseds_data[0]["documented"] == "NO":
                                if data.acusseds_data[0]["gender"] == "F":
                                    if "IMP_NAMES" in run.text:
                                        run.text = run.text.replace("IMP_NAMES", data.acusseds_data[0]["name"].strip().upper() + " (NO DOCUMENTADA)")
                                else:
                                    if "IMP_NAMES" in run.text:
                                        run.text = run.text.replace("IMP_NAMES", data.acusseds_data[0]["name"].strip().upper() + " (NO DOCUMENTADO)")
                                if "CARÁTULA" in file:
                                    if "TITULAR_TEXT" in run.text:
                                        run.text = run.text.replace(", TITULAR_TEXT ", "")
                                else:
                                    if "TITULAR_TEXT" in run.text:
                                        run.text = run.text.replace(" TITULAR_TEXT ", "")
                                if "IMP_CDIS" in run.text:
                                    run.text = run.text.replace("IMP_CDIS", "")
                                if "RESPECTIVELY_TEXT" in run.text:
                                    run.text = run.text.replace(" RESPECTIVELY_TEXT,", "")
                                if "RESPECTIVELY_CR_TEXT" in run.text:
                                    run.text = run.text.replace(" RESPECTIVELY_CR_TEXT", "")
                            else:
                                if "IMP_NAMES" in run.text:
                                    run.text = run.text.replace("IMP_NAMES", data.acusseds_data[0]["name"].strip().upper())
                                if "TITULAR_TEXT" in run.text:
                                    run.text = run.text.replace(" TITULAR_TEXT ", " titular de la cédula de identidad N° ")
                                if "IMP_CDIS" in run.text:
                                    run.text = run.text.replace("IMP_CDIS", f"{data.acusseds_data[0]['nationality'].strip().upper()}-{data.acusseds_data[0]["cdi"].strip().upper()}")
                                if "RESPECTIVELY_TEXT" in run.text:
                                    run.text = run.text.replace(" RESPECTIVELY_TEXT", "")
                                if "RESPECTIVELY_CR_TEXT" in run.text:
                                    run.text = run.text.replace(" RESPECTIVELY_CR_TEXT", "")
                            if data.acusseds_data[0]["gender"] == "F":
                                if "del ciudadano" in run.text:
                                    run.text = run.text.replace("del ciudadano", "de la ciudadana")
                                if "al ciudadano" in run.text:
                                    run.text = run.text.replace("al ciudadano", "a la ciudadana")
                                if "al referido ciudadano" in run.text:
                                    run.text = run.text.replace("al referido ciudadano", "a la referida ciudadana")
                                if "al imputado" in run.text:
                                    run.text = run.text.replace("al imputado", "a la imputada")
                                if "del imputado" in run.text:
                                    run.text = run.text.replace("del imputado", "de la imputada")

                        if (("ENTRADA" in current_patch) or ("BOLETAS (GRUPALES)" in current_patch) or ("OFICIOS (GRUPALES)" in current_patch)) and (data.n_acusseds > 1):
                            n_documented = data.n_acusseds - sum(data.acusseds_data[idx]["documented"] == "NO" for idx in range(data.n_acusseds))
                            if "IMP_NAMES" in run.text:
                                name_items = []
                                for idx in range(data.n_acusseds):
                                    if data.acusseds_data[idx]["documented"] == "NO":
                                        if data.acusseds_data[idx]["gender"] == "F":
                                            name_items.insert(0, data.acusseds_data[idx]["name"].strip().upper() + " (INDOCUMENTADA)")
                                        else:
                                            name_items.insert(0, data.acusseds_data[idx]["name"].strip().upper() + " (INDOCUMENTADO)")
                                    else:
                                        name_items.append(data.acusseds_data[idx]["name"].strip().upper())
                                run.text = run.text.replace("IMP_NAMES", formatter(name_items))
                            if n_documented == 0:
                                if "CARÁTULA" in file:
                                    if "TITULAR_TEXT" in run.text:
                                        run.text = run.text.replace(", TITULAR_TEXT ", "")
                                else:
                                    if "TITULAR_TEXT" in run.text:
                                        run.text = run.text.replace(" TITULAR_TEXT ", "")
                                if "IMP_CDIS" in run.text:
                                    run.text = run.text.replace("IMP_CDIS", "")
                                if "RESPECTIVELY_TEXT" in run.text:
                                    run.text = run.text.replace(" RESPECTIVELY_TEXT,", "")
                                if "RESPECTIVELY_CR_TEXT" in run.text:
                                    run.text = run.text.replace(" RESPECTIVELY_CR_TEXT", "")
                            if n_documented == 1:
                                if "TITULAR_TEXT" in run.text:
                                    run.text = run.text.replace("TITULAR_TEXT", "titular de la cédula de identidad N°")
                                if "IMP_CDIS" in run.text:
                                    for idx in range(data.n_acusseds):
                                        if data.acusseds_data[idx]["documented"] == "NO":
                                            continue
                                        else:
                                            if "CARÁTULA" in file:
                                                run.text = run.text.replace("IMP_CDIS", f"{data.acusseds_data[idx]['nationality'].strip().upper()}-{data.acusseds_data[idx]["cdi"].strip().upper()}")
                                            else:
                                                run.text = run.text.replace("IMP_CDIS", f"{data.acusseds_data[idx]['nationality'].strip().upper()}-{data.acusseds_data[idx]["cdi"].strip().upper()},")
                                if "RESPECTIVELY_TEXT" in run.text:
                                    run.text = run.text.replace(" RESPECTIVELY_TEXT,", "")
                                if "RESPECTIVELY_CR_TEXT" in run.text:
                                    run.text = run.text.replace(" RESPECTIVELY_CR_TEXT", "")
                            if n_documented > 1:
                                if "TITULAR_TEXT" in run.text:
                                    run.text = run.text.replace("TITULAR_TEXT", "titulares de las cédulas de identidad N°")
                                if "IMP_CDIS" in run.text:
                                    cdi_items = []
                                    for idx in range(data.n_acusseds):
                                        if data.acusseds_data[idx]["documented"] == "NO":
                                            continue
                                        else:
                                            cdi_items.append(f"{data.acusseds_data[idx]['nationality'].strip().upper()}-{data.acusseds_data[idx]["cdi"].strip().upper()}")
                                    run.text = run.text.replace("IMP_CDIS", f"{formatter(cdi_items)}")
                                if "RESPECTIVELY_TEXT" in run.text:
                                    run.text = run.text.replace("RESPECTIVELY_TEXT", "respectivamente")
                                if "RESPECTIVELY_CR_TEXT" in run.text:
                                    run.text = run.text.replace("RESPECTIVELY_CR_TEXT", "respectivamente")
                            if all(data.acusseds_data[i]["gender"] == "F" for i in range(data.n_acusseds)):
                                if "del ciudadano" in run.text:
                                    run.text = run.text.replace("del ciudadano", "de las ciudadanas")
                                if "al ciudadano" in run.text:
                                    run.text = run.text.replace("al ciudadano", "a las ciudadanas")
                                if "al referido ciudadano" in run.text:
                                    run.text = run.text.replace("al referido ciudadano", "a las referidas ciudadanas")
                                if "al imputado" in run.text:
                                    run.text = run.text.replace("al imputado", "a las imputadas")
                                if "del imputado" in run.text:
                                    run.text = run.text.replace("del imputado", "de las imputadas")
                            else:
                                if "del ciudadano" in run.text:
                                    run.text = run.text.replace("del ciudadano", "de los ciudadanos")
                                if "al ciudadano" in run.text:
                                    run.text = run.text.replace("al ciudadano", "a los ciudadanos")   
                                if "al referido ciudadano" in run.text:
                                    run.text = run.text.replace("al referido ciudadano", "a los referidos ciudadanos")
                                if "al imputado" in run.text:
                                    run.text = run.text.replace("al imputado", "a los imputados")
                                if "del imputado" in run.text:
                                    run.text = run.text.replace("del imputado", "de los imputados")

                        # --- Reemplazos a DECISIÓN ---
                        if "DECISIÓN" in current_patch:
                                # Buscar hacia arriba en la jerarquía hasta encontrar una carpeta con el patrón "N - Nombre"
                                search_path = os.path.normpath(current_patch)
                                idx = None
                                while True:
                                    folder_name = os.path.basename(search_path)
                                    m = re.match(r'^\s*(\d+)\s*-\s*', folder_name)
                                    if m:
                                        try:
                                            idx = int(m.group(1))
                                            break
                                        except ValueError:
                                            pass
                                    parent = os.path.dirname(search_path)
                                    # Si llegamos a la misma ruta o a la carpeta DECISIÓN, detenemos la búsqueda
                                    if parent == search_path or os.path.basename(search_path).upper() == "DECISIÓN":
                                        break
                                    search_path = parent

                                # Si no se encontró, intentar la penúltima carpeta como último recurso
                                if idx is None:
                                    penult = os.path.basename(os.path.dirname(current_patch))
                                    try:
                                        idx = int(penult.split(" - ")[0])
                                    except Exception:
                                        messagebox.showerror("Error", f"No se pudo determinar el índice del imputado desde la ruta: {current_patch}")
                                        sys.exit()

                                if data.acusseds_data[idx]["documented"] == "NO":
                                    if data.acusseds_data[idx]["gender"] == "F":
                                        if "IMP_NAMES" in run.text:
                                            run.text = run.text.replace("IMP_NAMES", data.acusseds_data[idx]["name"].strip().upper() + " (NO DOCUMENTADA)")
                                    else:
                                        if "IMP_NAMES" in run.text:
                                            run.text = run.text.replace("IMP_NAMES", data.acusseds_data[idx]["name"].strip().upper() + " (NO DOCUMENTADO)")
                                    if "TITULAR_TEXT" in run.text:
                                        run.text = run.text.replace(", TITULAR_TEXT ", "")
                                    if "IMP_CDIS" in run.text:
                                        run.text = run.text.replace("IMP_CDIS", "")
                                else:
                                    if "IMP_NAMES" in run.text:
                                        run.text = run.text.replace("IMP_NAMES", data.acusseds_data[idx]["name"].strip().upper())
                                    if "TITULAR_TEXT" in run.text:
                                        run.text = run.text.replace("TITULAR_TEXT", "titular de la cédula de identidad N°")
                                    if "IMP_CDIS" in run.text:
                                        run.text = run.text.replace("IMP_CDIS", f"{data.acusseds_data[idx]["nationality"].strip().upper()}-{data.acusseds_data[idx]["cdi"].strip().upper()}")
                                if data.acusseds_data[idx]["gender"] == "F":
                                    if "IMP_PRISON" in run.text:
                                        run.text = run.text.replace("IMP_PRISON", prison_metadata["F"])
                                    if "del ciudadano" in run.text:
                                        run.text = run.text.replace("del ciudadano", "de la ciudadana")
                                    if "al ciudadano" in run.text:
                                        run.text = run.text.replace("al ciudadano", "a la ciudadana")
                                    if "el ciudadano" in run.text:
                                        run.text = run.text.replace("el ciudadano", "la ciudadana")
                                    if "al imputado" in run.text:
                                        run.text = run.text.replace("al imputado", "a la imputada")
                                else:
                                    run.text = run.text.replace("IMP_PRISON", prison_metadata["M"])

                        # --- Post-reemplazos tribunalicios ---

                        # --- QUINTO ---
                        if trib_metadata["judge"]["name"].startswith("CÉSAR"):
                            # Gramática
                            def replace_uppercase(match):
                                word = match.group(0)
                                if word.isupper():
                                    if len(word) < 4:
                                        return word.lower()
                                    else:
                                        return word.capitalize()
                                else:
                                    return word

                            run.text = re.sub(r'\b[A-ZÁÉÍÓÚÑÜ-]{1,}\b', replace_uppercase, run.text)

                            # Fix(s)
                            if "xxx" in run.text:
                                run.text = run.text.replace("xxx", "XXX")
                            if "x.x.x." in run.text:
                                run.text = run.text.replace("x.x.x.", "X.X.X.")
                            if "xx:xx" in run.text:
                                run.text = run.text.replace("xx:xx", "XX:XX")
                            if "Cagc" in run.text:
                                run.text = run.text.replace("Cagc", "CAGC")
                            if "-p-" in run.text:
                                run.text = run.text.replace("-p-", "-P-")
                            if "abg" in run.text:
                                run.text = run.text.replace("abg", "Abg")
                            if "tuy" in run.text:
                                run.text = run.text.replace("tuy", "Tuy")
                            if "v-" in run.text:
                                run.text = run.text.replace("v-", "V-")
                            if "el Notificado" in run.text:
                                run.text = run.text.replace("el Notificado", "El notificado")
                            if "del Citado" in run.text:
                                run.text = run.text.replace("del Citado", "del citado")
                            if "el Citado" in run.text:
                                run.text = run.text.replace("el Citado", "El citado")
                            if "iii" in run.text:
                                run.text = run.text.replace("iii", "III")
                            if "Estado" in run.text:
                                run.text = run.text.replace("Estado", "estado")
                            if "Municipio" in run.text:
                                run.text = run.text.replace("Municipio", "municipio")
                            if "Horas" in run.text:
                                run.text = run.text.replace("Horas", "horas")
                            if "su Despacho" in run.text:
                                run.text = run.text.replace("su Despacho", "Su despacho")
                doc.save(doc_path)
    shutil.rmtree(rhino_folder)
    messagebox.showinfo("Éxito", "Expediente creado en el escritorio.")
    sys.exit()
