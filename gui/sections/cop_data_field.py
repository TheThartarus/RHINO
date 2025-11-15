import tkinter as tk
from tkinter import messagebox

from gui.style.style import Style

def cop_data_field(self, db):
    new_window = tk.Toplevel(self.root)
    new_window.title("DATOS DEL ÓRGANO APREHENSOR")
    new_window.iconbitmap("gui/style/rhino_icon.ico")
    new_window.geometry("+{}+{}".format(self.root.winfo_x() + 100, self.root.winfo_y() + 100))
    new_window.geometry("900x185")
    new_window.resizable(True, True)
    new_window.grid_columnconfigure(3, weight=1)

    # Desplegar el 'Label' de 'NOMBRE Y DIRECCIÓN DEL ÓRGANO APREHENSOR'
    cop_data_label = tk.Label(new_window, text="NOMBRE Y DIRECCIÓN DEL ÓRGANO APREHENSOR (OPCIONAL)", font=Style.label_font)
    cop_data_label.grid(row=0, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    # Desplegar el 'Label' de 'INCLUIR...'
    cop_data_label = tk.Label(new_window, text="INCLUIR 'DIRECTOR DEL...' O 'JEFE DEL...'", font=Style.label_font)
    cop_data_label.grid(row=2, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

    # Desplegar el 'Text' de 'NOMBRE Y DIRECCIÓN DEL ÓRGANO APREHENSOR'
    cop_data_text = tk.Text(new_window, font=Style.entry_font, height=2, width=40)
    cop_data_text.grid(row=1, column=0, columnspan=4, pady=Style.pady, padx=Style.padx, sticky="ew")

    # Definir la función del 'Button' de 'ACEPTAR'
    def register():
        cop_data = cop_data_text.get("1.0", "end-1c").strip()
        db.cop_data = cop_data

        self.trib_optionmenu.config(state=tk.DISABLED)
        self.fisc_optionmenu.config(state=tk.DISABLED)
        self.n_acusseds_optionmenu.config(state=tk.DISABLED)
        self.export_button.config(state=tk.NORMAL)
        self.accept_button.config(state=tk.DISABLED)

        messagebox.showinfo("Éxito", "Datos del órgano aprehensor registrados correctamente.")
        messagebox.showinfo("Éxito", "Todos los datos han sido registrados correctamente.")
        new_window.destroy()

    # Desplegar el 'Button' de 'ACEPTAR/SALTAR'
    register_button = tk.Button(new_window, text="ACEPTAR/SALTAR", font=Style.button_font, bg=Style.button_bg, fg=Style.button_fg,
                              activebackground=Style.button_active_bg, activeforeground=Style.button_active_fg, command=register)
    register_button.grid(row=2, column=3, pady=Style.pady, padx=Style.padx, sticky="ew")
    #register_button.bind("<Return>", lambda event: register())

if __name__ == "__main__":
    root = tk.Tk()
    app = None
    cop_data_field(app)
    root.mainloop()
