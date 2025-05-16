import tkinter as tk
import os
from tkinter import ttk


class AboutWindow(tk.Toplevel):
    """
    A class to create an About window for the application.
    This window displays the application title, version, description,
    and a changelog. The changelog is loaded from a text file.
    """

    def __init__(self, master=None):
        """
        Initializes the About window.
        Args:
            master (tk.Tk): The parent window.
        """
        super().__init__(master)
        self.title("About")
        self.geometry("500x400")
        self.iconbitmap("favicon.ico")
        self.resizable(False, False)

        title_label = tk.Label(
            self, text="Monitor de Sitios - v1.1.0", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        desc = "Monitor your favorite websites and get notified when they change.\nDeveloped by URAS - Elemento\nVisit: https://urasweb.com\nDonate me: https://liberapay.com/elemento/"
        desc_label = tk.Label(self, text=desc, justify="center")
        desc_label.pack(pady=5)

        changelog_label = tk.Label(
            self, text="Changelog:", font=("Arial", 12, "bold"))
        changelog_label.pack(pady=(15, 5))

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
        """
        Loads the changelog from a text file and displays it in the text widget.
        If the file does not exist, a message is displayed.
        The text widget is set to read-only mode after loading the content.
        """
        if os.path.exists("changelog.txt"):
            with open("changelog.txt", "r", encoding="utf-8") as f:
                content = f.read()
                self.text_widget.insert("1.0", content)
        else:
            self.text_widget.insert("1.0", "No changelog available.")
        self.text_widget.config(state="disabled")
