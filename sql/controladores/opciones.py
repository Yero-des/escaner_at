import sqlite3
import tkinter as tk
from tkinter import messagebox

def cargar_opciones(tree, tipo):
  for fila in tree.get_children():
    tree.delete(fila)

  conn = sqlite3.connect('escaner.db')
  cursor = conn.cursor()
  cursor.execute('SELECT nombre, tipo, esta_activo FROM opciones WHERE tipo = ?', (tipo,))
  for opcion in cursor.fetchall():
    tree.insert('', tk.END, values=opcion.upper())

  conn.close()


def agregar_opcion(ventana, nombre, tipo, entry_nombre, cargar_opciones):

  if not nombre or not tipo:
    messagebox.showerror("Error", "Por favor, ingrese datos válidos")
    return
  
  nombre = nombre.upper()

  conn = sqlite3.connect('escaner.db')
  cursor = conn.cursor()
  cursor.execute('INSERT INTO opciones (nombre, tipo, esta_activo) VALUES (?, ?, ?)', (nombre, tipo, 1))
  conn.commit()
  conn.close()

  entry_nombre.delete(0, tk.END)

  cargar_opciones()
  messagebox.showinfo("Éxito", "Opción agregada exitosamente", parent=ventana)


def eliminar_opcion(tree, cargar_opciones):
  seleccion = tree.selection()

  if not seleccion:
    messagebox.showerror("Error", "Seleccione una opción para eliminar")
    return

  opcion_id = tree.item(seleccion[0])['values'][0]

  conn = sqlite3.connect('escaner.db')
  cursor = conn.cursor()
  cursor.execute('DELETE FROM opciones WHERE id = ?', (opcion_id,))
  conn.commit()
  conn.close()

  cargar_opciones()
  messagebox.showinfo("Éxito", "Opción eliminada exitosamente")


def actualizar_opcion(tree, entry_nombre, entry_tipo, check_activo, cargar_opciones):
  seleccion = tree.selection()

  if not seleccion:
    messagebox.showerror("Error", "Seleccione una opción para actualizar")
    return

  opcion_id = tree.item(seleccion[0])['values'][0]
  nombre = entry_nombre.get()
  tipo = entry_tipo.get()
  esta_activo = 1 if check_activo.get() else 0

  if not nombre or not tipo:
    messagebox.showerror("Error", "Por favor, ingrese datos válidos")
    return

  conn = sqlite3.connect('escaner.db')
  cursor = conn.cursor()
  cursor.execute('UPDATE opciones SET nombre = ?, tipo = ?, esta_activo = ? WHERE id = ?', (nombre, tipo, esta_activo, opcion_id))
  conn.commit()
  conn.close()

  entry_nombre.delete(0, tk.END)
  entry_tipo.delete(0, tk.END)
  check_activo.set(1)

  cargar_opciones()
  messagebox.showinfo("Éxito", "Opción actualizada exitosamente")