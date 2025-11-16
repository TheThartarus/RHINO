import tkinter as tk
from tkinter import messagebox

from gui.style.style import Style
from gui.sections.imp_data_fields import imp_data_fields

def assis_data_fields(self, db):
    new_window = tk.Toplevel(self.root)
    new_window.title("DATOS DEL ASISTENTE")
    new_window.iconbitmap("gui/style/rhino_icon.ico")
    new_window.geometry("+{}+{}".format(self.root.winfo_x() + 100, self.root.winfo_y() + 100))
    new_window.geometry("530x115")
    new_window.resizable(False, False)
    new_window.grid_columnconfigure(3, weight=1)

    # Desplegar el 'Label' de 'FIRMA DEL ASISTENTE'
    assis_signature = tk.Label(new_window, text="FIRMA DEL ASISTENTE", font=Style.label_font)
    assis_signature.grid(row=0, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    # Definir la función de validación para el 'Entry' de 'FIRMA DEL ASISTENTE'
    def validate_firm_input(P):
        if P == "" or all(char.isalpha() or char == "." for char in P): return True
        return False

    # Desplegar el 'Entry' de 'FIRMA DEL ASISTENTE'
    assis_signature = tk.Entry(new_window, textvariable=self.db.assis_firm, font=Style.entry_font, validate="key")
    assis_signature.grid(row=0, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")
    assis_signature['validatecommand'] = (assis_signature.register(validate_firm_input), '%P')

    def register():
        assis_firm = assis_signature.get()

        if not assis_firm.strip():
            messagebox.showerror("Error", "Por favor, complete el campo.")
            return
        else:
            self.db.assis_firm.set(assis_firm)
            messagebox.showinfo("Éxito", "Firma del asistente registrada correctamente.")
            imp_data_fields(self, self.db)
            new_window.destroy()

    # Desplegar el 'Button' de 'ACEPTAR'
    register_button = tk.Button(new_window, text="ACEPTAR", font=Style.button_font, bg=Style.button_bg, fg=Style.button_fg,
                              activebackground=Style.button_active_bg, activeforeground=Style.button_active_fg, command=register)
    register_button.grid(row=1, column=0, pady=Style.pady, padx=Style.padx, sticky="ew")
    register_button.bind("<Return>", lambda event: register())

if __name__ == "__main__":
    root = tk.Tk()
    app = None
    assis_data_fields(app)
    root.mainloop()
