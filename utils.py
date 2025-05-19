import os
import requests
import sys
import tkinter as tk
import webbrowser
from tkinter import messagebox


class UpdateChecker:
    """
    Class for checking for updates in a Tkinter application.
    This class reads a remote version.json file to check for updates.
    """

    def __init__(self, current_version):
        self.check_for_updates(current_version)

    def check_for_updates(self, current_version):
        """
        Checks for updates by reading a remote version.json file.

        Args:
            current_version (str): Current app version.
        """
        try:
            version_url = "https://monitor.urasweb.com/version.json"

            response = requests.get(version_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                latest = data.get("latest_version", "")
                changelog = data.get("changelog", "")
                download_url = data.get("download_url", "")

                if latest != current_version:
                    message = (
                        f"Hay una nueva versión disponible: {latest}\n\n"
                        f"Registro de cambios:\n{changelog}\n\n"
                        f"¿Deseas ir a la página de descarga?"
                    )
                    if messagebox.askyesno("Actualización disponible", message):
                        webbrowser.open(download_url)
                else:
                    print("[Monitor de Sitios] Ya tienes la última versión.")
            else:
                print(
                    f"[Monitor de Sitios] No se pudo verificar actualizaciones. Código: {response.status_code}")

        except Exception as e:
            print(
                f"[Monitor de Sitios] Error al verificar actualizaciones: {e}")


class IconManager:
    """
    Class for managing the application icon in the system tray.
    This class handles the creation and management of the system tray icon.
    """

    def resource_path(relative_path):
        """
        Get the absolute path to the resource, works for dev and PyInstaller.
        Args:
            relative_path (str): The relative path to the resource.
        """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


class Tooltip:
    """
    Class for creating tooltips for widgets in a Tkinter application.
    """

    def __init__(self, widget, text):
        """
        Args:
            widget (widget): Widget to which the tooltip will be attached.
            text (str): Text to be displayed in the tooltip.
        """
        self.widget = widget
        self.text = text
        self.tooltip = None

        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """
        shows the tooltip when the mouse enters the widget.

        Args:
            event (tk.Event): Event object containing information about the event.
        """
        if self.tooltip or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text,
                         background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        """
        Hides the tooltip when the mouse leaves the widget.

        Args:
            event (tk.Event): Event object containing information about the event.
        """
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
