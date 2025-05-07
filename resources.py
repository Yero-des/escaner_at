
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

"""
Funcion para asignar el numero mas reciente segun los archivos
ya creados en la carpeta PROMOCIONES 
ejm:
(JACKPOT 1) ...
(JACKPOT 2) ... 
se creara el archivo
(JACKPOT 3)
automaticamente
"""
def asignar_numero_mas_reciente(ruta_origen, ruta_actual, web, tipo="AUTO"):

    # Ruta completa de promociones segun carpeta actual
    nombre_carpeta_promociones = "PROMOCIONES " + ruta_actual
    ruta_base_carpeta_promociones = os.path.join(ruta_origen, nombre_carpeta_promociones)
                                
    numero = 1 # Numero por defecto
    archivos_encontrados = [] # Lista de archivos encontrados

    # Verificar si existe la ruta 
    if os.path.exists(ruta_base_carpeta_promociones):

        # Encontrar nombres de archivos que comiencen con el recurso correspondiente
        archivos_encontrados = [
            archivo for archivo in os.listdir(ruta_base_carpeta_promociones) 
            if os.path.isfile(os.path.join(ruta_base_carpeta_promociones, archivo)) and archivo.startswith(f"({web}")
        ]

        # Se verifica si se ha encontrado algun archivo 
        if len(archivos_encontrados) != 0:

            # Ordenar segun numero
            archivos_encontrados.sort(reverse=True)

            # Tomar valor y numero actual
            elemento_actual = archivos_encontrados[0]
            index_tipo = len(f"({web} ")
            numero_actual = int(elemento_actual[index_tipo])

            # print(elemento_actual)
            # print(numero_actual)

            # Sumar el valor del nueor
            numero = numero_actual + 1

    # Asignar a un numero personalizado en caso el tipo no sea AUTO
    if tipo != "AUTO":
        numero = tipo

    valor_especial = f"{web} {numero}" # Concatenacion de valores de recurso y numero
    return valor_especial

def resource_path(relative_path):
    """Encuentra el recurso empaquetado o en el directorio de desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Carga el icono usando la ruta adaptada
icon_path = resource_path("img/apuesta_total.ico")
img_path = resource_path("img/logo_apuesta_total.png")