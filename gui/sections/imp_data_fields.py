import tkinter as tk
from tkinter import messagebox

from gui.style.style import Style
from gui.sections.cop_data_field import cop_data_field
import data

current_acussed = 0
def imp_data_fields(self):
    new_window = tk.Toplevel(self.root)
    new_window.title("DATOS DEL IMPUTADO N° " + str(current_acussed + 1))
    new_window.iconbitmap("gui/style/rhino_icon.ico")
    new_window.geometry("+{}+{}".format(self.root.winfo_x() + 100, self.root.winfo_y() + 100))
    new_window.geometry("665x340")
    new_window.resizable(False, False)
    new_window.grid_columnconfigure(3, weight=1)

    # Desplegar los 'Labels'
    name_label = tk.Label(new_window, text="NOMBRE", font=Style.label_font)
    name_label.grid(row=0, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    documented_label = tk.Label(new_window, text="DOCUMENTADO", font=Style.label_font)
    documented_label.grid(row=1, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    nationality_label = tk.Label(new_window, text="NACIONALIDAD", font=Style.label_font)
    nationality_label.grid(row=2, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    cdi_label = tk.Label(new_window, text="CÉDULA", font=Style.label_font)
    cdi_label.grid(row=3, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    gender_label = tk.Label(new_window, text="SEXO", font=Style.label_font)
    gender_label.grid(row=4, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    # Definir la función de validación para el 'Entry' de 'NOMBRE'
    def validate_name_input(P):
        if P == "" or all(char.isalpha() or char.isspace() for char in P): return True
        return False

    # Desplegar y validar el 'Entry' de 'NOMBRE'
    name_entry = tk.Entry(new_window, font=Style.entry_font, validate="key")
    name_entry.grid(row=0, columnspan=3, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")
    name_entry['validatecommand'] = (name_entry.register(validate_name_input), '%P')

    # Desplegar el 'OptionMenu' de 'DOCUMENTADO'
    documented_var = tk.StringVar(new_window)
    documented_var.set("SÍ")
    documented_menu = tk.OptionMenu(new_window, documented_var, "SÍ", "NO")
    documented_menu.grid(row=1, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")

    # Desplegar el 'OptionMenu' de 'VENEZOLANO O EXTRANJERO'
    nationality_var = tk.StringVar(new_window)
    nationality_var.set("VENEZOLANO")
    nationality_menu = tk.OptionMenu(new_window, nationality_var, "VENEZOLANO", "EXTRANJERO")
    nationality_menu.grid(row=2, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")

    # Definir la función de validación para el 'Entry' de 'CDI'
    def validate_cdi_input(P):
        if P == "" or all(char.isdigit() or char == "." for char in P): return True
        return False
    
    # Desplegar y validar el 'Entry' de 'CDI'
    cdi_entry = tk.Entry(new_window, font=Style.entry_font, validate="key")
    cdi_entry.grid(row=3, columnspan=3, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")
    cdi_entry['validatecommand'] = (cdi_entry.register(validate_cdi_input), '%P')

    # Desplegar el 'OptionMenu' de 'SEXO'
    gender_var = tk.StringVar(new_window)
    gender_var.set("SELECCIONAR")
    gender_menu = tk.OptionMenu(new_window, gender_var, "MASCULINO", "FEMENINO", "OTRO")
    gender_menu.grid(row=4, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")

    # Desplegar línea separadora
    tk.Frame(new_window, height=2, bd=1, relief=tk.SUNKEN).grid(row=5, column=1, columnspan=3, pady=Style.pady, sticky="ew")
    tk.Frame(new_window, height=2, bd=1, relief=tk.SUNKEN).grid(row=5, column=0, columnspan=3, pady=Style.pady, sticky="ew")

    # Definir la función del 'Button' de 'REGISTRAR'
    def register():
        name = name_entry.get().strip()
        cdi = cdi_entry.get().strip()
        gender = gender_var.get()
        documented = documented_var.get()
        nationality = nationality_var.get()

        if gender == "FEMENINO":
            gender = "F"
        elif gender == "MASCULINO":
            gender = "M"
        else:
            pass

        if nationality == "VENEZOLANO":
            nationality = "V"
        elif nationality == "EXTRANJERO":
            nationality = "E"
        else:
            pass

        if documented == "SÍ" and cdi and "." not in cdi:
            if len(cdi) == 9:
                cdi = cdi[:3] + "." + cdi[3:6] + "." + cdi[6:]
            elif len(cdi) == 8:
                cdi = cdi[:2] + "." + cdi[2:5] + "." + cdi[5:]
            elif len(cdi) == 7:
                cdi = cdi[:1] + "." + cdi[1:4] + "." + cdi[4:]

        # Si no está documentado, no exigir CDI
        if documented == "NO":
            cdi = ""

        if not name.strip() or (documented == "SÍ" and not cdi.strip()) or gender == "SELECCIONAR":
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        data.acusseds_data.append({'name': name, 'cdi': cdi, 'gender': gender, 'documented': documented, 'nationality': nationality})

        messagebox.showinfo("Éxito", "Imputado registrado correctamente.")
        new_window.destroy()

        global current_acussed

        current_acussed += 1
        if current_acussed < data.n_acusseds:
            imp_data_fields(self)
            new_window.destroy()
        else:
            messagebox.showinfo("Éxito", "Todos los imputados han sido registrados.")
            cop_data_field(self)

    # Desplegar el 'Button' de 'REGISTRAR'
    accept_button = tk.Button(new_window, text="REGISTRAR", font=Style.button_font, bg=Style.button_bg, fg=Style.button_fg,
                              activebackground=Style.button_active_bg, activeforeground=Style.button_active_fg, command=register)
    accept_button.grid(row=6, column=3, pady=Style.pady, padx=Style.padx, sticky="ew")
    accept_button.bind("<Return>", lambda event: register())

    def toggle_cdi(*args):
        if documented_var.get() == "NO":
            cdi_entry.delete(0, tk.END)
            cdi_entry.config(state=tk.DISABLED)
        else:
            cdi_entry.config(state=tk.NORMAL)

    try:
        documented_var.trace_add("write", toggle_cdi)
    except AttributeError:
        documented_var.trace("w", toggle_cdi)

    toggle_cdi()

if __name__ == "__main__":
    root = tk.Tk()
    app = None
    imp_data_fields(app)
    root.mainloop()
