import data

def formatter(items):
    """
    - Si hay un solo item, se retorna sin cambios
    - Si hay dos items, se une con ' y '
    - Si hay tres o más items, todos menos el último se unen
    con comas pues el último se une con ' y '
    """
    items = [str(i).strip() for i in items if i is
                not None and str(i).strip() != ""]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return str(items[0] + " y " + items[1])
    return ", ".join(items[:-1]) + " y " + items[-1]

def several_acusseds_replacements(
        self,
        file,
        run,
    ):
        n_documented = (data.n_acusseds -
                        sum(data.acusseds_data[idx]["documented"] == "NO"
                            for idx in range(data.n_acusseds)))

        if "IMP_NAMES" in run.text:
            name_items = []
            for idx in range(data.n_acusseds):
                if data.acusseds_data[idx]["documented"] == "NO":
                    if data.acusseds_data[idx]["gender"] == "F":
                        name_items.insert(
                            0,
                            data.acusseds_data[idx]["name"]
                            + " (INDOCUMENTADA)"
                        )
                    else:
                        name_items.insert(
                            0,
                            data.acusseds_data[idx]["name"]
                            + " (INDOCUMENTADO)"
                        )
                else:
                    name_items.append(
                        data.acusseds_data[idx]["name"]
                    )
            run.text = run.text.replace(
                "IMP_NAMES",
                formatter(name_items)
            )

        if n_documented == 0:
            if "CARÁTULA" in file:
                if "TITULAR_TEXT" in run.text:
                    run.text = run.text.replace(
                        ", TITULAR_TEXT ",
                        ""
                    )
            else:
                if "TITULAR_TEXT" in run.text:
                    run.text = run.text.replace(
                        " TITULAR_TEXT ",
                        ""
                    )
            if "IMP_CDIS" in run.text:
                run.text = run.text.replace(
                    "IMP_CDIS",
                    ""
                )
            if "RESPECTIVELY_TEXT" in run.text:
                run.text = run.text.replace(
                    " RESPECTIVELY_TEXT,",
                    ""
                )
            if "RESPECTIVELY_CR_TEXT" in run.text:
                run.text = run.text.replace(
                    " RESPECTIVELY_CR_TEXT",
                    ""
                )

        if n_documented == 1:
            if "TITULAR_TEXT" in run.text:
                run.text = run.text.replace(
                    "TITULAR_TEXT",
                    "titular de la cédula de identidad N°"
                )
            if "IMP_CDIS" in run.text:
                for idx in range(data.n_acusseds):
                    if data.acusseds_data[idx]["documented"] == "NO":
                        continue
                    else:
                        if "CARÁTULA" in file:
                            run.text = run.text.replace(
                                "IMP_CDIS",
                                data.acusseds_data[idx]['nationality']
                                + "-"
                                + data.acusseds_data[idx]["cdi"]
                            )
                        else:
                            run.text = run.text.replace(
                                "IMP_CDIS",
                                data.acusseds_data[idx]['nationality']
                                + "-"
                                + data.acusseds_data[idx]["cdi"]
                                + ","
                            )
            if "RESPECTIVELY_TEXT" in run.text:
                run.text = run.text.replace(
                    " RESPECTIVELY_TEXT,",
                    ""
                )
            if "RESPECTIVELY_CR_TEXT" in run.text:
                run.text = run.text.replace(
                    " RESPECTIVELY_CR_TEXT",
                    ""
                )

        if n_documented > 1:
            if "TITULAR_TEXT" in run.text:
                run.text = run.text.replace(
                    "TITULAR_TEXT",
                    "titulares de las cédulas de identidad N°"
                )
            if "IMP_CDIS" in run.text:
                cdi_items = []
                for idx in range(data.n_acusseds):
                    if data.acusseds_data[idx]["documented"] == "NO":
                        continue
                    else:
                        cdi_items.append(
                            data.acusseds_data[idx]['nationality']
                            + "-"
                            + data.acusseds_data[idx]["cdi"]
                        )
                run.text = run.text.replace(
                    "IMP_CDIS",
                    formatter(cdi_items)
                )
            if "RESPECTIVELY_TEXT" in run.text:
                run.text = run.text.replace(
                    "RESPECTIVELY_TEXT",
                    "respectivamente"
                )
            if "RESPECTIVELY_CR_TEXT" in run.text:
                run.text = run.text.replace(
                    "RESPECTIVELY_CR_TEXT",
                    "respectivamente"
                )

            if data.general_crime["multiple"] == True:
                if "del delito" in run.text:
                    run.text = run.text.replace(
                        "del delito",
                        "de los delitos"
                    )

        if all(data.acusseds_data[i]["gender"] == "F"
               for i in range(data.n_acusseds)):
            if "del ciudadano" in run.text:
                run.text = run.text.replace(
                    "del ciudadano",
                    "de las ciudadanas"
                )
            if "al ciudadano" in run.text:
                run.text = run.text.replace(
                    "al ciudadano",
                    "a las ciudadanas"
                )
            if "al referido ciudadano" in run.text:
                run.text = run.text.replace(
                    "al referido ciudadano",
                    "a las referidas ciudadanas"
                )
            if "al imputado" in run.text:
                run.text = run.text.replace(
                    "al imputado",
                    "a las imputadas"
                )
            if "del imputado" in run.text:
                run.text = run.text.replace(
                    "del imputado",
                    "de las imputadas"
                )
            if "los imputados" in run.text:
                run.text = run.text.replace(
                    "los imputados",
                    "las imputadas"
                )
        else:
            if "del ciudadano" in run.text:
                run.text = run.text.replace(
                    "del ciudadano",
                    "de los ciudadanos"
                )
            if "al ciudadano" in run.text:
                run.text = run.text.replace(
                    "al ciudadano",
                    "a los ciudadanos"
                )   
            if "al referido ciudadano" in run.text:
                run.text = run.text.replace(
                    "al referido ciudadano",
                    "a los referidos ciudadanos"
                )
            if "al imputado" in run.text:
                run.text = run.text.replace(
                    "al imputado",
                    "a los imputados"
                )
            if "del imputado" in run.text:
                run.text = run.text.replace(
                    "del imputado",
                    "de los imputados"
                )
