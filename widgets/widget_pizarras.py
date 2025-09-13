import os
import re
from wia import imprimir_documento
from tkinter import messagebox

# Función para imprimir todas las pizarras en la carpeta pizarras
def imprimir_pizarras(datos_compartidos):

  carpeta_actual = datos_compartidos["carpeta_actual"]
  carpeta_destino_no_modificable = datos_compartidos["carpeta_destino_no_modificable"]


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