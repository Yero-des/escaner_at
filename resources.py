import sys
import os
import re
import tkinter as tk
from datetime import datetime

def resource_path(relative_path):
    """Encuentra el recurso empaquetado o en el directorio de desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

"""
Funcion para actualizar el reloj cada segundo
retorna la fecha y hora actual en formato 'dd/mm/yyyy hh:mm'
ejm: 24/07/2024 14:30
"""
def actualizar_reloj(root, label):
    try:
        fecha_actual = datetime.now()
        fecha_formateada = datetime.strftime(fecha_actual, '%d/%m/%Y %H:%M')
        label.config(text=fecha_formateada)
        root.after(1000, lambda: actualizar_reloj(root, label))
    except tk.TclError:
        # Aquí llegas cuando root o label ya fueron destruidos
        return

def centrar_ventana(ventana, ancho, alto):

    ventana.withdraw()  # Ocultar mientras se configura

    # Obtener medidas de pantalla
    screen_width = ventana.winfo_screenwidth()

    # Calcular posición centrada
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    ventana.deiconify() # Mostrar la ventana después de configurar

def centrar_ventana_hija(ventana, ancho, alto, padre):

    ventana.withdraw()  # Ocultar mientras se configura

    # Obtener la posición de la ventana padre
    padre_x = padre.winfo_rootx()
    padre_y = padre.winfo_rooty()
    padre_ancho = padre.winfo_width()
    padre_alto = padre.winfo_height()
    
    # Calcular posición centrada respecto a la ventana padre
    x = padre_x + (padre_ancho - ancho) // 2
    y = padre_y + (padre_alto - alto) // 2
    
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    ventana.deiconify() # Mostrar la ventana después de configurar

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
def asignar_numero_mas_reciente(ruta_origen, ruta_actual, web, nombre_carpeta, tipo="AUTO"):

    # Ruta completa de promociones segun carpeta actual
    ruta_base_carpeta_promociones = os.path.join(ruta_origen, f'{nombre_carpeta} {ruta_actual}')
                                
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

"""
Función para verificar si es una carpeta indexada y con la fecha actual
retorna True si el nombre de la carpeta coincide con el dia actual y el formato
y False en caso el nombre de la carpeta no coincida
ejm:
T1 - YEROMI ZAVALA 24.07.25 (True) (Dia actual 24.07.25)
T1 - YEROMI ZAVALA 20.06.25 (False)
24.07.24 (False)
"""
def es_carpeta_indexada(carpeta_actual):
    fecha_actual = datetime.strftime(datetime.now(),'%d.%m.%y')

    formato_carpeta = fr"^T[123]\s-\s[A-Z]+\s[A-Z]+\s{re.escape(fecha_actual)}$"
    es_formato_correcto = re.match(formato_carpeta, carpeta_actual)

    # print(f'Verificando carpeta: {carpeta_actual}')
    # print(bool(es_formato_correcto))

    return bool(es_formato_correcto)

# Carga el icono usando la ruta adaptada
icon_path = resource_path("img/apuesta_total.ico")
img_path = resource_path("img/logo_apuesta_total.png")