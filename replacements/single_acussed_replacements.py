import data

def single_acussed_replacements(
        self,
        file,
        run,
    ):
        if data.acusseds_data[0]["documented"] == "NO":
            if data.acusseds_data[0]["gender"] == "F":
                if "IMP_NAMES" in run.text:
                    run.text = run.text.replace(
                        "IMP_NAMES",
                        data.acusseds_data[0]["name"]
                        + " (NO DOCUMENTADA)"
                    )
            else:
                if "IMP_NAMES" in run.text:
                    run.text = run.text.replace(
                        "IMP_NAMES",
                        data.acusseds_data[0]["name"]
                        + " (NO DOCUMENTADO)"
                    )

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
        else:
            if "IMP_NAMES" in run.text:
                run.text = run.text.replace(
                    "IMP_NAMES",
                    data.acusseds_data[0]["name"]
                )
            if "TITULAR_TEXT" in run.text:
                run.text = run.text.replace(
                    " TITULAR_TEXT ",
                    " titular de la cédula de identidad N° "
                )
            if "IMP_CDIS" in run.text:
                run.text = run.text.replace(
                    "IMP_CDIS", data.acusseds_data[0]['nationality']
                    + "-"
                    + data.acusseds_data[0]["cdi"]
                )
            if "RESPECTIVELY_TEXT" in run.text:
                run.text = run.text.replace(
                    " RESPECTIVELY_TEXT",
                    ""
                )
            if "RESPECTIVELY_CR_TEXT" in run.text:
                run.text = run.text.replace(
                    " RESPECTIVELY_CR_TEXT",
                    ""
                )

        if data.acusseds_data[0]["multiple"] == True:
            if "del delito" in run.text:
                run.text = run.text.replace(
                    "del delito",
                    "de los delitos"
                )

        if data.acusseds_data[0]["gender"] == "F":
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
            if "al referido ciudadano" in run.text:
                run.text = run.text.replace(
                    "al referido ciudadano",
                    "a la referida ciudadana"
                )
            if "al imputado" in run.text:
                run.text = run.text.replace(
                    "al imputado",
                    "a la imputada"
                )
            if "del imputado" in run.text:
                run.text = run.text.replace(
                    "del imputado",
                    "de la imputada"
                )
