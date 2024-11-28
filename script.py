import sys
import os
from wia import escanear_documento
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime


def resource_path(relative_path):
    """Encuentra el recurso empaquetado o en el directorio de desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Carga el icono usando la ruta adaptada
icon_path = resource_path("img/apuesta_total.ico")
img_path = resource_path("img/logo_apuesta_total.png")

# Modificar a mas nombres
nombres_principal = ["ATERAX", "BETSHOP", "JV", "LOTTINGO", "CABALLOS", "KASNET", "NIUBIZ", "REPORTE NIUBIZ"]
nombres_especial = ["DNI FRONTAL", "DNI REVERSO", "JUGADA", "REGISTRO"]

# Variable global para la carpeta destino
carpeta_destino = ""
carpeta_actual = ""
valor_especial = "JACKPOT 1"
index = 0  # Índice para seguir la lista de nombres

def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width - ancho) // 2
    y = (screen_height - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Crear ventana principal
root = tk.Tk()
root.title(f"Escáner AT")
root.iconbitmap(icon_path)
root.resizable(False, False)
centrar_ventana(root, 400, 350)

def comparacion_carpeta_fecha():
    global carpeta_actual

    fecha_actual = datetime.now()
    fecha_actual = datetime.strftime(fecha_actual,'%d/%m/%Y %H:%M')

    dia_carpeta = carpeta_actual[-8:-6] # Extrae el dia de la carpeta
    dia_fecha = fecha_actual[0:2]

    return dia_carpeta == dia_fecha

# Función para seleccionar la carpeta destino al iniciar la app
def seleccionar_carpeta_destino(tk, actualizar_reloj):

    global carpeta_destino
    global carpeta_actual

    carpeta_destino = filedialog.askdirectory(title="Selecciona la carpeta destino")
    subcarpetas = str.split(carpeta_destino,"/")
    carpeta_actual = subcarpetas[-1]

    if not carpeta_destino:
        messagebox.showerror("Error", "Debes seleccionar una carpeta de destino.")
        root.destroy()  # Cerrar la aplicación si no se selecciona ninguna carpeta
    else:

        es_igual_fecha = comparacion_carpeta_fecha()
        carpeta_hab = "red" if es_igual_fecha else "gray"

        # Carpeta actual
        label_carpeta = tk.Label(root, text=carpeta_actual, font=("Arial", 12), fg=(carpeta_hab))  # Fuente de 10px
        label_carpeta.pack(pady=5)

        if not es_igual_fecha:
            centrar_ventana(root, 400, 380)
            label_carpeta = tk.Label(root, text="La fecha no es la misma", font=("Arial", 8, "italic"), fg=("gray"))  # Fuente de 10px
            label_carpeta.pack(pady=2)

        # Frame para organizar los botones
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=15)

        # Botones
        btn_escanear = tk.Button(frame_botones, text="Escaneo general", command=manejar_escaneo)  # Cambia la función según lo necesites
        btn_escanear.pack(side="left", padx=10)  # Botón a la izquierda

        btn_jackpot = tk.Button(frame_botones, text="Escaneo especial", command=manejar_escaneo_especial)  # Cambia la función según lo necesites
        btn_jackpot.pack(side="left", padx=10)  # Botón a la derecha

        # Iniciar actualización del reloj
        actualizar_reloj()

# Función para manejar el escaneo y saltar archivos
def manejar_escaneo():

    global index
    global carpeta_actual

    if index >= len(nombres_principal):
        messagebox.showinfo("Completado", "Todos los documentos han sido procesados.")
        index = 0
        return

    nombre_actual = nombres_principal[index]
    
    # Preguntar al usuario si desea escanear o saltar
    respuesta = messagebox.askyesno("Escaneo de Documento", f"¿Deseas escanear {nombre_actual}?\n(Sí para escanear, No para saltar)")
    
    if respuesta:
      escanear_documento(nombre_actual, carpeta_destino, carpeta_actual)
    
    # Avanzar al siguiente nombre
    index += 1
    manejar_escaneo()

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
            global centrar_ventana, icon_path

            # Crear una ventana emergente para elegir opciones
            ventana_opciones = tk.Toplevel(root)
            ventana_opciones.title("Seleccionar información")
            ventana_opciones.iconbitmap(icon_path)
            ventana_opciones.resizable(False, False)
            centrar_ventana(ventana_opciones, 300, 200)

            ventana_opciones.grab_set()

            # Mensaje de instrucciones
            tk.Label(ventana_opciones, text="Selecciona un nombre para el registro:").pack(padx=10, pady=5)

            # Crear el combobox con opciones para el nombre
            opciones_web = ["JACKPOT", "WEB RETAIL", "CUMPLEAÑERO", "BINGO"]  # Opciones para el nombre
            combobox_web = ttk.Combobox(ventana_opciones, values=opciones_web)
            combobox_web.pack(padx=10, pady=5)

            # Establecer el valor por defecto
            combobox_web.set("JACKPOT")

            # Mensaje de instrucciones para el número
            tk.Label(ventana_opciones, text="Selecciona un número para el registro:").pack(padx=10, pady=5)

            # Crear el combobox con opciones para el número
            opciones_numero = ["1", "2", "3", "4", "5"]  # Opciones para el número
            combobox_numero = ttk.Combobox(ventana_opciones, values=opciones_numero)
            combobox_numero.pack(padx=10, pady=5)

            # Establecer el valor por defecto
            combobox_numero.set("1")

            # Función para procesar la selección
            def procesar_seleccion():
                global valor_especial
                
                web = combobox_web.get()  # Obtener el valor seleccionado del combobox de nombre
                numero = combobox_numero.get()  # Obtener el valor seleccionado del combobox de número

                valor_especial = f"{web} {numero}"
                ventana_opciones.destroy()  # Cerrar la ventana de opciones

                continuar_escaneo()

            # Botón para confirmar la selección
            btn_confirmar = tk.Button(ventana_opciones, text="Confirmar", command=procesar_seleccion)
            btn_confirmar.pack(pady=10)

            ventana_opciones.mainloop()

        mostrar_opciones()

    else:
        
        continuar_escaneo()

def continuar_escaneo():
    global index, valor_especial
    nombre_actual = nombres_especial[index]

    # Preguntar al usuario si desea escanear o saltar
    respuesta = messagebox.askyesno(f"Escaneo de Documento ({valor_especial})", f"¿Deseas escanear {nombre_actual}?\n(Sí para escanear, No para saltar)")

    if respuesta:
        escanear_documento(nombre_actual, carpeta_destino, carpeta_actual, valor_especial)

    # Avanzar al siguiente nombre
    index += 1
    manejar_escaneo_especial()