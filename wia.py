import os
import win32com.client
from tkinter import messagebox
from PIL import Image

def escanear_documento(nombre_archivo, carpeta_destino, carpeta_actual, nombre_especial="", dpi=75):
    try:
        
        # Crear la carpeta /PROMOCIONES EN CASO NO EXISTA
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

        messagebox.showinfo("Escaneo Exitoso", f"Archivo guardado como: {nombre_final}")

    except Exception as e:
        messagebox.showerror("Error al Escanear", f"No se pudo escanear: {e}")
