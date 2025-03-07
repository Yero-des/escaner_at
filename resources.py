
import sys
import os
def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def resource_path(relative_path):
    """Encuentra el recurso empaquetado o en el directorio de desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Carga el icono usando la ruta adaptada
icon_path = resource_path("img/apuesta_total.ico")
img_path = resource_path("img/logo_apuesta_total.png")