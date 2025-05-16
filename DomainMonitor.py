import json
import requests
import threading
import time
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import ttk
from datetime import datetime
from urllib.parse import urljoin, urlparse


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
        self.threads = []
        self.stop_threads = False
        self.setup_tree()
        self.start_monitoring_threads()

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
        container = ttk.Frame(self.parent)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        vsb = ttk.Scrollbar(container, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            container,
            columns=("estado", "fecha", "tiempo"),
            show="tree headings",
            height=20,
            yscrollcommand=vsb.set,
        )

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.config(command=self.tree.yview)

        total_width = 550
        self.tree.column("#0", width=int(
            total_width * 0.40), anchor="w")  # URL
        self.tree.column("estado", width=int(
            total_width * 0.10), anchor="center")
        self.tree.column("fecha", width=int(
            total_width * 0.40), anchor="center")
        self.tree.column("tiempo", width=int(
            total_width * 0.10), anchor="center")

        self.tree.heading("#0", text="URL")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("fecha", text="Última actualización")
        self.tree.heading("tiempo", text="Tiempo de respuesta")

        for domain in self.domains:
            url = domain.get("dominio", "Desconocido")
            tiempo = int(domain.get("tiempo", 60))
            item_id = self.tree.insert("", tk.END, text=url, values=(
                "---", "---", "---"), tags=("black",))
            self.tree_items[url] = item_id

        self.tree.tag_configure("green", foreground="green")
        self.tree.tag_configure("red", foreground="red")
        self.tree.tag_configure("yellow", foreground="orange")
        self.tree.tag_configure("black", foreground="black")

    def update_parent_color(self, parent_id):
        """
        Updates the color of the parent node based on its children.
        Green: all children green
        Red: all children red or error
        Yellow: mixed colors
        Black: no children or all loading

        Args:
            parent_id (str): The ID of the parent node in the Treeview.
        """
        children = self.tree.get_children(parent_id)
        colors = set()
        for child in children:
            tags = self.tree.item(child, "tags")
            if tags:
                colors.update(tags)

        new_tag = "black"
        if colors:
            if all(tag == "green" for tag in colors):
                new_tag = "green"
            elif all(tag == "red" for tag in colors):
                new_tag = "red"
            elif "green" in colors and "red" in colors:
                new_tag = "yellow"
            elif all(tag == "black" for tag in colors):
                new_tag = "black"
            else:
                new_tag = "yellow"

        self.tree.item(parent_id, tags=(new_tag,))

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
        while not self.stop_threads:
            try:
                response = requests.get(url, timeout=tiempo)
                status = response.status_code
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tiempo_ms = int(response.elapsed.total_seconds() * 1000)
                estado = "Ok" if status == 200 else f"{status} {response.reason}"
                color = "green" if status == 200 else "red"

                self.tree.item(self.tree_items[url], values=(
                    estado, fecha, f"{tiempo_ms} ms"), tags=(color,))
                self.update_parent_color(self.tree_items[url])
                if status != 200:
                    self.log_error(url, status, response.reason)
                    self.update_parent_color(self.tree_items[url])

                if status == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    links = soup.find_all("a", href=True)
                    base_url = url.rstrip('/')
                    base_domain = urlparse(base_url).netloc
                    for link in links:
                        href = link['href']
                        if any(s in href for s in ['#', '?']) or href.startswith(('mailto:', 'tel:')):
                            continue

                        full_url = urljoin(base_url + '/', href)
                        parsed_url = urlparse(full_url)
                        if parsed_url.netloc and parsed_url.netloc != base_domain:
                            continue

                        path = parsed_url.path
                        if not path.startswith("/"):
                            continue

                        child_url = base_url + path
                        if child_url == url:
                            continue

                        try:
                            sub_response = requests.get(child_url, timeout=10)
                            sub_status = sub_response.status_code
                            sub_fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            sub_tiempo = int(
                                sub_response.elapsed.total_seconds() * 1000)
                            sub_estado = "Ok" if sub_status == 200 else f"{sub_status} {sub_response.reason}"
                            sub_color = "green" if sub_status == 200 else "red"

                            exists = False
                            for item in self.tree.get_children(self.tree_items[url]):
                                if self.tree.item(item, "text") == path:
                                    exists = True
                                    self.tree.item(item, values=(
                                        sub_estado, sub_fecha, f"{sub_tiempo} ms"), tags=(sub_color,))
                                    self.update_parent_color(
                                        self.tree_items[url])
                                    break

                            if not exists:
                                new_id = self.tree.insert(
                                    self.tree_items[url],
                                    tk.END,
                                    text=path,
                                    values=(sub_estado, sub_fecha,
                                            f"{sub_tiempo} ms"),
                                    tags=(sub_color,)
                                )

                                children = list(
                                    self.tree.get_children(self.tree_items[url]))
                                sorted_children = sorted(
                                    children, key=lambda c: self.tree.item(c, "text"))

                                for idx, child in enumerate(sorted_children):
                                    self.tree.move(
                                        child, self.tree_items[url], idx)

                                self.update_parent_color(self.tree_items[url])

                        except requests.RequestException as e:
                            error_fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            self.tree.insert(
                                self.tree_items[url],
                                tk.END,
                                text=path,
                                values=("Error", error_fecha, "N/A"),
                                tags=("red",)
                            )
                            self.log_error(child_url, "Error", str(e))
                            self.update_parent_color(self.tree_items[url])

            except requests.RequestException as e:
                error_fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.tree.insert(
                    self.tree_items[url],
                    tk.END,
                    text=path,
                    values=("Error", error_fecha, "N/A"),
                    tags=("red",)
                )
                self.log_error(child_url, "Error", str(e))

            time.sleep(tiempo)

    def update_tree(self, url, text, color):
        """
        Updates the Treeview widget.
        This method refreshes the Treeview to reflect any changes in monitored domains.
        """
        item_id = self.tree_items.get(url)
        if item_id:
            self.tree.item(item_id, text=text, tags=(color,))
            self.update_parent_color(self.tree_items[url])
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

        self.start_monitoring_threads()
