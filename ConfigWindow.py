import tkinter as tk
import os
import json

from tkinter import messagebox
from utils import Tooltip

CONFIG_FILE = "config.json"


class ConfigWindow:
    """
    Class for configuring monitored domains in a Tkinter application.
    This class provides a GUI for adding, editing, and deleting monitored domains.
    """

    def __init__(self, master, domain_monitor=None):
        """
        Initializes the ConfigWindow class.
        Args:
            master (tk.Tk): The parent Tkinter window.
            domain_monitor (DomainMonitor): Reference to the domain monitor instance.
        """
        self.master = tk.Toplevel(master)
        self.master.title("Configuración de Sitios")
        self.master.geometry("500x400")
        self.data = []
        self.domain_monitor = domain_monitor

        self.load_config()
        self.create_table()

    def load_config(self):
        """
        Loads the configuration from the JSON file.
        """
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w") as f:
                json.dump([], f)

        with open(CONFIG_FILE, "r") as f:
            try:
                self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = []

    def create_table(self):
        """
        Creates the table for displaying monitored domains and their times.
        This method also creates the form for adding new domains.
        """
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        if hasattr(self, "form_frame"):
            self.form_frame.destroy()

        self.table_frame = tk.Frame(self.master)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

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
        self.form_frame = tk.Frame(self.master)
        self.form_frame.pack(pady=20)

        tk.Label(self.form_frame, text="Dominio:").grid(
            row=0, column=0, padx=5)
        self.new_domain_entry = tk.Entry(self.form_frame, width=30)
        self.new_domain_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.form_frame, text="Tiempo (s):").grid(
            row=0, column=2, padx=5)
        self.new_time_entry = tk.Entry(self.form_frame, width=10)
        self.new_time_entry.grid(row=0, column=3, padx=5)

        add_button = tk.Button(
            self.form_frame, text="Guardar", command=self.add_entry)
        add_button.grid(row=0, column=4, padx=5)

    def add_entry(self):
        """
        Adds a new domain entry to the configuration file.
        This method validates the input and checks for duplicates before saving.
        """
        dominio = self.new_domain_entry.get().strip()
        tiempo = self.new_time_entry.get().strip()

        if not dominio or not tiempo.isdigit():
            tk.messagebox.showerror("Error", "Dominio o tiempo inválido.")
            return

        if any(d["dominio"].lower().strip() == dominio.lower() for d in self.data):
            tk.messagebox.showwarning(
                "Duplicado", "Este dominio ya está en la lista.")
            return

        self.data.append({"dominio": dominio, "tiempo": int(tiempo)})
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.data, f, indent=4)
        self.refresh_table()

    def delete_entry(self, index):
        """
        Deletes a domain entry from the configuration file.
        This method prompts the user for confirmation before deleting.  
        Args:
            index (int): The index of the domain entry to delete.
        """
        confirm = messagebox.askyesno(
            "Confirmar eliminación", "¿Estás seguro de eliminar este dominio?")
        if confirm:
            self.data.pop(index)
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
            self.refresh_table()

    def edit_entry(self, index):
        """
        Edits an existing domain entry in the configuration file.
        This method allows the user to modify the domain and time values.
        Args:
            index (int): The index of the domain entry to edit.
        """
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
        """
        Saves the edited domain entry to the configuration file.
        This method validates the input and checks for duplicates before saving.
        Args:
            index (int): The index of the domain entry to edit.
            dominio (str): The new domain value.
            tiempo (str): The new time value.
        """
        dominio = dominio.strip()
        tiempo = tiempo.strip()

        if not dominio or not tiempo.isdigit():
            messagebox.showerror("Error", "Dominio o tiempo inválido.")
            return

        # Check for duplicates
        for i, d in enumerate(self.data):
            if i != index and d["dominio"].lower() == dominio.lower():
                messagebox.showwarning(
                    "Duplicado", "Ya existe otro dominio con ese nombre.")
                return

        self.data[index] = {"dominio": dominio, "tiempo": int(tiempo)}
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.data, f, indent=4)
        self.refresh_table()

    def refresh_table(self):
        """
        Refreshes the table to reflect the current configuration.
        This method clears the existing table and re-creates it with updated data.
        """
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()
        if hasattr(self, "form_frame"):
            self.form_frame.destroy()
        self.create_table()

        if self.domain_monitor:
            self.domain_monitor.reload()
