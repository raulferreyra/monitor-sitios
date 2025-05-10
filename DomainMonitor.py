import json
import requests
import threading
import time
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import ttk
from datetime import datetime
from urllib.parse import urljoin


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
        self.tree_items = {}
        self.tree_subitems = {}
        self.setup_tree()
        self.start_monitoring_threads()
        self.threads = []
        self.stop_threads = False

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

        for domain in self.domains:
            url = domain.get("dominio", "Desconocido")
            tiempo = int(domain.get("tiempo", 60))
            display_text = f"{url} ({tiempo}s)"
            parent = self.tree.insert(
                "", tk.END, text=display_text, tags=("gray",))
            child_status = self.tree.insert(
                parent, tk.END, text="Estado HTTP: ---")
            child_fecha = self.tree.insert(
                parent, tk.END, text="Última verificación: ---")
            child_tiempo = self.tree.insert(
                parent, tk.END, text="Tiempo de respuesta: ---")

            self.tree_items[url] = parent
            self.tree_subitems[url] = {
                "estado": child_status,
                "fecha": child_fecha,
                "tiempo": child_tiempo
            }

        self.tree.tag_configure("green", foreground="green")
        self.tree.tag_configure("red", foreground="red")
        self.tree.tag_configure("gray", foreground="gray")

    def start_monitoring_threads(self):
        """
        Starts monitoring threads for each domain.
        This method creates a thread for each domain to monitor its status.
        """
        self.stop_threads = False
        for domain in self.domains:
            url = domain.get("dominio", "Desconocido")
            tiempo = int(domain.get("tiempo", 60))
            thread = threading.Thread(
                target=self.monitor_domain,
                args=(url, tiempo),
                daemon=True
            )
            self.threads.append(thread)
            thread.start()

    def monitor_domain(self, url, tiempo):
        """
        Monitors a domain and updates its status in the Treeview.
        Args:
            url (str): The domain to monitor.
            tiempo (int): The time interval for monitoring the domain.
        """
        while True:
            try:
                response = requests.get(url, timeout=tiempo)
                status = response.status_code

                if status == 200:
                    color = "green"
                    display_text = f"{url} ({tiempo}s) ✅"
                else:
                    color = "red"
                    display_text = f"{url} ({tiempo}s) ❌ ({status})"
                    self.log_error(url, status, response.reason)

            except requests.RequestException as e:
                color = "red"
                display_text = f"{url} ({tiempo}s) ❌ ({str(e)})"
                self.log_error(url, "Error", str(e))

            self.tree.item(self.tree_items[url],
                           text=display_text, tags=(color,))
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tiempo_ms = int(response.elapsed.total_seconds() * 1000)
            status_text = f"{status} {response.reason}"

            self.update_subitems(url, status_text, fecha, tiempo_ms)
            time.sleep(tiempo)

    def update_tree(self, url, text, color):
        """
        Updates the Treeview widget.
        This method refreshes the Treeview to reflect any changes in monitored domains.
        """
        item_id = self.tree_items.get(url)
        if item_id:
            self.tree.item(item_id, text=text, tags=(color,))
        else:
            print(f"Error: No se encontró el dominio {url} en el Treeview.")

    def reload(self):
        """
        Reloads the monitored domains from the configuration file.
        This method clears the current Treeview and repopulates it with the updated domains.

        ADITIONAL NOTE:
        This method is called when the user wants to refresh the monitored domains.
        Only call this method in the Main class, not in the DomainMonitor class.
        """
        self.stop_threads = True
        self.threads = []

        self.domains = self.load_domains()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree_items.clear()

        for domain in self.domains:
            url = domain.get("dominio", "Desconocido")
            tiempo = int(domain.get("tiempo", 5))
            display_text = f"{url} ({tiempo}s)"
            parent = self.tree.insert(
                "", tk.END, text=display_text, tags=("gray",))
            child_status = self.tree.insert(
                parent, tk.END, text="Estado HTTP: ---")
            child_fecha = self.tree.insert(
                parent, tk.END, text="Última verificación: ---")
            child_tiempo = self.tree.insert(
                parent, tk.END, text="Tiempo de respuesta: ---")

            self.tree_items[url] = parent
            self.tree_subitems[url] = {
                "estado": child_status,
                "fecha": child_fecha,
                "tiempo": child_tiempo
            }

        self.start_monitoring_threads()

    def update_subitems(self, url, status_text, fecha, response_time):
        """
        Updates the subitems of a domain in the Treeview.
        Args:
            url (str): The domain to update.
            status_text (str): The HTTP status text to display.
            fecha (str): The last check date to display.
            response_time (str): The response time to display.
        """
        hijos = self.tree_subitems.get(url)
        if hijos:
            self.tree.item(hijos["estado"], text=f"Estado HTTP: {status_text}")
            self.tree.item(
                hijos["fecha"], text=f"Última verificación: {fecha}")
            self.tree.item(
                hijos["tiempo"], text=f"Tiempo de respuesta: {response_time} ms")
