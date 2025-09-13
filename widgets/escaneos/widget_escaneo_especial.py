import os
from wia import escanear_documento
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from resources import asignar_numero_mas_reciente, centrar_ventana_hija, icon_path

# Función para procesar la selección
def procesar_seleccion(ventana, datos_compartidos, datos_secundarios, unico=False):

  root = datos_compartidos["root"]
  carpeta_destino = datos_compartidos["carpeta_destino"]
  carpeta_actual = datos_compartidos["carpeta_actual"]
  valor_especial = datos_compartidos["valor_especial"]
  carpeta_destino_no_modificable = datos_compartidos["carpeta_destino_no_modificable"]
  nombres_especial_const = datos_compartidos["nombres_especial_const"]
  carpeta_actual = datos_compartidos["carpeta_actual"]

  combobox_web = datos_secundarios["combobox_web"].get()
  combobox_numero = datos_secundarios["combobox_numero"].get()

  nombres_especial = []

  nombre_carpeta = "PROMOCIONES" # Establece el nombre de la carpeta donde se guardaran los archivos

  # # Cambiar array de nombres segun tipo de escaneo
  if unico:
    nombres_especial.append("JUGADA")
  else:
    nombres_especial.extend(nombres_especial_const)

  for nombre in nombres_especial:
    nombre_actual = nombre

    valor_especial = asignar_numero_mas_reciente(
      ruta_origen=carpeta_destino_no_modificable,
      ruta_actual=carpeta_actual,
      web=combobox_web,
      nombre_carpeta=nombre_carpeta,
      tipo=combobox_numero
    )

    # Preguntar al usuario si desea escanear o saltar
    respuesta = messagebox.askyesnocancel(
      f"Escaneo ({valor_especial})", 
      f"¿Deseas escanear {nombre_actual}?\n(Sí para escanear, No para saltar)",
      parent=ventana
    )

    # Actualizar la carpeta destino para incluir subcarpeta PROMOCIONES
    carpeta_destino_especial = os.path.join(carpeta_destino, f"{nombre_carpeta} {carpeta_actual}")

    if respuesta:
      escanear_documento(root, nombre_actual, carpeta_destino_especial, carpeta_actual, valor_especial)
    
    if respuesta == None:
      messagebox.showinfo("Cancelado", "El proceso ha sido cancelado.", parent=ventana)
      return

  # Si ya se procesaron todos los documentos
  messagebox.showinfo("Completado", "Todos los documentos han sido procesados.", parent=ventana)

# Funcion para manejar el escaneo y saltar archivos de jackpot 
def manejar_escaneo_especial(datos_compartidos):

  root = datos_compartidos["root"]
  opciones_web = datos_compartidos["opciones_web"]

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

  frame_botones = tk.Frame(ventana_opciones)
  frame_botones.pack(pady=15)

  # Establecer datos secundarios mendiante funciones
  datos_secundarios = {
    "combobox_web": combobox_web,
    "combobox_numero": combobox_numero,
  }

  # Botón para escaneo multiple
  btn_multiple = tk.Button(frame_botones, text="Multiple", command= lambda:procesar_seleccion(ventana_opciones, datos_compartidos, datos_secundarios))
  btn_multiple.pack(side="left", pady=10, padx=10)

  # Boton para escaneo unico
  btn_unico = tk.Button(frame_botones, text="Unico", command= lambda:procesar_seleccion(ventana_opciones, datos_compartidos, datos_secundarios, True))
  btn_unico.pack(side="right", pady=10, padx=10)

  ventana_opciones.mainloop()



