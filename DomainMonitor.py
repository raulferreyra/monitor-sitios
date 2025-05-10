import json
import requests
import threading
import time
import tkinter as tk
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

    def view_domain(url, time, update_callback, log_callback):
        """
        Monitors a domain and updates the GUI with the status.
        Args:
            url (str): The URL of the domain to monitor.
            time (int): The time interval for monitoring in seconds.
            update_callback (function): Callback function to update the GUI.
            log_callback (function): Callback function to log errors.
        """
        while True:
            try:
                response = requests.get(url, timeout=time)
                status = response.status_code

                if status <= status < 300:
                    update_callback(url, status, "green", "OK ✅")
                else:
                    error_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {url} Error {status}: {response.reason}"
                    update_callback(url, status, "red", f"Error: ❌ ({status})")
                    log_callback(error_msg)

            except requests.RequestException as e:
                error_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {url} {type(e).__name__}: {str(e)}"
                update_callback(url, None, "red", f"Error.")
                log_callback(error_msg)

            time.sleep(time)

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

    def log_error(self, domain, status_code, reason):
        """
        Logs errors to the error file.
        Args:
            domain (str): The domain that caused the error.
            status_code (int): The HTTP status code received.
            reason (str): The reason for the error.
        """
        error_entry = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dominio": domain,
            "error": f"{status_code} - {reason}"
        }

        try:
            with open(self.error_path, "r") as f:
                errores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            errores = []
        errores.append(error_entry)

        with open(self.error_path, "w") as f:
            json.dump(errores, f, indent=4)

    def setup_tree(self):
        """
        Sets up the Treeview widget for displaying monitored domains.
        This method creates the Treeview widget and populates it with the monitored domains.
        """
        self.tree = ttk.Treeview(self.parent)
        self.tree.heading("#0", text="Dominios monitoreados")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.reload()

    def reload(self):
        """
        Reloads the domain list and updates the Treeview.
        """
        self.domains = self.load_domains()
        for item in self.tree.get_children():
            self.tree.delete(item)

        for domain in self.domains:
            url = domain.get("dominio", "Desconocido")
            tiempo = int(domain.get("tiempo", 5))
            display_text = f"{url} ({tiempo}s)"

            try:
                response = requests.get(url, timeout=tiempo)
                status = response.status_code

                if status == 200:
                    color = "green"
                    display_text += " ✅"
                else:
                    color = "red"
                    display_text += f" ❌ ({status})"
                    self.log_error(url, status, response.reason)

            except requests.RequestException as e:
                color = "red"
                display_text += f" ❌ ({str(e)})"
                self.log_error(url, "Error", str(e))

            node = self.tree.insert("", tk.END, text=display_text)
            self.tree.item(node, tags=(color,))

        self.tree.tag_configure("green", foreground="green")
        self.tree.tag_configure("red", foreground="red")
