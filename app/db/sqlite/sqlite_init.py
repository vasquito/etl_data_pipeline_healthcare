import sqlite3
import os

from app.utils.root import add_project_root
add_project_root()
from app import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # v1
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_etl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            node1 TEXT,
            node2 TEXT,
            node3 TEXT,
            node4 TEXT,
            result TEXT,
            UNIQUE(id)
        )
    """)

    # v1
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_centers (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            direccion TEXT,
            barrio TEXT,
            comuna TEXT,
            telefono TEXT,
            web TEXT,
            area_progr TEXT,
            esp TEXT,
            lat REAL,
            lon REAL
        )
    """)

    conn.commit()
    conn.close()

def init_once():
    if not os.path.exists(DB_PATH):
        print("Inicializando base de datos SQLite...")
        init_db()
        print("Base de datos SQLite completada y inicializada...")
    else:
        print("Base de datos ya inicializada")

# Ejecutar una vez importado
init_once()
