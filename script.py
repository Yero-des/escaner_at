import os
import locale
from pathlib import Path
from wia import escanear_documento
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime
from resources import centrar_ventana, centrar_ventana_hija, icon_path

# Modificar a mas nombres
nombres_principal = ["KASNET", "NIUBIZ", "REPORTE NIUBIZ", "CABALLOS", "LOTTINGO", "BETSHOP", "JV", "VALE DE DESCUENTO"]
opciones_web = ["JACKPOT", "VALE DE REGISTRO", "LUNES REGALON", "VIERNES DONATELO", "LOTTINGO", "WEB RETAIL", "CUMPLEAÑERO", "VLT"] 
nombres_especial = ["DNI FRONTAL", "DNI REVERSO", "JUGADA", "COMPROBANTE"]

# Variable global para la carpeta destino
carpeta_destino = ""
carpeta_destino_no_modificable = ""
carpeta_actual = ""
valor_especial = "JACKPOT 1"
index = 0  # Índice para seguir la lista de nombres

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

def verificar_o_crear_ruta(ruta_base, carpeta1, carpeta2, carpeta3):
    ruta_carpeta1 = os.path.join(ruta_base, carpeta1)
    ruta_carpeta2 = os.path.join(ruta_carpeta1, carpeta2)
    ruta_carpeta3 = os.path.join(ruta_carpeta2, carpeta3)
    
    # Verifica y crea la primera carpeta si no existe
    if not os.path.exists(ruta_carpeta1):
        os.makedirs(ruta_carpeta1)
    
    # Verifica y crea la segunda carpeta si no existe
    if not os.path.exists(ruta_carpeta2):
        os.makedirs(ruta_carpeta2)

    # Verifica y crea la tercera carpeta si no existe
    if not os.path.exists(ruta_carpeta3):
        os.makedirs(ruta_carpeta3)
    
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
        btn_jackpot.pack(side="left", padx=10)  # Botón al medio

        btn_carpeta = tk.Button(frame_botones, text="Carpeta", command=ver_carpeta) # Ver carpeta actual en explorador
        btn_carpeta.pack(side="right", padx=10) # Boton a la derecha

        # Iniciar actualización del reloj
        actualizar_reloj()

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

    global index
    global carpeta_actual

    if index >= len(nombres_principal):
        messagebox.showinfo("Completado", "Todos los documentos han sido procesados.")
        index = 0
        return
    
    actualizar_carpeta_destino(False)

    nombre_actual = nombres_principal[index]
    
    # Preguntar al usuario si desea escanear o saltar
    respuesta = messagebox.askyesnocancel("Escaneo de Documento", f"¿Deseas escanear {nombre_actual}?\n(Sí para escanear, No para saltar)")

    if respuesta:
      escanear_documento(root, nombre_actual, carpeta_destino, carpeta_actual)
    
    if respuesta == None:
        messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.")
        index = 0
        return
    
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
            global centrar_ventana, icon_path, opciones_web

            # Crear una ventana emergente para elegir opciones
            ventana_opciones = tk.Toplevel(root)
            ventana_opciones.title("Seleccionar información")
            ventana_opciones.iconbitmap(icon_path)
            ventana_opciones.resizable(False, False)
            ventana_opciones.focus_force()
            centrar_ventana_hija(ventana_opciones, 300, 200, root)

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
            def procesar_seleccion():
                global valor_especial, carpeta_destino_no_modificable, carpeta_actual

                # Path completo de promociones segun carpeta actual
                carpeta_especial = "PROMOCIONES " + carpeta_actual
                carpeta_especial_path = os.path.join(carpeta_destino_no_modificable, carpeta_especial)

                numero = 1 # Valor seleccionado por defecto para numero de escaneo
                web = combobox_web.get()  # Obtener el valor seleccionado del combobox de nombre
                archivos_encontrados = []

                # Asignar el numero mas reciente
                if os.path.exists(carpeta_especial_path):

                    archivos_encontrados = [
                        archivo for archivo in os.listdir(carpeta_especial_path) 
                        if os.path.isfile(os.path.join(carpeta_especial_path, archivo)) and archivo.startswith(f"({web}")
                    ]

                    if len(archivos_encontrados) != 0:

                        # Ordenar segun numero
                        archivos_encontrados.sort(reverse=True)

                        # Tomar valor y numero actual
                        elemento_actual = archivos_encontrados[0]
                        index_tipo = len(f"({web} ")
                        numero_actual = int(elemento_actual[index_tipo])

                        print(elemento_actual)
                        print(numero_actual)

                        numero = numero_actual + 1

                print("Archivos encontrados:", archivos_encontrados)

                if combobox_numero.get() != "AUTO":
                    numero = combobox_numero.get()

                valor_especial = f"{web} {numero}"
                ventana_opciones.destroy()  # Cerrar la ventana de opciones

                continuar_escaneo()

            # Botón para confirmar la selección
            btn_confirmar = tk.Button(ventana_opciones, text="Confirmar", command= lambda:procesar_seleccion())
            btn_confirmar.pack(pady=10)

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