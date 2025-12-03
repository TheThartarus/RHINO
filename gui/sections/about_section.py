import tkinter as tk

from gui.style.style import Style

def show_about(self):
    new_window = tk.Toplevel(self.root)
    new_window.title("ACERCA DE RHINO")
    new_window.iconbitmap("gui/style/rhino_icon.ico")
    new_window.geometry(
        "+{}+{}".format(
            self.root.winfo_x()
            + 100,
            self.root.winfo_y()
            + 100
        )
    )
    new_window.geometry("400x300")
    new_window.resizable(False, False)
    new_window.grid_columnconfigure(3, weight=1)

    # Desplegar el 'Label' con la información de la aplicación
    about_text = "Rhino 1.5.1" \
    "\n\nDesarrollado por: TheThartarus" \
    "\n\n\n\n© 2025 Todos los derechos reservados"
    about_label = tk.Label(
        new_window,
        text=about_text,
        font=Style.label_font,
        justify="center",
        wraplength=350
    )
    about_label.pack(expand=True)

    # Desplegar el 'Button' de 'CERRAR'
    close_button = tk.Button(
        new_window,
        text="CERRAR",
        font=Style.button_font,
        bg=Style.button_bg,
        fg=Style.button_fg,
        activebackground=Style.button_active_bg,
        activeforeground=Style.button_active_fg,
        command=new_window.destroy
    )
    close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = None
    show_about()
    root.mainloop()
