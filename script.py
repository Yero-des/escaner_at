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
from resources import asignar_numero_mas_reciente, centrar_ventana, centrar_ventana_hija, es_carpeta_indexada, icon_path
from start import *

# Función para verificar y crear la estructura de carpetas
def verificar_o_crear_ruta(ruta_base, carpeta1, carpeta2, carpeta3):

    ruta_carpeta1 = os.path.join(ruta_base, carpeta1)
    ruta_carpeta2 = os.path.join(ruta_carpeta1, carpeta2)
    ruta_carpeta3 = os.path.join(ruta_carpeta2, carpeta3)
    ruta_carpeta_pizarras = os.path.join(ruta_carpeta3, f'PIZARRAS {carpeta3}')

    # Verifica y crea la primera carpeta si no existe
    if not os.path.exists(ruta_carpeta1):
        os.makedirs(ruta_carpeta1)
    
    # Verifica y crea la segunda carpeta si no existe
    if not os.path.exists(ruta_carpeta2):
        os.makedirs(ruta_carpeta2)

    # Verifica y crea la tercera carpeta si no existe
    if not os.path.exists(ruta_carpeta3):
        os.makedirs(ruta_carpeta3)

    # Verifica y crea la carpeta de pizarras si no existe
    if not os.path.exists(ruta_carpeta_pizarras):
        os.makedirs(ruta_carpeta_pizarras)
    
    # Asigna la ruta final a una variable
    ruta_final = ruta_carpeta3
    return ruta_final

# Función para seleccionar la carpeta destino al iniciar la app
def seleccionar_carpeta_destino(tk, actualizar_reloj):

    global carpeta_destino, carpeta_destino_no_modificable, carpeta_actual

    # Fecha actual
    fecha_actual = datetime.now()
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # Configurar el idioma a español

    # Extraer datos en variables diferentes
    anio = str(fecha_actual.year) # Año actual
    nombre_mes = fecha_actual.strftime("%B").upper()  # Nombre del mes en mayúsculas
    fecha_formateada = fecha_actual.strftime("%d.%m.%y")  # Formato dd.mm.yy

    # Obtener la ruta de "Documentos" de forma independiente al usuario
    ruta_raiz = Path.home() / "Documents"

    ruta_final = verificar_o_crear_ruta(
        ruta_raiz, 
        carpeta1=anio, 
        carpeta2=nombre_mes, 
        carpeta3=fecha_formateada
    )

    carpeta_destino = carpeta_destino_no_modificable = filedialog.askdirectory(
        title="Selecciona la carpeta destino",
        initialdir=ruta_final  # Establecer la ruta inicial
    )

    subcarpetas = str.split(carpeta_destino,"/")
    carpeta_actual = subcarpetas[-1]

    if not carpeta_destino:
        messagebox.showerror("Error", "Debes seleccionar una carpeta de destino.")
        root.destroy()  # Cerrar la aplicación si no se selecciona ninguna carpeta
        return
    
# Función para imprimir todas las pizarras en la carpeta pizarras
def imprimir_pizarras():
    global  carpeta_destino_no_modificable, carpeta_actual

    carpeta_pizarras = f"PIZARRAS {carpeta_actual[-8:]}"
    carpeta_principal = os.path.dirname(carpeta_destino_no_modificable)
    ruta_carpeta_pizarras = os.path.join(carpeta_principal, carpeta_pizarras)

    # Validar si se encontró
    if not os.path.exists(ruta_carpeta_pizarras):
        messagebox.showinfo("Error", "No se encontró la carpeta 'PIZARRAS'")
        return

    # Buscar imágenes en la carpeta
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    ruta_archivos = [
        os.path.join(ruta_carpeta_pizarras, archivo)
        for archivo in os.listdir(ruta_carpeta_pizarras)
        if archivo.lower().endswith(extensiones_validas)
    ]

    if not ruta_archivos:
        messagebox.showinfo("Sin Archivos", f'No se encontraron imágenes en la carpeta: "{ruta_carpeta_pizarras}"')
        return

    for ruta_archivo in ruta_archivos:

        # Tomamos la ruta completa de la imagen
        ruta_archivo_actual = ruta_archivo
        nombre_archivo_actual = re.split(r"[\\/]", ruta_archivo_actual)[-1] # Tomanos el ultimo elemento de la ruta

        respuesta = messagebox.askyesnocancel(
            "Imprimir Documento",
            f"¿Deseas imprimir {nombre_archivo_actual}?\n(Sí para escanear, No para saltar)"
        )

        if respuesta is None:
            messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.")
            return

        if respuesta:
            imprimir_documento(ruta_archivo_actual)

    # messagebox.showinfo("Completado", "Todos los documentos han sido procesados.")

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

# Función para abrir la carpeta actual en el explorador de archivos
def ver_carpeta():

    global carpeta_destino

    actualizar_carpeta_destino(False)

    os.startfile(carpeta_destino)
    return

# Función para manejar el escaneo y saltar archivos
def manejar_escaneo():
    global carpeta_actual

    actualizar_carpeta_destino(False)

    for nombre in nombres_principal:
        nombre_actual = nombre
        
        # Preguntar al usuario si desea escanear o saltar
        respuesta = messagebox.askyesnocancel("Escaneo de Documento", f"¿Deseas escanear {nombre_actual}?\n(Sí para escanear, No para saltar)")

        if respuesta:
            escanear_documento(root, nombre_actual, carpeta_destino, carpeta_actual)
        
        if respuesta == None:
            messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.")
            index = 0
            return
        
    messagebox.showinfo("Completado", "Todos los documentos han sido procesados")
    
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

# Funcion para realizar un escaneo simple
def manejar_escaneo_simple():
    # Crear una ventana emergente para elegir opciones
    ventana_opciones = tk.Toplevel(root)
    centrar_ventana_hija(ventana_opciones, 300, 100, root) # LLamar funcion justo despues de crear la ventana

    ventana_opciones.title("Datos de escaneo")
    ventana_opciones.iconbitmap(icon_path)
    ventana_opciones.resizable(False, False)
    ventana_opciones.focus_force()
    actualizar_carpeta_destino(True)

    ventana_opciones.grab_set()

    # Mensaje de instrucciones
    nombre_archivo_entry = tk.Entry(ventana_opciones)
    nombre_archivo_entry.pack(padx=10, pady=15)
    
    def procesar_escaneo_simple(event=None):

        nombre_archivo = nombre_archivo_entry.get().upper()
        # print(nombre_archivo)

        valor_especial = asignar_numero_mas_reciente(
            ruta_origen=carpeta_destino_no_modificable,
            ruta_actual=carpeta_actual,
            web="ARCHIVO"
        )   

        escanear_documento(root, nombre_archivo, carpeta_destino, carpeta_actual, valor_especial)
        ventana_opciones.destroy()

    # Al presionar Enter en el Entry, se llama a procesar_escaneo_simple
    nombre_archivo_entry.bind("<Return>", procesar_escaneo_simple)

    tk.Button(ventana_opciones, text="Escanear", command=procesar_escaneo_simple).pack(padx=10, pady=5)

    ventana_opciones.mainloop()