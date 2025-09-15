import os
import tkinter as tk
from tkinter import messagebox, ttk
from resources import centrar_ventana_hija
from sql.controladores.opciones import actualizar_opcion, agregar_opcion, cargar_opciones, eliminar_opcion

def configurar_opciones(datos_compartidos, tipo):

    # Extraer pantalla principal
    root = datos_compartidos["root"]
    icon_path = datos_compartidos["icon_path"]
    
    # Crear una ventana emergente para elegir opciones
    ventana_opciones = tk.Toplevel(root)
    centrar_ventana_hija(ventana_opciones, 500, 400, root)

    ventana_opciones.title("Opciones principales")
    ventana_opciones.iconbitmap(icon_path)
    ventana_opciones.resizable(False, False)
    ventana_opciones.focus_force()
    ventana_opciones.grab_set()

    # Input de nombre de opcion
    frame_form = tk.Frame(ventana_opciones)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    # Botones
    frame_buttons = tk.Frame(ventana_opciones)
    frame_buttons.pack(pady=10)

    btn_agregar = tk.Button(
    frame_buttons, 
    text="Agregar", 
    command=lambda: agregar_opcion(
        ventana=ventana_opciones,
        nombre=entry_nombre.get(), 
        tipo=tipo,
        entry_nombre=entry_nombre,
        cargar_opciones=lambda: cargar_opciones(tree, tipo))
    )
    btn_agregar.grid(row=0, column=0, padx=5)

    btn_actualizar = tk.Button(
    frame_buttons, 
    text="Actualizar", 
    # command=lambda: actualizar_opcion(tree, entry_nombre.get(), entry_edad.get(), entry_nombre, entry_edad, lambda: cargar_usuarios(tree))
    )
    btn_actualizar.grid(row=0, column=1, padx=5)

    btn_eliminar = tk.Button(
    frame_buttons, 
    text="Eliminar", 
    # command=lambda: eliminar_opcion(tree, lambda: cargar_opciones(tree))
    )
    btn_eliminar.grid(row=0, column=2, padx=5)

    # Tabla de usuarios
    frame_table = tk.Frame(ventana_opciones)
    frame_table.pack(pady=10)

    columns = ("Nombre", "Tipo", "Activo")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    # tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre") 
    tree.heading("Tipo", text="Tipo")
    tree.heading("Activo", text="Activo")

    # tree.column("ID", width=50)
    tree.column("Nombre", width=150)
    tree.column("Tipo", width=50)
    tree.column("Activo", width=150)

    tree.pack()

    cargar_opciones(tree, tipo)
    
    ventana_opciones.mainloop()

# Función para abrir la carpeta actual en el explorador de archivos
def ver_carpeta(datos_compartidos):

    carpeta_destino = datos_compartidos["carpeta_destino"]

    os.startfile(carpeta_destino)
    return