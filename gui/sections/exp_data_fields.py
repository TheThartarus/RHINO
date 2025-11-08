import tkinter as tk
from tkinter import messagebox

from gui.style.style import Style
from gui.sections.assis_data_fields import assis_data_fields

def exp_data_fields(self, db):
    new_window = tk.Toplevel(self.root)
    new_window.title("N° DE EXPEDIENTE")
    new_window.iconbitmap("gui/style/rhino_icon.ico")
    new_window.geometry("+{}+{}".format(self.root.winfo_x() + 100, self.root.winfo_y() + 100))
    new_window.geometry("490x115")
    new_window.resizable(False, False)
    new_window.grid_columnconfigure(3, weight=1)

    # Desplegar el 'Label' de 'N° DE EXPEDIENTE'
    expedient_number_label = tk.Label(new_window, text="N° DE EXPEDIENTE", font=Style.label_font)
    expedient_number_label.grid(row=0, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    # Definir la función de validación para el 'Entry' de 'N° DE EXPEDIENTE'
    def validate_expedient_number_input(P):
        if P == "" or all(char.isdigit() for char in P): return True
        return False

    # Desplegar el 'Entry' de 'N° DE EXPEDIENTE'
    expedient_number_entry = tk.Entry(new_window, textvariable=self.db.expedient_number_var, font=Style.entry_font, validate="key")
    expedient_number_entry.grid(row=0, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")
    expedient_number_entry['validatecommand'] = (expedient_number_entry.register(validate_expedient_number_input), '%P')

    def register():
        exp_number = expedient_number_entry.get()

        if not exp_number.strip():
            messagebox.showerror("Error", "Por favor, complete el campo.")
            return
        else:
            self.db.expedient_number_var.set(exp_number)
            messagebox.showinfo("Éxito", "Número de expediente registrado correctamente.")
            assis_data_fields(self, self.db)
            new_window.destroy()

    # Desplegar el 'Button' de 'REGISTRAR'
    register_button = tk.Button(new_window, text="ACEPTAR", font=Style.button_font, bg=Style.button_bg, fg=Style.button_fg,
                              activebackground=Style.button_active_bg, activeforeground=Style.button_active_fg, command=register)
    register_button.grid(row=1, column=0, pady=Style.pady, padx=Style.padx, sticky="ew")
    register_button.bind("<Return>", lambda event: register())

if __name__ == "__main__":
    root = tk.Tk()
    app = None
    exp_data_fields(app)
    root.mainloop()
