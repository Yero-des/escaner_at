import os
import locale
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from datetime import datetime

from resources import centrar_ventana, es_carpeta_indexada

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

# Función para cambiar la carpeta destino desde el menú
def cambiar_carpeta_destino(datos_compartidos, label_carpeta, label_carpeta_aviso=None):
   
  root = datos_compartidos["root"]
  carpeta_destino = ""
  carpeta_destino_no_modificable = ""
  carpeta_actual = ""

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
    title="Cambiar la carpeta destino",
    initialdir=ruta_final  # Establecer la ruta inicial
  )

  if carpeta_destino:

    subcarpetas = str.split(carpeta_destino,"/")
    carpeta_actual = subcarpetas[-1]

    # Actualizar las etiquetas de carpeta 
    es_carpeta_correcta = es_carpeta_indexada(carpeta_actual) # Verificar si el formato de la carpeta es correcto
    carpeta_hab = "red" if es_carpeta_correcta else "gray" # Color de la etiqueta segun formato correcto o no

    if es_carpeta_correcta and label_carpeta_aviso.winfo_ismapped():

      centrar_ventana(root, 400, 400)
      label_carpeta_aviso.grid_remove()

    elif not es_carpeta_correcta and not label_carpeta_aviso.winfo_ismapped():

      centrar_ventana(root, 400, 420)
      label_carpeta_aviso.grid()

    label_carpeta.config(text=carpeta_actual, fg=(carpeta_hab))

    # Guardar las variables en el diccionario compartido
    datos_compartidos["carpeta_destino"] = carpeta_destino
    datos_compartidos["carpeta_destino_no_modificable"] = carpeta_destino_no_modificable
    datos_compartidos["carpeta_actual"] = carpeta_actual

    messagebox.showinfo("Carpeta cambiada", f"Carpeta cambiada correctamente a:\n \"{carpeta_actual}\"")

  else:
    messagebox.showerror("Error", "Debes seleccionar una carpeta de destino.")


# Función para seleccionar la carpeta destino al iniciar la app
def seleccionar_carpeta_destino(datos_compartidos):

  # Inicializar variables globales
  carpeta_destino = ""
  carpeta_destino_no_modificable = ""
  carpeta_actual = ""

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

  # Guardar las variables en el diccionario compartido
  datos_compartidos["carpeta_destino"] = carpeta_destino
  datos_compartidos["carpeta_destino_no_modificable"] = carpeta_destino_no_modificable
  datos_compartidos["carpeta_actual"] = carpeta_actual

  return not carpeta_destino
    