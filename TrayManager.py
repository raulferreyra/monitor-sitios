import pystray
from PIL import Image
from pystray import MenuItem as item


class TrayManager:
    def __init__(self, app, icon_path="favicon.png"):
        self.app = app
        self.tray_icon = None
        self.icon_image = None

        try:
            self.icon_image = Image.open(icon_path)
        except Exception as e:
            print("Error cargando el icono:", e)

    def show_tray_icon(self):
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
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
