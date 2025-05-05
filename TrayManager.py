import pystray
from PIL import Image
from pystray import MenuItem as item


class TrayManager:
    """
    Class for managing the system tray icon in a Tkinter application.
    This class provides methods to show and hide the tray icon,
    as well as to handle click events on the icon.
    """

    def __init__(self, app, icon_path="favicon.png"):
        """
        Initializes the TrayManager class.
        Args:
            app (App): Reference to the main application instance.
            icon_path (str): Path to the icon image file.
        """
        self.app = app
        self.tray_icon = None
        self.icon_image = None

        try:
            self.icon_image = Image.open(icon_path)
        except Exception as e:
            print("Error cargando el icono:", e)

    def show_tray_icon(self):
        """
        Shows the tray icon in the system tray.
        This method creates the tray icon and sets up the menu items.
        """
        if self.tray_icon is None and self.icon_image:
            menu = pystray.Menu(
                item("Restaurar", self.app.show_window),
                item("Salir", self.app.quit_app)
            )
            self.tray_icon = pystray.Icon(
                "us_monitor",
                self.icon_image,
                "US - Monitor de Sitios",
                menu,
                on_click=self.app.show_window
            )
            self.tray_icon.run_detached()

    def stop_tray_icon(self):
        """
        Stops the tray icon and removes it from the system tray.
        This method is called when the application is closed or exited.
        """
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
