import tkinter as tk
import json
import os


class ErrorLogWindow(tk.Toplevel):
    """
    A class to create a window that displays the error log of the application.
    This window shows the date, domain, and error message for each entry in the log.
    The log is loaded from a JSON file named "error.json".
    """

    def __init__(self, master=None):
        """
        Initializes the ErrorLog window.
        Args:
            master (tk.Tk): The parent window.
        """
        super().__init__(master)
        self.title("Registro de Errores")
        self.geometry("600x400")
        self.resizable(True, True)

        title_label = tk.Label(
            self, text="Registro de Errores", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.text = tk.Text(frame, wrap="none", yscrollcommand=scrollbar.set)
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text.yview)

        self.load_errors()

    def load_errors(self):
        """
        Loads the error log from a JSON file and displays it in the text widget.
        If the file does not exist or is empty, a message is displayed.
        The text widget is set to read-only mode after loading the content.
        """

        if not os.path.exists("error.json"):
            self.text.insert("1.0", "No hay errores registrados.")
            return

        try:
            with open("error.json", "r", encoding="utf-8") as f:
                errors = json.load(f)
            if not errors:
                self.text.insert("1.0", "No hay errores registrados.")
                return

            header = f"{'Fecha y Hora':<22} | {'Dominio':<50} | Error\n"
            self.text.insert("1.0", header)
            self.text.insert("2.0", "-" * 100 + "\n")

            for entry in errors:
                line = f"{entry['fecha']:<22} | {entry['dominio'][:48]:<50} | {entry['error']}\n"
                self.text.insert("end", line)
        except Exception as e:
            self.text.insert("1.0", f"Error leyendo archivo de errores: {e}")
        self.text.config(state="disabled")
