
import sqlite3
from datetime import datetime
from typing import Any

import pandas as pd
from pandas import DataFrame

from app.utils.root import add_project_root
add_project_root()
from app import DB_PATH
TABLE_NAME = "audit_etl"


def insert_audit_etl(node1=None, node2=None, node3=None, node4=None, result=None, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO audit_etl (date, node1, node2, node3, node4, result)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, node1, node2, node3, node4, result))
    conn.commit()
    conn.close()


def delete_audit_etl(db_path: str = DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()


def get_all_audit_etl(db_path: str = DB_PATH) -> DataFrame:
    # Dummy
    '''
    df = pd.DataFrame({
        "id": [1, 2],
        "date": ["2025-11-16 15:30:20", "2025-11-15 20:30:20"],
        "node1": ["OK", "OK"],
        "node2": ["OK", "ERROR"],
        "node3": ["OK", "-"],
        "node4": ["OK", "-"],
        "result": ["Completado", "Falló"]
    })
    '''
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("""SELECT * FROM audit_etl ORDER BY date DESC""", conn)
    conn.close()
    return df


def get_last_audit_etl(db_path: str = DB_PATH) -> DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("""SELECT * FROM audit_etl ORDER BY date DESC LIMIT 1""", conn)
    conn.close()
    return df
