import tkinter as tk
from TrayManager import TrayManager
from ConfigWindow import ConfigWindow
from DomainMonitor import DomainMonitor
from utils import Tooltip

# =========================
# Monitor de Sitios v0.1.a
# =========================
__version__ = "0.1.a"
__project_name__ = "Monitor de Sitios"
__author__ = "URAS - Elemento"
__license__ = "MIT"
# =========================
# =========================


class App:
    """
    Main application class for the Tkinter GUI.
    This class initializes the main window, creates the tray icon,
    and manages the application lifecycle.
    """

    def show_window(self, _=None):
        """
        Shows the main window when the tray icon is clicked.
        This method is called when the user clicks on the tray icon.
        It restores the main window and stops the tray icon.
        """
        self.root.after(0, self.root.deiconify)
        self.tray.stop_tray_icon()

    def quit_app(self, _=None):
        """
        Quits the application when the user selects "Quit" from the tray icon menu.
        This method is called when the user selects "Quit" from the tray icon menu.
        """
        self.tray.stop_tray_icon()
        self.root.quit()

    def reload_monitor(self):
        """
        Reloads the domain monitor when the user clicks the refresh button.
        This method is called when the user clicks the refresh button in the main window.
        """
        DomainMonitor(self.root, self.domain_monitor.config_path).reload()

    def open_config(self):
        """
        Opens the configuration window when the user clicks the config button.
        This method is called when the user clicks the config button in the main window.
        """
        ConfigWindow(self.root, self.domain_monitor)

    def hide_window(self):
        """
        Hides the main window when the user closes it.
        This method is called when the user closes the main window.
        It hides the window and shows the tray icon.
        """
        self.root.withdraw()
        self.tray.show_tray_icon()

    def create_widgets(self):
        """
        Creates the main widgets for the application.
        This method creates the header, refresh button, config button,
        and the domain monitor widget.
        """
        header = tk.Frame(self.root)
        header.pack(fill=tk.X, pady=10, padx=10)

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)
        header.columnconfigure(2, weight=0)

        title = tk.Label(header, text="Sitios en revisión", font=("Arial", 18))
        title.grid(row=0, column=0, sticky="w")

        refresh_button = tk.Button(header, text="🔄", font=("Arial", 14),
                                   relief="flat", bd=0, command=self.reload_monitor)
        refresh_button.grid(row=0, column=1, padx=5)
        Tooltip(refresh_button, "Actualizar vista")

        config_button = tk.Button(header, text="⚙️", font=("Arial", 14),
                                  relief="flat", bd=0, command=self.open_config)
        config_button.grid(row=0, column=2, padx=5)
        Tooltip(config_button, "Abrir configuración")

        self.domain_monitor = DomainMonitor(self.root)

    def __init__(self, root):
        """
        Initializes the main application class.
        Args:
            root (tk.Tk): The main Tkinter window.
        """
        self.root = root
        self.root.title("US - Monitor de Sitios")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.tray = TrayManager(self)
        self.create_widgets()


if __name__ == "__main__":
    """
    Main function to run the application.
    This function creates the main Tkinter window and starts the application.
    """
    root = tk.Tk()
    root.iconbitmap("favicon.ico")
    app = App(root)
    root.mainloop()
