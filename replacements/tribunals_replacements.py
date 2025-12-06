import re

def replace_uppercase(match):
    word = match.group(0)
    if word.isupper():
        if len(word) < 4:
            return word.lower()
        else:
            return word.capitalize()
    else:
        return word

def tribunals_replacements(
        self,
        run,
        trib_metadata,
    ):
        if trib_metadata["judge"]["name"].startswith("CÉSAR"):
            run.text = re.sub(
                r'\b[A-ZÁÉÍÓÚÑÜ-]{1,}\b',
                replace_uppercase,
                run.text
            )

            if "xxx" in run.text:
                run.text = run.text.replace(
                    "xxx",
                    "XXX"
                )
            if "x.x.x." in run.text:
                run.text = run.text.replace(
                    "x.x.x.",
                    "X.X.X."
                )
            if "xx:xx" in run.text:
                run.text = run.text.replace(
                    "xx:xx",
                    "XX:XX"
                )
            if "Cagc" in run.text:
                run.text = run.text.replace(
                    "Cagc",
                    "CAGC"
                )
            if "-p-" in run.text:
                run.text = run.text.replace(
                    "-p-",
                    "-P-"
                )
            if "abg" in run.text:
                run.text = run.text.replace(
                    "abg",
                    "Abg"
                )
            if "tuy" in run.text:
                run.text = run.text.replace(
                    "tuy",
                    "Tuy"
                )
            if "v-" in run.text:
                run.text = run.text.replace(
                    "v-",
                    "V-"
                )
            if "el Notificado" in run.text:
                run.text = run.text.replace(
                    "el Notificado",
                    "El notificado"
                )
            if "del Citado" in run.text:
                run.text = run.text.replace(
                    "del Citado",
                    "del citado"
                )
            if "el Citado" in run.text:
                run.text = run.text.replace(
                    "el Citado",
                    "El citado"
                )
            if "iii" in run.text:
                run.text = run.text.replace(
                    "iii",
                    "III"
                )
            if "Estado" in run.text:
                run.text = run.text.replace(
                    "Estado",
                    "estado"
                )
            if "Municipio" in run.text:
                run.text = run.text.replace(
                    "Municipio",
                    "municipio"
                )
            if "Horas" in run.text:
                run.text = run.text.replace(
                    "Horas",
                    "horas"
                )
            if "su Despacho" in run.text:
                run.text = run.text.replace(
                    "su Despacho",
                    "Su despacho"
                )
