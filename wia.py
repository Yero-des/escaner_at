import os
import win32com.client
from tkinter import messagebox

def escanear_documento(nombre_archivo, carpeta_destino, carpeta_actual, nombre_especial = ""):
    try:
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
            item.Properties["6146"].Value = 75  # DPI horizontal
            item.Properties["6147"].Value = 75  # DPI vertical
        except Exception as ex:
            print("No se pudieron configurar las propiedades del escáner:", ex)
        
        # Realizar el escaneo utilizando el método ShowAcquireImage
        image = wia_dialog.ShowAcquireImage()  # Inicia el escaneo con las configuraciones aplicadas
        if image is None:
            raise Exception("El escaneo fue cancelado o fallido.")
        
        destino = ""

        # Guardar la imagen escaneada en la carpeta destino
        if nombre_especial != "":
            destino = os.path.join(carpeta_destino, f"({nombre_especial}) {nombre_archivo} {carpeta_actual}.png")
        else:
            destino = os.path.join(carpeta_destino, f"{nombre_archivo} {carpeta_actual}.png")

        image.SaveFile(destino)
        
        messagebox.showinfo("Escaneo Exitoso", f"Archivo guardado como: {destino}")
    
    except Exception as e:
        messagebox.showerror("Error al Escanear", f"No se pudo escanear: {e}")

