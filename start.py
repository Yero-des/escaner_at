import tkinter as tk
from script import *
from PIL import Image, ImageTk
from datetime import datetime

# Obtener fecha y hora actual
fecha_actual = datetime.now()
fecha_actual = datetime.strftime(fecha_actual,'%d/%m/%Y %H:%M')

# Función para actualizar la fecha y hora
def actualizar_reloj():

  fecha_actual = datetime.now()
  fecha_formateada = datetime.strftime(fecha_actual, '%d/%m/%Y %H:%M')
  label_fecha.config(text=fecha_formateada)
  root.after(1000, actualizar_reloj)  # Llama a esta función nuevamente en 1 segundo

# Seleccionar carpeta destino al inicio
root.after(100, seleccionar_carpeta_destino)  # Iniciar la selección de carpeta después de 100 ms

# Cargar imagen
imagen_original = Image.open(img_path)  # Reemplaza con la ruta de tu imagen
imagen_redimensionada = imagen_original.resize((400, 200))  # Ajustar tamaño
imagen = ImageTk.PhotoImage(imagen_redimensionada)

# Etiqueta para mostrar la imagen
label_imagen = tk.Label(root, image=imagen)
label_imagen.pack(pady=5)  # La imagen se coloca en la parte superior

# Etiqueta para mostrar la fecha encima de los botones
label_fecha = tk.Label(root, text=fecha_actual, font=("Arial", 10, "bold"))  # Fuente de 15px
label_fecha.pack(pady=5)  # La fecha se coloca encima de los botones

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

# Iniciar el bucle de la aplicación
root.mainloop()