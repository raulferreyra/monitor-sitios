import tkinter as tk


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
