import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from resources import *
from widgets.opciones_widget import *

# Modificar a mas nombres
nombres_principal = ["KASNET", "NIUBIZ", "REPORTE NIUBIZ", "CABALLOS", "LOTTINGO", "KURAX", "GOLDEN", "BETSHOP", "VALE DE DESCUENTO"]
opciones_web = ["JACKPOT", "VALE DE REGISTRO", "LUNES REGALON", "VIERNES DONATELO", "LOTTINGO", "WEB RETAIL", "CUMPLEAÑERO", "VLT"]
nombres_especial = ["DNI FRONTAL", "DNI REVERSO", "JUGADA", "COMPROBANTE"]
nombres_especial_const = nombres_especial.copy()

# Variable global para la carpeta destino
carpeta_destino = ""
carpeta_destino_no_modificable = ""
carpeta_actual = ""
valor_especial = "JACKPOT 1"
index = 0  # Índice para seguir la lista de nombres

# Crear ventana principal
root = tk.Tk()
centrar_ventana(root, 400, 400) # Centramos la ventana principal justo despues de crearla
root.title(f"Escáner AT")
root.iconbitmap(icon_path)
root.resizable(False, False)

# Crea un menú principal
menu_bar = tk.Menu(root)

# Crear un submenú "Opciones principales"
menu_opciones = tk.Menu(menu_bar, tearoff=0) 

# Establecer un diccionario con los datos que seran compartidos entre funciones
datos_compartidos = {
  "root": root,
  "icon_path": icon_path,
}  

menu_opciones.add_command(
  label="Opciones principales",
  command=lambda: configurar_opciones_principales(datos_compartidos)
)
menu_opciones.add_command(
  label="Opciones especiales", 
  command= lambda: configurar_opciones_especiales(datos_compartidos)
)
menu_opciones.add_command(
  label="Promociones",
  command=lambda: configurar_promociones(datos_compartidos)
)

# Agregar el submenú al menú principal
menu_bar.add_cascade(label="Configuración", menu=menu_opciones)

# Asociar el menú a la ventana
root.config(menu=menu_bar)

# # Obtener fecha y hora actual y formatearla
fecha_actual = datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M')

# Cargar imagen
imagen_original = Image.open(img_path)  # Reemplaza con la ruta de tu imagen
imagen_redimensionada = imagen_original.resize((400, 200))  # Ajustar tamaño
imagen = ImageTk.PhotoImage(imagen_redimensionada)

"""
DISEÑO DE LA VENTANA PRINCIPAL
"""
# Crear frame superior sin bordes
frame_superior = tk.Frame(root, borderwidth=0, highlightthickness=0)
frame_superior.pack(side="top", fill="x")

""""
Frame superior contiene:
- Imagen
- Fecha y hora actual
"""
# Etiqueta para mostrar la imagen
label_imagen = tk.Label(frame_superior, image=imagen, borderwidth=0, highlightthickness=0)
label_imagen.pack(fill="x")

# # Etiqueta para mostrar la fecha encima de los botones
label_fecha = tk.Label(frame_superior, text=fecha_actual, font=("Arial", 10, "bold"))  # Fuente de 15px
label_fecha.pack(fill="x")  # La fecha se coloca encima de los botones

# # Seleccionar carpeta destino al inicio
# # root.after(100, seleccionar_carpeta_destino(tk, actualizar_reloj(root, label_fecha)))  # Iniciar la selección de carpeta después de 100 ms

# # Verificar si el formato de la carpeta es correcto
# es_carpeta_correcta = es_carpeta_indexada(carpeta_actual)

# carpeta_hab = "red" if es_carpeta_correcta else "gray"

# # Carpeta actual
# label_carpeta = tk.Label(root, text=carpeta_actual, font=("Arial", 12), fg=(carpeta_hab))  # Fuente de 10px
# label_carpeta.pack(pady=5)

# if not es_carpeta_correcta:
#     centrar_ventana(root, 400, 420)
#     label_carpeta = tk.Label(root, text="La fecha o formato es incorrecto", font=("Arial", 8, "italic"), fg=("gray"))  # Fuente de 10px
#     label_carpeta.pack(pady=2)

# # Frame general para organizar botones
# frame_botones = tk.Frame(root)
# frame_botones.pack(pady=15)

# # Subframe superior - 3 botones centrados
# frame_superior = tk.Frame(frame_botones)
# frame_superior.pack()

# btn_escanear = tk.Button(frame_superior, text="Escaneo general", command=manejar_escaneo)
# btn_escanear.pack(side="left", padx=10)

# btn_jackpot = tk.Button(frame_superior, text="Escaneo especial", command=manejar_escaneo_especial)
# btn_jackpot.pack(side="left", padx=10)

# btn_carpeta = tk.Button(frame_superior, text="Carpeta", command=ver_carpeta)
# btn_carpeta.pack(side="left", padx=10)

# # Subframe inferior - 2 botones centrados
# frame_inferior = tk.Frame(frame_botones)
# frame_inferior.pack(pady=10)

# btn_simple = tk.Button(frame_inferior, text="Escaneo simple", command=manejar_escaneo_simple)
# btn_simple.pack(side="left", padx=15)

# btn_imprimir = tk.Button(frame_inferior, text="Imprimir pizarras", command=imprimir_pizarras)
# btn_imprimir.pack(side="left", padx=15)

# Iniciar actualización del reloj
actualizar_reloj(root, label=label_fecha)

# Iniciar el bucle de la aplicación
root.mainloop()
