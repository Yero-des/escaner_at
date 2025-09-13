import os
import locale
from pathlib import Path
from tkinter import filedialog, messagebox
from datetime import datetime

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
    