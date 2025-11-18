import tkinter as tk

from gui.style.style import Style
from gui.sections.exp_data_fields import exp_data_fields
from gui.sections.show_about import show_about
from export import export
import data

class RhinoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rhino")
        self.root.iconbitmap("gui/style/rhino_icon.ico")
        self.root.geometry("380x305")
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(0, weight=1)

        # Desplegar los 'Labels'
        self.trib_label = tk.Label(self.root, text="TRIBUNAL", font=Style.label_font)
        self.trib_label.grid(row=0, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

        self.fisc_label = tk.Label(self.root, text="FISCALÍA", font=Style.label_font)
        self.fisc_label.grid(row=1, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

        self.n_acusseds_label = tk.Label(self.root, text="N° DE IMPUTADOS", font=Style.label_font)
        self.n_acusseds_label.grid(row=2, column=0, pady=Style.pady, padx=Style.padx, sticky="w")

        # Desplegar el 'OptionMenu' de 'TRIBUNAL'
        self.trib = tk.StringVar(self.root)
        self.trib.set("CONTROL 1")
        self.trib_optionmenu = tk.OptionMenu(self.root, self.trib, "CONTROL 1", "CONTROL 2", "CONTROL 3", "CONTROL 4", "CONTROL 5")
        self.trib_optionmenu.grid(row=0, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")

        # Desplegar el 'OptionMenu' de 'FISCALÍA'
        self.fisc = tk.StringVar(self.root)
        self.fisc.set("FLAGRANCIA")
        self.fisc_optionmenu = tk.OptionMenu(self.root, self.fisc, "FLAGRANCIA", "27°", "26°", "22°")
        self.fisc_optionmenu.grid(row=1, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")

        # Desplegar el 'OptionMenu' de 'N° DE IMPUTADOS'
        self.n_acusseds = tk.StringVar(self.root)
        self.n_acusseds.set("1")
        self.n_acusseds_optionmenu = tk.OptionMenu(self.root, self.n_acusseds, "1", "2", "3", "4", "5", "6", "7", "8")
        self.n_acusseds_optionmenu.grid(row=2, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")

        # Desplegar línea separadora
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN).grid(row=3, column=0, columnspan=2, pady=Style.pady, sticky="ew")

        def accept(self):
            data.trib = self.trib.get()
            data.fisc = self.fisc.get()
            data.n_acusseds = int(self.n_acusseds.get())

            exp_data_fields(self)

        # Desplegar el 'Button' de 'ACEPTAR'
        self.accept_button = tk.Button(self.root, text="ACEPTAR", font=Style.button_font, bg=Style.button_bg, fg=Style.button_fg,
                                       activebackground=Style.button_active_bg, activeforeground=Style.button_active_fg, command=lambda: accept(self))
        self.accept_button.grid(row=4, column=1, pady=Style.pady, padx=Style.padx, sticky="ew")

        # Desplegar el 'Button' de 'EXPORTAR'
        self.export_button = tk.Button(self.root, text="EXPORTAR", font=Style.button_font, bg=Style.button_bg, fg=Style.button_fg,
                                       activebackground=Style.button_active_bg, activeforeground=Style.button_active_fg, state=tk.DISABLED, command=lambda: export(self))
        self.export_button.grid(row=4, column=0, pady=Style.pady, padx=Style.padx, sticky="ew")

        # Desplegar el 'Button' de 'ACERCA DE RHINO'
        self.about_button = tk.Button(self.root, text="ACERCA DE RHINO", font=Style.button_font, bg=Style.button_bg, fg=Style.button_fg,
                                       activebackground=Style.button_active_bg, activeforeground=Style.button_active_fg, command=lambda: show_about(self))
        self.about_button.grid(row=5, column=0, columnspan=2, pady=Style.pady, padx=Style.padx, sticky="ew")

if __name__ == "__main__":
    root = tk.Tk()
    app = RhinoApp(root)
    root.mainloop()
