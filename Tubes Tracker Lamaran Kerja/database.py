# database.py
import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_db_connection():
    """Membuat dan mengembalikan koneksi ke database."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error koneksi database: {e}")
        return None

def execute_query(query, params=()):
    """Menjalankan query INSERT/UPDATE/DELETE."""
    with get_db_connection() as conn:
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"Query gagal: {e}")
                return None

def get_dataframe(query, params=()):
    """Mengambil data dari database dan mengembalikannya sebagai DataFrame."""
    with get_db_connection() as conn:
        if conn:
            try:
                return pd.read_sql_query(query, conn, params=params)
            except Exception as e:
                print(f"Gagal mengambil DataFrame: {e}")
                return pd.DataFrame()
    return pd.DataFrame()