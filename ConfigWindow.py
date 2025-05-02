import tkinter as tk
import os
import json

from tkinter import messagebox

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

        # Section for add new domain
        form_frame = tk.Frame(self.master)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Dominio:").grid(row=0, column=0, padx=5)
        self.new_domain_entry = tk.Entry(form_frame, width=30)
        self.new_domain_entry.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Tiempo (s):").grid(row=0, column=2, padx=5)
        self.new_time_entry = tk.Entry(form_frame, width=10)
        self.new_time_entry.grid(row=0, column=3, padx=5)

        add_button = tk.Button(
            form_frame, text="Guardar", command=self.add_entry)
        add_button.grid(row=0, column=4, padx=5)

    def add_entry(self):
        dominio = self.new_domain_entry.get().strip()
        tiempo = self.new_time_entry.get().strip()

        if dominio and tiempo.isdigit():
            self.data.append({"dominio": dominio, "tiempo": int(tiempo)})
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
            self.master.destroy()
            ConfigWindow(self.master.master)  # Recarga la ventana
        else:
            tk.messagebox.showerror("Error", "Dominio o tiempo inválido.")
