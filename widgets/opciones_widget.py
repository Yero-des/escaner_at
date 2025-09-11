import os
import locale
import re
from pathlib import Path
from PIL import Image
from wia import escanear_documento, imprimir_documento
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime
from resources import centrar_ventana_hija

def configurar_opciones_principales(datos_compartidos):

    # Extraer pantalla principal
    root = datos_compartidos["root"]
    
    # Crear una ventana emergente para elegir opciones
    ventana_opciones = tk.Toplevel(root)
    centrar_ventana_hija(ventana_opciones, 300, 100, root)

    ventana_opciones.title("Datos de escaneo")
    ventana_opciones.iconbitmap(datos_compartidos["icon_path"])
    ventana_opciones.resizable(False, False)
    ventana_opciones.focus_force()
    ventana_opciones.grab_set()

    # Botones y tabla del crud 
    
    ventana_opciones.mainloop()

def configurar_opciones_especiales(datos_compartidos):
    messagebox.showinfo("Opción 2", "Ejecutando opción 2...")

def configurar_promociones(datos_compartidos):
    messagebox.showinfo("Opción 3", "Ejecutando opción 3...")