import json
import tkinter as tk
import requests
from tkinter import ttk
from datetime import datetime


class DomainMonitor:
    """
    Class for monitoring domains in a Tkinter application.
    This class provides a GUI for displaying monitored domains and their times.
    """

    def __init__(self, parent, config_path="config.json", error_path="error.json"):
        """
        Initializes the DomainMonitor class.
        Args:
            parent (tk.Tk): The parent Tkinter window.
            config_path (str): Path to the configuration file containing monitored domains.
            error_path (str): Path to the error file for logging errors.
        """
        self.parent = parent
        self.config_path = config_path
        self.error_path = error_path
        self.tree = None
        self.domains = self.load_domains()
        self.setup_tree()

    def load_domains(self):
        """
        Loads the monitored domains from the configuration file.
        Returns:
            list: A list of dictionaries containing domain information.
        """
        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error cargando dominios: {e}")
            return []

    def setup_tree(self):
        """
        Sets up the Treeview widget for displaying monitored domains.
        This method creates the Treeview widget and populates it with the monitored domains.
        """
        self.tree = ttk.Treeview(self.parent)
        self.tree.heading("#0", text="Dominios monitoreados")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for domain in self.domains:
            url = domain.get("dominio", "Desconocido")
            tiempo = domain.get("tiempo", "?")
            self.tree.insert("", tk.END, text=f"{url} ({tiempo}s)")

    def reload(self):
        """
        Reloads the domain list and updates the Treeview.
        """
        self.domains = self.load_domains()
        for item in self.tree.get_children():
            self.tree.delete(item)

        for domain in self.domains:
            url = domain.get("dominio", "Desconocido")
            tiempo = domain.get("tiempo", "?")
            self.tree.insert("", tk.END, text=f"{url} ({tiempo}s)")
