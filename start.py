import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from resources import *
from widgets.widget_opciones import *
from widgets.widgets_inicio import seleccionar_carpeta_destino

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

"""
DISEÑO DEL MENU DE VENTANA PRINCIPAL
"""
menu_bar = tk.Menu(root) # Crea un menú principal

# Establecer un diccionario con los datos que seran compartidos entre funciones
datos_compartidos = {
  "root": root,
  "icon_path": icon_path,
  "carpeta_destino": carpeta_destino,
  "carpeta_destino_no_modificable": carpeta_destino_no_modificable,
  "carpeta_actual": carpeta_actual,
}  

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
menu_bar.add_cascade(label="Configuración", menu=menu_opciones)

# ====== Menú de primer nivel que ejecuta algo directo ======
def accion_directa():
    print("Ejecutando acción directa...")  # aquí puedes llamar a tu función

menu_bar.add_command(label="Reejecutar", command=accion_directa)

# Asociar menú a la ventana
root.config(menu=menu_bar)

# Cargar imagen
imagen_original = Image.open(img_path)  # Reemplaza con la ruta de tu imagen
imagen_redimensionada = imagen_original.resize((400, 200))  # Ajustar tamaño
imagen = ImageTk.PhotoImage(imagen_redimensionada)

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

if not es_carpeta_correcta:
  centrar_ventana(root, 400, 420)

  # Etiqueta de aviso de formato incorrecto
  label_carpeta = tk.Label(frame_contenedor, text="La fecha o formato es incorrecto", font=("Arial", 8, "italic"), fg=("gray"))  # Fuente de 10px
  label_carpeta.grid(row=3, column=0, pady=2)

"""
DISEÑO DE LOS BOTONES DE LA VENTANA PRINCIPAL
"""
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