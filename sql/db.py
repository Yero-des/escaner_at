import os
import sqlite3

# Listas de opciones por defecto (ahora solo strings)
nombres_especial = [
  "DNI FRONTAL", "DNI REVERSO", "JUGADA", "COMPROBANTE"
]
nombres_principal = [
  "KASNET", "NIUBIZ", "REPORTE NIUBIZ", "LOTTINGO",
  "GOLDEN", "BETSHOP", "VALE DE DESCUENTO"
]
promociones = [
  "MEGAJACKPOT", "GANADOR LOTTINGO", "WEB RETAIL", "CUMPLEAÑERO"
]

"""
Ruta de la base de datos en AppData\\Local
"""
base_path = os.path.join(os.environ["LOCALAPPDATA"], "EscanerAT")
os.makedirs(base_path, exist_ok=True)
ruta_db = os.path.join(base_path, "escaner.db")

# Insertar registros por defecto
def insertar_opciones(cursor, lista, tipo, inicializar=False):

  for orden, nombre in enumerate(lista, start=1):  # orden según llegada
    try:
      # Resetear la secuencia solo al inicializar completamente
      if inicializar:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='opciones'")
      cursor.execute('''
        INSERT OR IGNORE INTO opciones (nombre, orden, tipo, activo)
        VALUES (?, ?, ?, 1)
      ''', (nombre, orden, tipo))
    except Exception as e:
      print(f"⚠️ Error al guardar {nombre}: {e}")

# Inicializar la base de datos con las tablas y datos por defecto
def inicializar_db():
  conn = sqlite3.connect(ruta_db)
  cursor = conn.cursor()

  # Crear tabla con restricción de unicidad por (nombre, tipo)
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

  insertar_opciones(cursor, nombres_especial, "especial", inicializar=True)
  insertar_opciones(cursor, nombres_principal, "principal", inicializar=True)
  insertar_opciones(cursor, promociones, "promocion", inicializar=True)

  conn.commit()
  conn.close()

def datos_por_tipo(tipo):
  conn = sqlite3.connect(ruta_db)
  cursor = conn.cursor()
  
  cursor.execute("""
    SELECT nombre 
    FROM opciones 
    WHERE tipo = ? AND activo = 1
    ORDER BY orden ASC
  """, (tipo,))

  # Extraer solo los nombres de las filas obtenidas
  nombres = [fila[0] for fila in cursor.fetchall()]

  conn.close()
  return nombres