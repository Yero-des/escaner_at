import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from resources import *
from widgets.escaneos.widget_escaneo_especial import manejar_escaneo_especial
from widgets.widget_opciones import *
from widgets.widget_inicio import cambiar_carpeta_destino, seleccionar_carpeta_destino
from widgets.escaneos.widget_escaneo_general import manejar_escaneo_general
from widgets.escaneos.widget_escaneo_simple import manejar_escaneo_simple
from widgets.widget_pizarras import imprimir_pizarras

"""
DISEÑO INICIAL DE LA VENTANA PRINCIPAL
"""
VERSION = "1.2.1"

root = tk.Tk()
centrar_ventana(root, 400, 400) # Centramos la ventana principal justo despues de crearla
root.title(f"Escáner AT (v{VERSION})")
root.iconbitmap(icon_path)
root.resizable(False, False)

"""
INICIALIZACION DE VARIABLES GLOBALES
"""
# Establecer un diccionario con los datos que seran compartidos entre funciones
nombres_especial = ["DNI FRONTAL", "DNI REVERSO", "JUGADA", "COMPROBANTE"]
datos_compartidos = {
  #
  "nombres_principal": ["KASNET", "NIUBIZ", "REPORTE NIUBIZ", "CABALLOS", "LOTTINGO", "KURAX", "GOLDEN", "BETSHOP", "VALE DE DESCUENTO"],
  "opciones_web": ["JACKPOT", "VALE DE REGISTRO", "LUNES REGALON", "VIERNES DONATELO", "LOTTINGO", "WEB RETAIL", "CUMPLEAÑERO", "VLT"],
  "nombres_especial": nombres_especial,
  "nombres_especial_const": nombres_especial.copy(),
  # Variables globales simple
  "root": root,
  "icon_path": icon_path,
  "carpeta_destino": "",
  "carpeta_destino_no_modificable": "",
  "carpeta_actual": "",
  "valor_especial": "JACKPOT 1",
}  

# Cargar imagen
imagen_original = Image.open(img_path)  # Reemplaza con la ruta de tu imagen
imagen_redimensionada = imagen_original.resize((400, 200))  # Ajustar tamaño
imagen = ImageTk.PhotoImage(imagen_redimensionada)

"""
DISEÑO DEL MENU DE VENTANA PRINCIPAL
"""
menu_bar = tk.Menu(root) # Crea un menú principal

""""
Menu principal contiene:
- Opciones principales
  * Opciones principales
  * Opciones especiales
  * Promociones
"""
# Crear menú principal
menu_bar = tk.Menu(root)

# ====== Menú "Configuración" con submenú ======
menu_opciones = tk.Menu(menu_bar, tearoff=0)
menu_opciones.add_command(
  label="Opciones principales",
  command=lambda: configurar_opciones_principales(datos_compartidos)
)
menu_opciones.add_command(
  label="Opciones especiales", 
  command=lambda: configurar_opciones_especiales(datos_compartidos)
)
menu_opciones.add_command(
  label="Promociones",
  command=lambda: configurar_promociones(datos_compartidos)
)
menu_bar.add_cascade(label="Configuración", menu=menu_opciones) # Agregar submenú al menu "Configuración"

""""
Menu carpetas contiene:
- Carpetas
  * Ver carpeta
  * Cambiar carpeta destino
"""
# ====== Menú "Carpetas" con  submenú ======
menu_carpetas = tk.Menu(menu_bar, tearoff=0)
menu_carpetas.add_command(
  label="Ver carpeta",
  command=lambda: ver_carpeta(datos_compartidos)
)
menu_carpetas.add_command(
  label="Cambiar carpeta destino", 
  command=lambda: cambiar_carpeta_destino(
    datos_compartidos, 
    label_carpeta, 
    label_carpeta_aviso
  )
) 
menu_bar.add_cascade(label="Carpetas", menu=menu_carpetas) # Agregar submenú al menu "Carpetas"
root.config(menu=menu_bar) # Asociar menú completo a la ventana principal

"""
DISEÑO DE LA VENTANA PRINCIPAL
"""
# Crear frame contenedor sin bordes
frame_contenedor = tk.Frame(root)
frame_contenedor.pack(side="top", fill="x")

""""
Frame contenedor contiene:
- Imagen
- Fecha y hora actual
- Carpeta actual
  * Aviso de formato incorrecto (si aplica)
"""
# Etiqueta imagen "Apuesta total"
label_imagen = tk.Label(frame_contenedor, image=imagen, borderwidth=0, highlightthickness=0)
label_imagen.grid(row=0, column=0) 

# ====== Tomar datos de pantalla emergente para seleccionar carpeta ======
if seleccionar_carpeta_destino(datos_compartidos):  
  messagebox.showerror("Error", "Debes seleccionar una carpeta de destino.")
  root.destroy()
  exit()  # Salir del programa si no se selecciona ninguna carpeta

es_carpeta_correcta = es_carpeta_indexada(datos_compartidos["carpeta_actual"]) # Verificar si el formato de la carpeta es correcto
carpeta_hab = "red" if es_carpeta_correcta else "gray" # Color de la etiqueta segun formato correcto o no

# ====== Resto de etiquetas ======

# Etiqueta de fecha y hora actual
label_fecha = tk.Label(frame_contenedor, 
  text=datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M'), # Extraer fecha y hora actual
  font=("Arial", 10, "bold") # Fuente de 10px
)
label_fecha.grid(row=1, column=0, pady=5, padx=5)

# Etiqueta de carpeta actual
label_carpeta = tk.Label(frame_contenedor, text=datos_compartidos["carpeta_actual"], font=("Arial", 12), fg=(carpeta_hab))  # Fuente de 10px
label_carpeta.grid(row=2, column=0, pady=5)

# Etiqueta de aviso de formato incorrecto
label_carpeta_aviso = tk.Label(frame_contenedor, text="La fecha o formato es incorrecto", font=("Arial", 8, "italic"), fg=("gray"))  # Fuente de 10px
label_carpeta_aviso.grid(row=3, column=0, pady=2)
label_carpeta_aviso.grid_remove()  # Ocultar la etiqueta inicialmente

if not es_carpeta_correcta:
  centrar_ventana(root, 400, 420)
  label_carpeta_aviso.grid()  # Mostrar la etiqueta si la carpeta es incorrecta

"""
DISEÑO DE LOS BOTONES DE LA VENTANA PRINCIPAL
"""
# Frame general para organizar botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=15)

# Subframe superior - 3 botones centrados
frame_superior = tk.Frame(frame_botones)
frame_superior.pack()

""""
Frame superior contiene:
- Boton escaneo general
- Boton escaneo especial
"""
btn_escanear = tk.Button(frame_superior, text="Escaneo general", command= lambda: manejar_escaneo_general(datos_compartidos), width=15)
btn_escanear.pack(side="left", padx=10)

btn_jackpot = tk.Button(frame_superior, text="Escaneo especial", command= lambda: manejar_escaneo_especial(datos_compartidos), width=15)
btn_jackpot.pack(side="left", padx=10)

# Subframe inferior - 2 botones centrados
frame_inferior = tk.Frame(frame_botones)
frame_inferior.pack(pady=10)

""""
Frame inferior contiene:
- Boton escaneo simple
- Boton imprimir pizarras
"""
btn_simple = tk.Button(frame_inferior, text="Escaneo simple", command= lambda: manejar_escaneo_simple(datos_compartidos), width=15)
btn_simple.pack(side="left", padx=10)

btn_imprimir = tk.Button(frame_inferior, text="Imprimir pizarras", command= lambda: imprimir_pizarras(datos_compartidos), width=15)
btn_imprimir.pack(side="left", padx=10)

# Iniciar actualización del reloj
actualizar_reloj(root, label=label_fecha)

# Iniciar el bucle de la aplicación
root.mainloop()