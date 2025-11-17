
import sqlite3
from datetime import datetime
from typing import Any

import pandas as pd
from pandas import DataFrame

from app.utils.root import add_project_root
add_project_root()
from app import DB_PATH
TABLE_NAME = "medical_centers"

def insert_dataframe(df: pd.DataFrame, db_path: str = DB_PATH):
    with sqlite3.connect(db_path) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
        #df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)


def find_all(db_path: str = DB_PATH) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)


def find_by_comuna(comuna: str, db_path: str = DB_PATH) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        query = f"SELECT * FROM {TABLE_NAME} WHERE comuna = ?"
        return pd.read_sql(query, conn, params=(comuna,))


def delete_medical_centers(db_path: str = DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()
