import sqlite3

def inicializar_db():
  conn = sqlite3.connect('escaner.db')
  cursor = conn.cursor()

  # Crear tabla con restricción en tipo
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS opciones (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nombre TEXT NOT NULL UNIQUE,
      tipo TEXT NOT NULL CHECK(tipo IN ('principal', 'especial', 'promocion')),
      esta_activo INTEGER NOT NULL DEFAULT 1
    )
  ''')
  conn.commit()

  # Listas de opciones por defecto
  nombres_especial = ["DNI FRONTAL", "DNI REVERSO", "JUGADA", "COMPROBANTE"]
  nombres_principal = ["KASNET", "NIUBIZ", "LOTTINGO", "GOLDEN", "BETSHOP", "VALE DE DESCUENTO"]
  opciones_web = ["MEGAJACKPOT", "LOTTINGO", "WEB RETAIL", "CUMPLEAÑERO"]

  # Insertar registros por defecto
  def insertar_opciones(lista, tipo):
    for nombre in lista:
      cursor.execute('''
        INSERT OR IGNORE INTO opciones (nombre, tipo, esta_activo)
        VALUES (?, ?, 1)
      ''', (nombre, tipo))

  insertar_opciones(nombres_especial, "especial")
  insertar_opciones(nombres_principal, "principal")
  insertar_opciones(opciones_web, "promocion")

  conn.commit()
  conn.close()