import tkinter as tk
import os
import json

from tkinter import messagebox
from utils import Tooltip

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
        # Eliminar tabla anterior si existe
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Encabezados opcionales
        tk.Label(self.table_frame, text="Dominio", font=(
            "Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(self.table_frame, text="Tiempo (s)", font=(
            "Arial", 10, "bold")).grid(row=0, column=1, padx=5)

        for i, row in enumerate(self.data):
            tk.Label(self.table_frame, text=row["dominio"], anchor="w", width=30).grid(
                row=i, column=0, padx=5, sticky="w")
            tk.Label(self.table_frame, text=row["tiempo"], anchor="center", width=10).grid(
                row=i, column=1, padx=5)

            edit_button = tk.Button(
                self.table_frame, text="✏️", command=lambda idx=i: self.edit_entry(idx))
            edit_button.grid(row=i, column=2, padx=5)
            Tooltip(edit_button, "Actualizar dominio")

            delete_button = tk.Button(
                self.table_frame, text="🗑️", command=lambda idx=i: self.delete_entry(idx))
            delete_button.grid(row=i, column=3, padx=5)
            Tooltip(delete_button, "Eliminar dominio")

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
            # Refresh window
            ConfigWindow(self.master.master)
        else:
            tk.messagebox.showerror("Error", "Dominio o tiempo inválido.")

    def delete_entry(self, index):
        confirm = messagebox.askyesno(
            "Confirmar eliminación", "¿Estás seguro de eliminar este dominio?")
        if confirm:
            self.data.pop(index)
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
            self.master.destroy()
            ConfigWindow(self.master.master)

    def edit_entry(self, index):
        # Delete custom widgets in this row
        for widget in self.table_frame.grid_slaves(row=index):
            widget.destroy()

        dominio_actual = self.data[index]["dominio"]
        tiempo_actual = self.data[index]["tiempo"]

        dominio_entry = tk.Entry(self.table_frame, width=30)
        dominio_entry.insert(0, dominio_actual)
        dominio_entry.grid(row=index, column=0, padx=5)

        tiempo_entry = tk.Entry(self.table_frame, width=10)
        tiempo_entry.insert(0, str(tiempo_actual))
        tiempo_entry.grid(row=index, column=1, padx=5)

        save_button = tk.Button(self.table_frame, text="💾", command=lambda: self.save_edit(
            index, dominio_entry.get(), tiempo_entry.get()))
        save_button.grid(row=index, column=2, padx=5)
        Tooltip(save_button, "Guardar")

        cancel_button = tk.Button(
            self.table_frame, text="❌", command=self.refresh_table)
        cancel_button.grid(row=index, column=3, padx=5)
        Tooltip(cancel_button, "Cancelar")

    def save_edit(self, index, dominio, tiempo):
        if dominio and tiempo.isdigit():
            self.data[index] = {
                "dominio": dominio.strip(), "tiempo": int(tiempo.strip())}
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
            self.master.destroy()
            ConfigWindow(self.master.master)
        else:
            messagebox.showerror("Error", "Dominio o tiempo inválido.")
