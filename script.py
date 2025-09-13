import os
import locale
import re
from pathlib import Path
from PIL import Image
from wia import escanear_documento, imprimir_documento
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime
from resources import asignar_numero_mas_reciente, centrar_ventana, centrar_ventana_hija, icon_path

# Función para actualizar el directorio de la carpeta segun el escaneo sea especial o no
def actualizar_carpeta_destino(es_metodo_especial):
    global carpeta_destino, carpeta_actual

    carpeta_especial = "PROMOCIONES " + carpeta_actual
    carpeta_especial_path = os.path.join(carpeta_destino, carpeta_especial)

    # Corroborar si la carpeta ha sido modificada
    es_carpeta_modificada = carpeta_destino.endswith(carpeta_especial)

    # print(es_carpeta_modificada, es_metodo_especial)

    if es_carpeta_modificada and es_metodo_especial:
        pass  # No hacemos nada, ya es especial
    elif es_carpeta_modificada and not es_metodo_especial:
        # Quitar la última carpeta y dejar la ruta original
        carpeta_destino = os.path.dirname(carpeta_destino)
    elif not es_carpeta_modificada and es_metodo_especial:
        # Cambiar a ruta especial
        carpeta_destino = carpeta_especial_path

    # print(f"Carpeta Destino: {carpeta_destino}")

# Funcion para manejar el escaneo y saltar archivos de jackpot 
def manejar_escaneo_especial():
    global index, carpeta_actual, valor_especial

    # Si ya se procesaron todos los documentos
    if index >= len(nombres_especial):
        messagebox.showinfo("Completado", "Todos los documentos han sido procesados.")
        index = 0
        return

    # Solo en la primera ejecución, pedir nombre y número
    if index == 0:

        # Crear ventana para opciones seleccionables
        def mostrar_opciones():
            global centrar_ventana, icon_path, opciones_web

            # Crear una ventana emergente para elegir opciones
            ventana_opciones = tk.Toplevel(root)
            centrar_ventana_hija(ventana_opciones, 300, 200, root)

            ventana_opciones.title("Seleccionar información")
            ventana_opciones.iconbitmap(icon_path)
            ventana_opciones.resizable(False, False)
            ventana_opciones.focus_force()

            ventana_opciones.grab_set()

            # Mensaje de instrucciones
            tk.Label(ventana_opciones, text="Selecciona un nombre para el registro:").pack(padx=10, pady=5)

            # Crear el combobox con opciones para el nombre
            combobox_web = ttk.Combobox(ventana_opciones, values=opciones_web)
            combobox_web.pack(padx=10, pady=5)

            # Establecer el valor por defecto
            combobox_web.set("JACKPOT")

            # Mensaje de instrucciones para el número
            tk.Label(ventana_opciones, text="Selecciona un número para el registro:").pack(padx=10, pady=5)

            # Crear el combobox con opciones para el número
            opciones_numero = ["AUTO", "1", "2", "3", "4", "5"]  # Opciones para el número
            combobox_numero = ttk.Combobox(ventana_opciones, values=opciones_numero)
            combobox_numero.pack(padx=10, pady=5)

            # Establecer el valor por defecto
            combobox_numero.set("AUTO")

            # Función para procesar la selección
            def procesar_seleccion(unico=False):
                global valor_especial, carpeta_destino_no_modificable, carpeta_actual, nombres_especial

                # Cambiar array de nombres segun tipo de escaneo
                if unico:
                    nombres_especial = ["JUGADA"]
                else:
                    nombres_especial = nombres_especial_const

                valor_especial = asignar_numero_mas_reciente(
                    ruta_origen=carpeta_destino_no_modificable,
                    ruta_actual=carpeta_actual,
                    web=combobox_web.get(),
                    tipo=combobox_numero.get()
                )

                ventana_opciones.destroy()  # Cerrar la ventana de opciones

                continuar_escaneo()

            frame_botones = tk.Frame(ventana_opciones)
            frame_botones.pack(pady=15)

            # Botón para escaneo multiple
            btn_multiple = tk.Button(frame_botones, text="Multiple", command= lambda:procesar_seleccion())
            btn_multiple.pack(side="left", pady=10, padx=10)

            # Boton para escaneo unico
            btn_unico = tk.Button(frame_botones, text="Unico", command= lambda:procesar_seleccion(True))
            btn_unico.pack(side="right", pady=10, padx=10)

            ventana_opciones.mainloop()

        mostrar_opciones()

    else:
        
        continuar_escaneo()

def continuar_escaneo():
    global index, valor_especial, carpeta_destino, primera_promo
    nombre_actual = nombres_especial[index]

    # Preguntar al usuario si desea escanear o saltar
    respuesta = messagebox.askyesnocancel(f"Escaneo ({valor_especial})", f"¿Deseas escanear {nombre_actual}?\n(Sí para escanear, No para saltar)")

    actualizar_carpeta_destino(True)

    if respuesta:
        escanear_documento(root, nombre_actual, carpeta_destino, carpeta_actual, valor_especial)
    
    if respuesta == None:
        messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.")
        index = 0
        return

    # Avanzar al siguiente nombre
    index += 1
    manejar_escaneo_especial()
