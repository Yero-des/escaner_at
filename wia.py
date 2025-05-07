import os
import win32com.client
from tkinter import messagebox, Toplevel, Label, Button
from PIL import Image, ImageTk
from resources import centrar_ventana_hija, icon_path

def escanear_documento(root, nombre_archivo, carpeta_destino, carpeta_actual, nombre_especial="", dpi=75):
    try:
        
        # Crear las carpetas faltantes EN CASO NO EXISTA
        if not os.path.exists(carpeta_destino):
            # Si no existe, la crea
            os.makedirs(carpeta_destino)

        # Crear un diálogo WIA
        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
        
        # Seleccionar el dispositivo de escaneo
        device_manager = win32com.client.Dispatch("WIA.DeviceManager")
        if device_manager.DeviceInfos.Count == 0:
            raise Exception("No se encontró ningún dispositivo de escaneo.")
        
        # Conectar al primer dispositivo disponible
        device = device_manager.DeviceInfos.Item(1).Connect()

        # Configurar propiedades del escáner (DPI horizontal y vertical)
        try:
            item = device.Items[1]
            item.Properties["6147"].Value = dpi  # DPI horizontal
            item.Properties["6148"].Value = dpi  # DPI vertical
        except Exception as ex:
            print("Advertencia: No se pudieron configurar algunas propiedades:", ex)
        
        # Realizar el escaneo utilizando el método ShowAcquireImage
        image = wia_dialog.ShowAcquireImage()  # Inicia el escaneo con las configuraciones aplicadas
        if image is None:
            raise Exception("El escaneo fue cancelado o fallido.")
        
        destino_temporal = os.path.join(carpeta_destino, "temporal_scan.png")

        # Guardar la imagen escaneada como PNG temporalmente
        image.SaveFile(destino_temporal)

        # Convertir la imagen PNG a JPG
        destino_final = ""
        nombre_final = ""

        if nombre_especial != "":
            nombre_final = f"({nombre_especial}) {nombre_archivo} {carpeta_actual}.jpg"
        else:
            nombre_final = f"{nombre_archivo} {carpeta_actual}.jpg"

        destino_final = os.path.join(carpeta_destino, nombre_final)

        with Image.open(destino_temporal) as img:
            img = img.convert("RGB")  # Convertir a RGB si es necesario
            img.save(destino_final, "JPEG")

        # Eliminar el archivo temporal
        os.remove(destino_temporal)

        # Mostrar ventana emergente con la imagen escaneada
        mostrar_resultado(destino_final, nombre_final, root)
        # messagebox.showinfo("Escaneo Exitoso", f"Archivo guardado como: {nombre_final}")


    except Exception as e:
        messagebox.showerror("Error al Escanear", f"No se pudo escanear: {e}")

def mostrar_resultado(ruta_imagen, nombre_archivo, root):

    ventana = Toplevel()
    ventana.title("Escaneo Exitoso")
    ventana.resizable(False, False)  # Evita que se redimensione
    ventana.iconbitmap(icon_path)
    ventana.grab_set()  # Hace la ventana modal (bloquea interacción con otras ventanas)
    ventana.focus_force()
    centrar_ventana_hija(ventana, 300, 390, root)

    # Cargar la imagen
    img = Image.open(ruta_imagen)
    img.thumbnail((250, 250))  # Redimensionar la imagen
    img_tk = ImageTk.PhotoImage(img)

    # Etiqueta con la imagen
    label_imagen = Label(ventana, image=img_tk)
    label_imagen.image = img_tk
    label_imagen.pack(pady=10)

    nombres_archivos = nombre_archivo.split(" - ")

    # Etiqueta con el mensaje
    label_texto = Label(ventana, text=f"Archivo guardado como:\n{nombres_archivos[0]} -\n{nombres_archivos[1]}", font=("Arial", 10))
    label_texto.pack()

    # Botón Aceptar
    btn_aceptar = Button(ventana, text="Aceptar", font=("Arial", 9), command=ventana.destroy)
    btn_aceptar.pack(pady=10)
    btn_aceptar.config(default="active")
    ventana.bind("<Return>", lambda event: ventana.destroy())

    ventana.wait_window()