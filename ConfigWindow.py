import tkinter as tk
import os
import json

CONFIG_FILE = "config.json"


class ConfigWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Configuración de Sitios")
        self.master.geometry("500x400")
        self.data = []

        self.load_config()
        self.create_table()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w") as f:
                json.dump([], f)

        with open(CONFIG_FILE, "r") as f:
            try:
                self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = []

    def create_table(self):
        header = tk.Frame(self.master)
        header.pack(fill=tk.X, pady=10)
        tk.Label(header, text="Dominio", font=("Arial", 12, "bold"),
                 width=30, anchor="w").grid(row=0, column=0)
        tk.Label(header, text="Tiempo (s)", font=(
            "Arial", 12, "bold"), width=15).grid(row=0, column=1)

        for i, item in enumerate(self.data):
            row = tk.Frame(self.master)
            row.pack(fill=tk.X, padx=10)
            tk.Label(row, text=item.get("dominio", ""),
                     anchor="w", width=30).grid(row=0, column=0)
            tk.Label(row, text=item.get("tiempo", ""),
                     width=15).grid(row=0, column=1)
