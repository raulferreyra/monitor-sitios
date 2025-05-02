import tkinter as tk
from TrayManager import TrayManager
from ConfigWindow import ConfigWindow
from DomainMonitor import DomainMonitor
from utils import Tooltip


class App:
    def show_window(self, _=None):
        self.root.after(0, self.root.deiconify)
        self.tray.stop_tray_icon()

    def quit_app(self, _=None):
        self.tray.stop_tray_icon()
        self.root.quit()

    def open_config(self):
        ConfigWindow(self.root)

    def hide_window(self):
        self.root.withdraw()
        self.tray.show_tray_icon()

    def create_widgets(self):
        header = tk.Frame(self.root)
        header.pack(fill=tk.X, pady=10, padx=10)

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)
        header.columnconfigure(2, weight=0)

        title = tk.Label(header, text="Sitios en revisión", font=("Arial", 18))
        title.grid(row=0, column=0, sticky="w")

        refresh_button = tk.Button(header, text="🔄", font=("Arial", 14),
                                   relief="flat", bd=0, command=self.open_config)
        refresh_button.grid(row=0, column=1, padx=5)
        Tooltip(refresh_button, "Actualizar vista")

        config_button = tk.Button(header, text="⚙️", font=("Arial", 14),
                                  relief="flat", bd=0, command=self.open_config)
        config_button.grid(row=0, column=2, padx=5)
        Tooltip(config_button, "Abrir configuración")

        placeholder = tk.Label(
            self.root, text="Aquí se mostrarán los sitios monitoreados.", font=("Arial", 12))
        placeholder.pack(pady=20)

    def __init__(self, root):
        self.root = root
        self.root.title("US - Monitor de Sitios")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.tray = TrayManager(self)
        self.create_widgets()


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("favicon.ico")
    app = App(root)
    root.mainloop()
