import tkinter as tk
from tkinter import ttk
import os


class AboutWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("About")
        self.geometry("500x400")
        self.resizable(False, False)

        # Title
        title_label = tk.Label(
            self, text="Monitor de Sitios - v1.1.0", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Description
        desc = "Monitor your favorite websites and get notified when they change.\nDeveloped by URAS - Elemento\nVisit: https://urasweb.com"
        desc_label = tk.Label(self, text=desc, justify="center")
        desc_label.pack(pady=5)

        # Changelog
        changelog_label = tk.Label(
            self, text="Changelog:", font=("Arial", 12, "bold"))
        changelog_label.pack(pady=(15, 5))

        # Scrollable changelog viewer
        changelog_frame = tk.Frame(self)
        changelog_frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(changelog_frame, orient="vertical")
        self.text_widget = tk.Text(
            changelog_frame, wrap="word", yscrollcommand=scrollbar.set, height=10)
        scrollbar.config(command=self.text_widget.yview)

        self.text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_changelog()

    def load_changelog(self):
        if os.path.exists("changelog.txt"):
            with open("changelog.txt", "r", encoding="utf-8") as f:
                content = f.read()
                self.text_widget.insert("1.0", content)
        else:
            self.text_widget.insert("1.0", "No changelog available.")
        self.text_widget.config(state="disabled")
