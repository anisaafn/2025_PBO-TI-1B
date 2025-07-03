# setup_db.py
import sqlite3
from konfigurasi import DB_PATH

def setup_database():
    """Membuat database dan tabel pekerjaan dengan kolom catatan."""
    print(f"Membuat database di: {DB_PATH}")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pekerjaan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_perusahaan TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    status TEXT NOT NULL,
                    tanggal_lamar DATE NOT NULL,
                    catatan TEXT
                );
            """)
            print("Tabel 'pekerjaan' dengan kolom baru berhasil dibuat atau sudah ada.")
    except sqlite3.Error as e:
        print(f"Error saat membuat database: {e}")

if __name__ == "__main__":
    print("Menjalankan setup database...")
    print("Pastikan file database lama (jika ada) sudah dihapus untuk pembaruan skema.")
    setup_database()