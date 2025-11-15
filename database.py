import tkinter as tk

class Database:
        def __init__(self):
                self.trib_var = tk.StringVar(value="CONTROL 1")
                self.fisc_var = tk.StringVar(value="FLAGRANCIA")
                self.n_acusseds_var = tk.StringVar(value="1")
                self.expedient_number_var = tk.StringVar(value="")

                self.total_acusseds = 0
                self.current_acussed = 0
                self.acusseds_data = []

                self.assis_firm = tk.StringVar(value="")

                self.cop_data = ""
