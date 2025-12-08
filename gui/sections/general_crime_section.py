import tkinter as tk
from tkinter import messagebox

from gui.style.style import Style
from gui.sections.cop_section import cop_section

import data

def general_crime_section(self):
    new_window = tk.Toplevel(self.root)
    new_window.title("NOMBRE, LEY Y ARTÍCULO DEL DELITO(S)")
    new_window.iconbitmap("gui/style/rhino_icon.ico")
    new_window.geometry(
        "+{}+{}".format(
            self.root.winfo_x()
            + 100,
            self.root.winfo_y()
            + 100
        )
    )
    new_window.geometry("900x235")
    new_window.resizable(False, False)
    new_window.grid_columnconfigure(3, weight=1)

    # Desplegar los Labels
    crime_data_label = tk.Label(
        new_window,
        text="NOMBRE, LEY Y ARTÍCULO DEL DELITO(S) (OPCIONAL)",
        font=Style.label_font
    )
    crime_data_label.grid(
        row=0,
        column=0,
        pady=Style.pady,
        padx=Style.padx,
        sticky="w"
    )

    crime_data_label = tk.Label(
        new_window,
        text="INCLUIR 'PREVISTO(S) Y SANCIONADO(S) EN...'",
        font=Style.label_font
    )
    crime_data_label.grid(
        row=2,
        column=0,
        pady=Style.pady,
        padx=Style.padx,
        sticky="w"
    )

    crime_data_label = tk.Label(
        new_window,
        text="VARIOS DELITOS",
        font=Style.label_font
    )
    crime_data_label.grid(
        row=2,
        column=1,
        pady=Style.pady,
        padx=Style.padx,
        sticky="w"
    )

    general_label = tk.Label(
        new_window,
        text="GENERAL",
        font=Style.label_font
    )
    general_label.grid(
        row=3,
        column=0,
        pady=Style.pady,
        padx=Style.padx,
        sticky="w"
    )

    # Desplegar el Text de NOMBRE, LEY Y ARTÍCULO DEL DELITO
    crime_data_text = tk.Text(
        new_window,
        font=Style.entry_font,
        height=2,
        width=40
    )
    crime_data_text.grid(
        row=1,
        column=0,
        columnspan=4,
        pady=Style.pady,
        padx=Style.padx,
        sticky="ew"
    )

    # Desplegar el OptionMenu de VARIOS DELITOS
    crime_data_var = tk.StringVar(new_window)
    crime_data_var.set("NO")
    crime_data_optionmenu = tk.OptionMenu(
        new_window,
        crime_data_var,
        "SÍ",
        "NO"
    )
    crime_data_optionmenu.grid(
        row=2,
        column=3,
        pady=Style.pady,
        padx=Style.padx,
        sticky="ew",
        columnspan=2
    )

    def accept():
        crime = crime_data_text.get("1.0", "end-1c").strip()

        if crime_data_var.get() == "SÍ":
            multiple = True
        else:
            multiple = False
        
        data.general_crime.update(
            {
                "crime": crime,
                "multiple": multiple
            }
        )

        messagebox.showinfo(
            "Éxito",
            "Todos los datos delictivos han sido registrados correctamente."
        )

        cop_section(self)
        new_window.destroy()

    # Desplegar el Button de ACEPTAR/SALTAR
    accept_button = tk.Button(
        new_window,
        text="ACEPTAR/SALTAR",
        font=Style.button_font,
        bg=Style.button_bg,
        fg=Style.button_fg,
        activebackground=Style.button_active_bg,
        activeforeground=Style.button_active_fg,
        command=accept
    )
    accept_button.grid(
        row=3,
        column=1,
        pady=Style.pady,
        padx=Style.padx,
        sticky="ew",
        columnspan=4
    )

if __name__ == "__main__":
    root = tk.Tk()
    app = None
    general_crime_section(app)
    root.mainloop()
