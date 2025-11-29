import tkinter as tk
from tkinter import messagebox

from gui.style.style import Style
from gui.sections.imp_data_fields import imp_data_fields
import data

def assis_data_fields(self):
    new_window = tk.Toplevel(self.root)
    new_window.title("DATOS DEL ASISTENTE")
    new_window.iconbitmap("gui/style/rhino_icon.ico")
    new_window.geometry(
        "+{}+{}".format(
            self.root.winfo_x()
            + 100,
            self.root.winfo_y()
            + 100
        )
    )
    new_window.geometry("530x115")
    new_window.resizable(False, False)
    new_window.grid_columnconfigure(3, weight=1)

    # Desplegar el 'Label' de 'FIRMA DEL ASISTENTE'
    assis_firm_label = tk.Label(
        new_window,
        text="FIRMA DEL ASISTENTE",
        font=Style.label_font
    )
    assis_firm_label.grid(
        row=0,
        column=0,
        pady=Style.pady,
        padx=Style.padx,
        sticky="w"
    )

    # Definir la función de validación para el 'Entry' de 'FIRMA'
    def validate_firm_input(P):
        if P == "" or all(char.isalpha()
                          or char == "." for char in P): return True
        return False

    # Desplegar el 'Entry' de 'FIRMA DEL ASISTENTE'
    assis_firm_entry = tk.Entry(
        new_window,
        font=Style.entry_font,
        validate="key"
    )
    assis_firm_entry.grid(
        row=0,
        column=1,
        pady=Style.pady,
        padx=Style.padx,
        sticky="ew"
    )
    assis_firm_entry['validatecommand'] = (
        assis_firm_entry.register(validate_firm_input),
        '%P'
    )

    def register():
        assis_firm = assis_firm_entry.get().strip()

        if not assis_firm:
            messagebox.showerror(
                "Error",
                "Por favor, complete el campo."
            )
            return

        data.assis_firm = assis_firm
        messagebox.showinfo(
            "Éxito",
            "Firma del asistente registrada correctamente."
        )
        imp_data_fields(self)
        new_window.destroy()

    # Desplegar el 'Button' de 'ACEPTAR'
    register_button = tk.Button(
        new_window, text="ACEPTAR",
        font=Style.button_font,
        bg=Style.button_bg,
        fg=Style.button_fg,
        activebackground=Style.button_active_bg,
        activeforeground=Style.button_active_fg,
        command=register
    )
    register_button.grid(
        row=1,
        column=0,
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
    assis_data_fields(app)
    root.mainloop()
