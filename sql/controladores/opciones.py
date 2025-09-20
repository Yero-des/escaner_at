import sqlite3
import tkinter as tk
from tkinter import messagebox
from sql.db import datos_por_tipo, nombres_especial, nombres_principal, promociones, insertar_opciones

# Carga opciones activas desde la base de datos y las devuelve como diccionario
def cargar_opciones_por_tipo(tipo):
  conn = sqlite3.connect("escaner.db")
  cursor = conn.cursor()

  cursor.execute("""
    SELECT id, nombre, orden, tipo, activo
    FROM opciones
    WHERE tipo = ?
    ORDER BY orden ASC
  """, (tipo,))
  rows = cursor.fetchall()
  conn.close()

  # Convertir a diccionario: {id: {"nombre":..., "orden":..., "tipo":...}}
  datos = {
    row[0]: {"nombre": row[1], "orden": row[2], "tipo": row[3], "activo": row[4]}
    for row in rows
  }

  return datos

# Restablecer la tabla de opciones a su estado inicial con sus valores por defecto
def restablecer_opciones():

  # Confirmación del usuario antes de proceder
  respuesta = messagebox.askyesno(
    "Restablecer opciones",
    "¿Esta seguro que desea restablecer las opciones? esto eliminara todos los cambios realizados en la base de datos y no podran ser recuperados.",
    icon='warning' 
  )

  # Si el usuario elige "No", salir de la función y no ejecutar ningún cambio
  if respuesta == False:
    return

  conn = sqlite3.connect('escaner.db')
  cursor = conn.cursor()

  # Aseguramos que la tabla exista
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS opciones (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nombre TEXT NOT NULL,
      orden INTEGER NOT NULL,
      tipo TEXT NOT NULL CHECK(tipo IN ('principal', 'especial', 'promocion')),
      activo BOOLEAN NOT NULL DEFAULT 1,
      UNIQUE(nombre, tipo) -- 🔑 Aquí está la clave
    )
  ''')

  # Eliminar todos los registros (más rápido que borrar tabla)
  cursor.execute("DELETE FROM opciones")

  # Reiniciar contador de IDs (opcional, solo si quieres que empiece en 1 de nuevo)
  cursor.execute("DELETE FROM sqlite_sequence WHERE name='opciones'")

  insertar_opciones(cursor, nombres_especial, "especial")
  insertar_opciones(cursor, nombres_principal, "principal")
  insertar_opciones(cursor, promociones, "promocion")

  conn.commit()
  conn.close()

  messagebox.showinfo("Opciones restablecidas", "Las opciones han sido restablecidas a sus valores por defecto.")

# Logica que actualiza o agrega una opcion segun exista o no
def actualizar_o_agregar_opcion(cursor, opcion):

  nombre_actual = opcion["nombre"]
  tipo_actual = opcion["tipo"]
  orden_actual = opcion["orden"]
  esta_activo = opcion["activo"]

  # Resetear la secuencia antes de agregar nuevos registros
  cursor.execute("DELETE FROM sqlite_sequence WHERE name='opciones'")

  # Inserta dentro de la base de datos solo los datos nuevos 
  # - En caso de que el nombre y tipo ya existan, se actualiza el registro
  cursor.execute("""
    INSERT INTO opciones (nombre, tipo, orden, activo)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(nombre, tipo) DO UPDATE SET
      orden = excluded.orden,
      activo = excluded.activo
  """, (nombre_actual, tipo_actual, orden_actual, esta_activo))