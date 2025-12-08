from docx.shared import Pt

import data

def global_replacements(
        self,
        file,
        run,
        trib_metadata,
        month_names,
        today_date,
        year_diffs
    ):
        run.font.name = trib_metadata["FONT_NAME"]

        if "CARÁTULA" in file:
            pass
        else:
            run.font.size = Pt(trib_metadata["FONT_SIZE"])

        if "EXP_NAME" in run.text:
            run.text = run.text.replace(
                "EXP_NAME", "MP21-P-"
                + str(today_date.year)
                + "-"
                + data.exp_number
            )
        if "EXP_LONG_DATE" in run.text:
            run.text = run.text.replace(
                "EXP_LONG_DATE",
                str(today_date.day)
                + " de "
                + str(month_names[today_date.month])
                + " de "
                + str(today_date.year)
            )
        if "YEAR" in run.text:
            run.text = run.text.replace(
                "YEAR",
                str(today_date.year)
            )
        if "DAYS" in run.text:
            if trib_metadata["judge"]["name"].startswith("LISSETH"):
                run.text = run.text.replace(
                    "DAYS",
                    str((year_diffs["ind"] + 1))
                    + "°"
                    + " y "
                    + str(year_diffs["fed"])
                    + "°"
                )
            else:
                run.text = run.text.replace(
                    "DAYS",
                    str((year_diffs["ind"] + 1))
                    + "°, "
                    + str(year_diffs["fed"])
                    + "°"
                    + " y "
                    + str(year_diffs["rev"])
                    + "°"
                )
        if "EXP_SHORT_DATE" in run.text:
            run.text = run.text.replace(
                "EXP_SHORT_DATE",
                str(today_date.day)
                + "/"
                + str(today_date.month)
                + "/"
                + str(today_date.year)
            )
        if "TRB_LONG_NUM_MAYUS" in run.text:
            run.text = run.text.replace(
                "TRB_LONG_NUM_MAYUS",
                trib_metadata["TRB_LONG_NUM_MAYUS"]
            )
        if "TRB_LONG_NUM_MINUS" in run.text:
            run.text = run.text.replace(
                "TRB_LONG_NUM_MINUS",
                trib_metadata["TRB_LONG_NUM_MINUS"]
            )
        if "TRB_SHORT_NUM" in run.text:
            run.text = run.text.replace(
                "TRB_SHORT_NUM",
                trib_metadata["TRB_SHORT_NUM"]
            )
        if "JUDGE_NAME" in run.text:
            run.text = run.text.replace(
                "JUDGE_NAME",
                trib_metadata["judge"]["name"]
            )
        if "JUDGE_INITIALS" in run.text:
            run.text = run.text.replace(
                "JUDGE_INITIALS",
                trib_metadata["judge"]["initials"]
            )
        if "SECRETARY_NAME" in run.text:
            run.text = run.text.replace(
                "SECRETARY_NAME",
                trib_metadata["secretary"]["name"]
            )
        if "SECRETARY_INITIALS" in run.text:
            run.text = run.text.replace(
                "SECRETARY_INITIALS",
                trib_metadata["secretary"]["initials"]
            )
        if trib_metadata["judge"]["gender"] == "F":
            if "JUEZ" in run.text:
                run.text = run.text.replace(
                    "JUEZ",
                    "JUEZA"
                )
        if trib_metadata["judge"]["gender"] == "F":
            if "DR" in run.text:
                run.text = run.text.replace(
                    "DR",
                    "DRA"
                )
        if trib_metadata["judge"]["name"].startswith("ROGER"):
            run.text = run.text.replace(
                "DR",
                "ABG"
            )
        if trib_metadata["judge"]["name"].startswith("CÉSAR"):
            run.text = run.text.replace(
                "DR",
                "ABG"
            )
        if trib_metadata["secretary"]["gender"] == "F":
            run.text = run.text.replace(
                "SECRETARIO",
                "SECRETARIA"
            )
        if "ASSISTANT_INITIALS" in run.text:
            run.text = run.text.replace(
                "ASSISTANT_INITIALS",
                data.assis_firm
            )
        if data.fisc == "FLAGRANCIA":
            if "FIS_NUM_MAYUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MAYUS",
                    "DE LA SALA DE FLAGRANCIA"
                )
            if "FIS_NUM_MINUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MINUS",
                    "de la Sala de Flagrancia"
                )
        elif data.fisc == "27°":
            if "FIS_NUM_MAYUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MAYUS",
                    "VIGÉSIMA SÉPTIMA (27°)"
                )
            if "FIS_NUM_MINUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MINUS",
                    "Vigésima Séptima (27°)"
                )
        elif data.fisc == "26°":
            if "FIS_NUM_MAYUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MAYUS",
                    "VIGÉSIMA SEXTA (26°)"
                )
            if "FIS_NUM_MINUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MINUS",
                    "Vigésima Sexta (26°)"
                )
        elif data.fisc == "22°":
            if "FIS_NUM_MAYUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MAYUS",
                    "VIGÉSIMA SEGUNDA (22°)"
                )
            if "FIS_NUM_MINUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MINUS",
                    "Vigésima Segunda (22°)"
                )
        elif data.fisc == "23°":
            if "FIS_NUM_MAYUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MAYUS",
                    "VIGÉSIMA TERCERA (23°)"
                )
            if "FIS_NUM_MINUS" in run.text:
                run.text = run.text.replace(
                    "FIS_NUM_MINUS",
                    "Vigésima Tercera (23°)"
                )
        if "IMP_COP" in run.text:
            if not data.cop_data.strip():
                pass
            else:
                run.text = run.text.replace(
                    "IMP_COP",
                    data.cop_data.strip()
                )
        if data.n_acusseds == 1:
            if "GENERAL_CRIME" in run.text:
                if not data.acusseds_data[0]["crime"].strip():
                    pass
                else:
                    run.text = run.text.replace(
                        "GENERAL_CRIME",
                        data.acusseds_data[0]["crime"].strip()
                    )
        else:
            if "GENERAL_CRIME" in run.text:
                if not data.general_crime["crime"].strip():
                    pass
                else:
                    run.text = run.text.replace(
                        "GENERAL_CRIME",
                        data.general_crime["crime"].strip()
                    )
