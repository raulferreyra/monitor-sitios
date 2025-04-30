import tkinter as tk
from tkinter import messagebox


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("US - Monitor de Sitios")
        self.root.geometry("800x600")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
