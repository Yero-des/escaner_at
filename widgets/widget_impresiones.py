import os
import re
import winsound
from wia import imprimir_documento
from tkinter import messagebox
from resources import formatos_paths
from wia import escanear_documento
from .widget_opciones import ver_carpeta

# Función para imprimir todas las pizarras en la carpeta pizarras
def imprimir_pizarras(datos_compartidos):
  
  carpeta_actual = datos_compartidos["carpeta_actual"]
  carpeta_destino_no_modificable = datos_compartidos["carpeta_destino_no_modificable"]

  carpeta_pizarras = f"PIZARRAS {carpeta_actual[-10:]}"
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
    
  # 🔽 Ordenar por fecha (más reciente primero)
  ruta_archivos.sort(
      key=lambda ruta: os.path.getmtime(ruta),
  )

  for ruta_archivo in ruta_archivos:

    # Tomamos la ruta completa de la imagen
    ruta_archivo_actual = ruta_archivo
    nombre_archivo_actual = re.split(r"[\\/]", ruta_archivo_actual)[-1] # Tomanos el ultimo elemento de la ruta

    respuesta = messagebox.askyesnocancel(
      "Imprimir Pizarras",
      f"¿Deseas imprimir {nombre_archivo_actual}?\n(Sí para escanear, No para saltar)"
    )

    if respuesta is None:
      messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.")
      return

    if respuesta:
      imprimir_documento(ruta_archivo_actual)

  # messagebox.showinfo("Completado", "Todos los documentos han sido procesados.")
  
# Función para imprimir todos los formatos de NIUBIZ y DESCUENTO
def administrar_formatos(datos_compartidos):
  
  root = datos_compartidos["root"]
  carpeta_actual = datos_compartidos["carpeta_actual"]
  carpeta_destino = datos_compartidos["carpeta_destino"]
  
  # Impresión de formatos (niubiz, vale de descuento)
  for formato in formatos_paths:
    # Tomamos el nombre actual
    nombre_archivo_actual = re.split(r"[\\/]", formato)[-1] # Tomanos el ultimo elemento de la ruta
    nombre_archivo_actual = nombre_archivo_actual.split('_')[1]

    respuesta = messagebox.askyesnocancel(
      "Administrar Formatos",
      f"¿Deseas imprimir {nombre_archivo_actual}?\n(Sí para escanear, No para saltar)"
    )

    if respuesta is None:
      messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.")
      return

    if respuesta:
      imprimir_documento(formato)
      
  # Escaneo de formatos (vale de descuento)
  nombres_formatos = ['VALE DE DESCUENTO']

  for nombre in nombres_formatos:
    
    nombre_actual = nombre
    
    # Preguntar al usuario si desea escanear o saltar
    respuesta = messagebox.askyesnocancel("Administrar Formatos", f"¿Deseas escanear {nombre_actual.lower()}?\n(Sí para escanear, No para saltar)")

    if respuesta:
      escanear_documento(root, nombre_actual, carpeta_destino, carpeta_actual)
    
    if respuesta == None:
      messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.")
      return

  winsound.MessageBeep()
  respuesta = messagebox.askyesno("Completado", "Todos los documentos han sido procesados, desea ver los reportes actualizados?")
  if respuesta:
    ver_carpeta(datos_compartidos)
    
  # messagebox.showinfo("Completado", "Todos los documentos han sido procesados.")