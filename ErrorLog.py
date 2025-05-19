import tkinter as tk
import json
import os
import csv
import xlwt
from utils import IconManager, Tooltip
from tkinter import filedialog, messagebox


class ErrorLogWindow(tk.Toplevel):
    """
    A class to create a window that displays the error log of the application.
    This window shows the date, domain, and error message for each entry in the log.
    The log is loaded from a JSON file named "error.json".
    The window contains a text widget with horizontal and vertical scrollbars
    """

    def __init__(self, master=None):
        """
        Initializes the ErrorLog window.
        Args:
            master (tk.Tk): The parent window.
        """

        super().__init__(master)
        self.title("Registro de Errores")
        self.geometry("800x400")
        self.iconbitmap(IconManager.resource_path("favicon.ico"))
        self.resizable(False, False)

        header = tk.Frame(self)
        header.pack(fill=tk.X, pady=10, padx=10)

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)
        header.columnconfigure(2, weight=0)

        title_label = tk.Label(
            header, text="Registro de Errores", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, sticky="w")

        csv_button = tk.Button(header, text="📄", font=("Arial", 14),
                               relief="flat", bd=0, command=self.export_to_csv)
        csv_button.grid(row=0, column=1, padx=5)
        Tooltip(csv_button, "Exportar a CSV")

        xls_button = tk.Button(header, text="📊", font=("Arial", 14),
                               relief="flat", bd=0, command=self.export_to_xls)
        xls_button.grid(row=0, column=2, padx=5)
        Tooltip(xls_button, "Exportar a XLS")

        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        y_scrollbar = tk.Scrollbar(frame, orient="vertical")
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = tk.Scrollbar(frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        self.text = tk.Text(
            frame,
            wrap="none",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        self.text.pack(side="left", fill="both", expand=True)

        y_scrollbar.config(command=self.text.yview)
        x_scrollbar.config(command=self.text.xview)

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

            header = f"{'Fecha y Hora':<22} | {'Dominio':<60} | Error\n"
            self.text.insert("1.0", header)
            self.text.insert("2.0", "-" * 120 + "\n")

            for entry in errors:
                line = f"{entry['fecha']:<22} | {entry['dominio']:<60} | {entry['error']}\n"
                self.text.insert("end", line)
        except Exception as e:
            self.text.insert("1.0", f"Error leyendo archivo de errores: {e}")
        self.text.config(state="disabled")

    def export_to_csv(self):
        """
        Exports the error log to a CSV file.
        The CSV file is named "error_log.csv" and is saved in the current directory.
        The user is prompted to choose the save location and file name.
        If the error log file does not exist or is empty, a warning message is displayed.
        """
        try:
            if not os.path.exists("error.json"):
                messagebox.showwarning(
                    "Advertencia", "No hay registros para exportar.")
                return

            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv")],
                title="Guardar como..."
            )
            if not filepath:
                return  # El usuario canceló

            with open("error.json", "r", encoding="utf-8") as f:
                errors = json.load(f)

            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Fecha", "Dominio", "Error"])
                for entry in errors:
                    writer.writerow(
                        [entry["fecha"], entry["dominio"], entry["error"]])

            messagebox.showinfo(
                "Éxito", f"Archivo CSV exportado correctamente:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a CSV:\n{e}")

    def export_to_xls(self):
        """
        Exports the error log to a XLS file.
        The XLS file is named "error_log.xls" and is saved in the current directory.
        The user is prompted to choose the save location and file name.
        If the error log file does not exist or is empty, a warning message is displayed.
        """
        try:
            if not os.path.exists("error.json"):
                messagebox.showwarning(
                    "Advertencia", "No hay registros para exportar.")
                return

            filepath = filedialog.asksaveasfilename(
                defaultextension=".xls",
                filetypes=[("Archivos Excel 97-2003", "*.xls")],
                title="Guardar como..."
            )
            if not filepath:
                return  # El usuario canceló

            with open("error.json", "r", encoding="utf-8") as f:
                errors = json.load(f)

            wb = xlwt.Workbook()
            ws = wb.add_sheet("Errores")

            ws.write(0, 0, "Fecha")
            ws.write(0, 1, "Dominio")
            ws.write(0, 2, "Error")

            for i, entry in enumerate(errors, start=1):
                ws.write(i, 0, entry["fecha"])
                ws.write(i, 1, entry["dominio"])
                ws.write(i, 2, entry["error"])

            wb.save(filepath)
            messagebox.showinfo(
                "Éxito", f"Archivo XLS exportado correctamente:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a XLS:\n{e}")
