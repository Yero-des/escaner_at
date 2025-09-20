from tkinter import messagebox
from sql.db import datos_por_tipo
from wia import escanear_documento

# Función que maneja el escaneo general
def manejar_escaneo_general(datos_compartidos):

  root = datos_compartidos["root"]
  carpeta_actual = datos_compartidos["carpeta_actual"]
  carpeta_destino = datos_compartidos["carpeta_destino"]

  # Filtra y ordena por tipo "principal" en db
  nombres_principal = datos_por_tipo("principal")

  for nombre in nombres_principal:
    nombre_actual = nombre
    
    # Preguntar al usuario si desea escanear o saltar
    respuesta = messagebox.askyesnocancel("Escaneo de Documento", f"¿Deseas escanear {nombre_actual}?\n(Sí para escanear, No para saltar)")

    if respuesta:
      escanear_documento(root, nombre_actual, carpeta_destino, carpeta_actual)
    
    if respuesta == None:
      messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.")
      return
      
  messagebox.showinfo("Completado", "Todos los documentos han sido procesados")
    