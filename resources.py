
import sys
import os
def centrar_ventana(ventana, ancho, alto):

    # Obtener medidas de pantalla
    screen_width = ventana.winfo_screenwidth()

    # Calcular posición centrada
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def centrar_ventana_hija(ventana, ancho, alto, padre):

    # Obtener la posición de la ventana padre
    padre_x = padre.winfo_rootx()
    padre_y = padre.winfo_rooty()
    padre_ancho = padre.winfo_width()
    padre_alto = padre.winfo_height()
    
    # Calcular posición centrada respecto a la ventana padre
    x = padre_x + (padre_ancho - ancho) // 2
    y = padre_y + (padre_alto - alto) // 2
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def resource_path(relative_path):
    """Encuentra el recurso empaquetado o en el directorio de desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Carga el icono usando la ruta adaptada
icon_path = resource_path("img/apuesta_total.ico")
img_path = resource_path("img/logo_apuesta_total.png")