import os
from wia import escanear_documento
import tkinter as tk
from resources import asignar_numero_mas_reciente, centrar_ventana_hija, icon_path

# Funcion para realizar un escaneo simple
def manejar_escaneo_simple(datos_compartidos):

  root = datos_compartidos["root"]
  carpeta_destino_no_modificable = datos_compartidos["carpeta_destino_no_modificable"]
  carpeta_actual = datos_compartidos["carpeta_actual"]
  carpeta_destino = datos_compartidos["carpeta_destino"]
  nombre_carpeta = "ARCHIVOS" # Establece el nombre de la carpeta donde se guardaran los archivos

  # Crear una ventana emergente para elegir opciones
  ventana_opciones = tk.Toplevel(root)
  centrar_ventana_hija(ventana_opciones, 300, 100, root) # LLamar funcion justo despues de crear la ventana

  ventana_opciones.title("Datos de escaneo")
  ventana_opciones.iconbitmap(icon_path)
  ventana_opciones.resizable(False, False)
  ventana_opciones.focus_force()
  ventana_opciones.grab_set()

  # Actualizar carpeta destino unicamente en funcion
  carpeta_destino_simple = os.path.join(carpeta_destino, f"{nombre_carpeta} {carpeta_actual}")

  # Mensaje de instrucciones
  nombre_archivo_entry = tk.Entry(ventana_opciones)
  nombre_archivo_entry.pack(padx=10, pady=15)
  
  def procesar_escaneo_simple(event=None):

    nombre_archivo = nombre_archivo_entry.get().upper() # Convertir a mayusculas

    # Asignar numero mas reciente en caso sea auto
    valor_especial = asignar_numero_mas_reciente(
      ruta_origen=carpeta_destino_no_modificable,
      ruta_actual=carpeta_actual,
      web="ARCHIVO",
      nombre_carpeta=nombre_carpeta,
    )   

    escanear_documento(root, nombre_archivo, carpeta_destino_simple, carpeta_actual, valor_especial)
    ventana_opciones.destroy()

  # Al presionar Enter en el Entry, se llama a procesar_escaneo_simple
  nombre_archivo_entry.bind("<Return>", procesar_escaneo_simple)

  tk.Button(ventana_opciones, text="Escanear", command=procesar_escaneo_simple).pack(padx=10, pady=5)

  ventana_opciones.mainloop()