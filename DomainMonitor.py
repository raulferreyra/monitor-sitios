import json
import tkinter as tk
from tkinter import ttk


class DomainMonitor:
    def __init__(self, parent, config_path="config.json"):
        self.parent = parent
        self.config_path = config_path
        self.tree = None
        self.domains = self.load_domains()
        self.setup_tree()

    def load_domains(self):
        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error cargando dominios: {e}")
            return []

    def setup_tree(self):
        self.tree = ttk.Treeview(self.parent)
        self.tree.heading("#0", text="Dominios monitoreados")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for domain in self.domains:
            url = domain.get("dominio", "Desconocido")
            tiempo = domain.get("tiempo", "?")
            self.tree.insert("", tk.END, text=f"{url} ({tiempo}s)")
