import tkinter as tk
from tkinter import messagebox

from gui.style.style import Style
from gui.sections.assis_section import assis_data_fields
import data

def exp_data_fields(self):
    new_window = tk.Toplevel(self.root)
    new_window.title("N° DE EXPEDIENTE")
    new_window.iconbitmap("gui/style/rhino_icon.ico")
    new_window.geometry(
        "+{}+{}".format(
            self.root.winfo_x()
            + 100,
            self.root.winfo_y()
            + 100
        )
    )
    new_window.geometry("490x115")
    new_window.resizable(True, True)
    new_window.grid_columnconfigure(3, weight=1)

    # Desplegar el 'Label' de 'N° DE EXPEDIENTE'
    exp_number_label = tk.Label(
        new_window,
        text="N° DE EXPEDIENTE",
        font=Style.label_font
    )
    exp_number_label.grid(
        row=0,
        column=0,
        pady=Style.pady,
        padx=Style.padx,
        sticky="w"
    )

    # Definir la función de validación para el 'Entry' de 'N° DE EXPEDIENTE'
    def validate_exp_number_input(P):
        if P == "" or all(char.isdigit() for char in P): return True
        return False

    # Desplegar el 'Entry' de 'N° DE EXPEDIENTE'
    exp_number_entry = tk.Entry(
        new_window,
        font=Style.entry_font,
        validate="key"
    )
    exp_number_entry.grid(
        row=0,
        column=1,
        pady=Style.pady,
        padx=Style.padx,
        sticky="ew"
    )
    exp_number_entry['validatecommand'] = (
        exp_number_entry.register(validate_exp_number_input),
        '%P'
    )

    # Desplegar el 'Label' de ejemplo de formato
    format_label = tk.Label(
        new_window,
        text="EJEMPLO: 004523",
        font=Style.label_font
    )
    format_label.grid(
        row=1,
        column=0,
        pady=Style.pady,
        padx=Style.padx,
        sticky="w"
    )

    def register():
        exp_number = exp_number_entry.get().strip()

        if not exp_number:
            messagebox.showerror(
                "Error",
                "Por favor, complete el campo."
            )
            return

        data.exp_number = exp_number
        messagebox.showinfo(
            "Éxito",
            "Número de expediente registrado correctamente."
        )
        assis_data_fields(self)
        new_window.destroy()

    # Desplegar el 'Button' de 'ACEPTAR'
    register_button = tk.Button(
        new_window,
        text="ACEPTAR",
        font=Style.button_font,
        bg=Style.button_bg,
        fg=Style.button_fg,
        activebackground=Style.button_active_bg,
        activeforeground=Style.button_active_fg,
        command=register
    )
    register_button.grid(
        row=1,
        column=1,
        pady=Style.pady,
        padx=Style.padx,
        sticky="ew"
    )
    register_button.bind(
        "<Return>",
        lambda event: register()
    )

if __name__ == "__main__":
    root = tk.Tk()
    app = None
    exp_data_fields(app)
    root.mainloop()
