import sqlite3
import os

DATABASE_NAME = "finanzas.db"

def crear_tabla():
    """Crea la tabla 'movimientos' si no existe."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha DATE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insertar_movimiento(tipo, descripcion, monto, fecha):
    """Inserta un nuevo movimiento en la base de datos."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movimientos (tipo, descripcion, monto, fecha) VALUES (?, ?, ?, ?)", 
                   (tipo, descripcion, monto, fecha))
    conn.commit()
    conn.close()

def obtener_movimientos():
    """Obtiene todos los movimientos de la base de datos."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movimientos")
    movimientos = cursor.fetchall()
    conn.close()
    return movimientos

def actualizar_movimiento(id, tipo, descripcion, monto, fecha):
    """Actualiza un movimiento existente en la base de datos."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE movimientos SET tipo = ?, descripcion = ?, monto = ?, fecha = ? WHERE id = ?", 
                   (tipo, descripcion, monto, fecha, id))
    conn.commit()
    conn.close()

def borrar_movimiento(id):
    """Borra un movimiento de la base de datos."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movimientos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Aseguramos que la base de datos y la tabla se creen al iniciar
if not os.path.exists(DATABASE_NAME):
    crear_tabla()
