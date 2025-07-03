# konfigurasi.py
import os

# Direktori dasar proyek
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Nama file database
NAMA_DB = 'lamaran_pekerjaan.db'

# Path lengkap ke file database
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

# Kategori Status Lamaran
KATEGORI_STATUS = ["Rencana Dilamar", "Sudah Apply", "Ditolak", "Diterima"]
