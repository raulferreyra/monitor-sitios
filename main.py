import tkinter as tk
import threading
import pystray
from PIL import Image
from tkinter import messagebox


class App:
    def show_window(self, _=None):
        self.root.after(0, self.root.deiconify)
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None

    def quit_app(self, _=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()

    def show_tray_icon(self):
        if self.tray_icon is None:
            menu = pystray.Menu(
                pystray.MenuItem("Restaurar", self.show_window),
                pystray.MenuItem("Salir", self.quit_app)
            )
            self.tray_icon = pystray.Icon(
                "us_monitor", self.icon_image, "US - Monitor de Sitios", menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def open_config(self):
        # This method will replace the configuration modal
        messagebox.showinfo(
            "Configuración", "Aquí irá la ventana de configuración.")

    def hide_window(self):
        # Hide Main Window
        self.root.withdraw()
        if not hasattr(self, 'tray_icon') or self.tray_icon is None:
            self.show_tray_icon()

    def create_widgets(self):
        # Up container with grid
        header = tk.Frame(self.root)
        header.pack(fill=tk.X, pady=10, padx=10)

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)
        header.columnconfigure(2, weight=0)

        # Welcome Label
        title = tk.Label(header, text="Sitios en revisión", font=("Arial", 18))
        title.grid(row=0, column=0, sticky="w")

        # Button for refresh
        refresh_button = tk.Button(
            header, text="🪄", font=("Arial", 14), relief="flat", bd=0, command=self.open_config
        )
        refresh_button.grid(row=0, column=1, padx=5)

        # Button for open conf
        config_button = tk.Button(
            header, text="⚙️", font=("Arial", 14), relief="flat", bd=0, command=self.open_config
        )
        config_button.grid(row=0, column=2)

        # Placeholder for table
        placeholder = tk.Label(
            self.root, text="Aquí se mostrarán los sitios monitoreados.", font=("Arial", 12))
        placeholder.pack(pady=20)

    def __init__(self, root):
        self.root = root
        self.root.title("US - Monitor de Sitios")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.tray_icon = None
        try:
            self.icon_image = Image.open("favicon.png")
        except Exception as e:
            print("Error cargando el icono:", e)
            self.icon_image = None

        self.create_widgets()


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("favicon.ico")
    app = App(root)
    root.mainloop()
