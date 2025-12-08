from tkinter import messagebox
import os
import sys
import re

import data

def decision_replacements(
        self,
        current_patch,
        run,
        prison_metadata,
    ):
        # Encontrar una carpeta con el patrón "N - Nombre"
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
            # Al encontrar la carpeta DECISIÓN, detener la búsqueda
            if parent == (search_path or
                          os.path.basename(search_path).upper() ==
                          "DECISIÓN"):
                break
            search_path = parent

        # Si no se encontró, intentar la penúltima carpeta como último recurso
        if idx is None:
            penult = os.path.basename(os.path.dirname(current_patch))
            try:
                idx = int(penult.split(" - ")[0])
            except Exception:
                messagebox.showerror(
                    "Error",
                    "No se pudo determinar el índice del imputado desde la ruta: "
                    + current_patch)
                sys.exit()

        if data.acusseds_data[idx]["documented"] == "NO":
            if data.acusseds_data[idx]["gender"] == "F":
                if "IMP_NAMES" in run.text:
                    run.text = run.text.replace(
                        "IMP_NAMES",
                        data.acusseds_data[idx]["name"]
                        .strip()
                        .upper()
                        + " (NO DOCUMENTADA)"
                    )
            else:
                if "IMP_NAMES" in run.text:
                    run.text = run.text.replace(
                        "IMP_NAMES",
                        data.acusseds_data[idx]["name"]
                        .strip()
                        .upper()
                        + " (NO DOCUMENTADO)"
                    )

            if "TITULAR_TEXT" in run.text:
                run.text = run.text.replace(
                    ", TITULAR_TEXT ",
                    ""
                )
            if "IMP_CDIS" in run.text:
                run.text = run.text.replace(
                    "IMP_CDIS",
                    ""
                )
        else:
            if "IMP_NAMES" in run.text:
                run.text = run.text.replace(
                    "IMP_NAMES",
                    data.acusseds_data[idx]["name"]
                    .strip()
                    .upper()
                )
            if "TITULAR_TEXT" in run.text:
                run.text = run.text.replace(
                    "TITULAR_TEXT",
                    "titular de la cédula de identidad N°"
                )
            if "IMP_CDIS" in run.text:
                run.text = run.text.replace(
                    "IMP_CDIS",
                    data.acusseds_data[idx]["nationality"]
                    .strip()
                    .upper()
                    + "-"
                    + data.acusseds_data[idx]["cdi"]
                    .strip()
                    .upper()
                )

        if data.acusseds_data[idx]["gender"] == "F":
            if "IMP_PRISON" in run.text:
                run.text = run.text.replace(
                    "IMP_PRISON",
                    prison_metadata["F"]
                )
            if "del ciudadano" in run.text:
                run.text = run.text.replace(
                    "del ciudadano",
                    "de la ciudadana"
                )
            if "al ciudadano" in run.text:
                run.text = run.text.replace(
                    "al ciudadano",
                    "a la ciudadana"
                )
            if "el ciudadano" in run.text:
                run.text = run.text.replace(
                    "el ciudadano",
                    "la ciudadana"
                )
            if "al imputado" in run.text:
                run.text = run.text.replace(
                    "al imputado",
                    "a la imputada"
                )
        else:
            run.text = run.text.replace(
                "IMP_PRISON",
                prison_metadata["M"]
            )

        if "IMP_CRIME" in run.text:
            run.text = run.text.replace(
                "IMP_CRIME",
                data.acusseds_data[idx]["crime"]
                .strip()
            )
        if data.acusseds_data[idx]["multiple"]:
            if "del delito" in run.text:
                run.text = run.text.replace(
                    "del delito",
                    "de los delitos"
                )
