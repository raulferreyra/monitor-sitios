import tkinter as tk
from tkinter import messagebox


class App:
    def open_config(self):
        # This method will replace the configuration modal
        messagebox.showinfo(
            "Configuración", "Aquí irá la ventana de configuración.")

    def hide_window(self):
        # Hide Main Window
        self.root.withdraw()

    def create_widgets(self):
        # Welcome Label
        title = tk.Label(
            self.root, text="Sitios en revisión", font=("Arial", 18))
        title.pack(pady=20)

        # Button for open conf
        config_button = tk.Button(
            self.root, text="⚙️", font=(14), command=self.open_config)
        config_button.pack(pady=10)

        # Button for refresh
        config_button = tk.Button(
            self.root, text="🪄", font=(14), command=self.open_config)
        config_button.pack(pady=10)

        # Placeholder for table
        placeholder = tk.Label(
            self.root, text="Aquí se mostrarán los sitios monitoreados.", font=("Arial", 12))
        placeholder.pack(pady=20)

    def __init__(self, root):
        self.root = root
        self.root.title("US - Monitor de Sitios")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.create_widgets()


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("favicon.ico")
    app = App(root)
    root.mainloop()
