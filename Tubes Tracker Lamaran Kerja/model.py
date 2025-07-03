# model.py
import datetime
from konfigurasi import KATEGORI_STATUS

class Pekerjaan:
    """Merepresentasikan satu entitas lamaran pekerjaan."""
    def __init__(self, nama_perusahaan, latitude, longitude, status, tanggal_lamar, catatan="", id_pekerjaan=None):
        if not nama_perusahaan:
            raise ValueError("Nama perusahaan tidak boleh kosong.")
        if status not in KATEGORI_STATUS:
            raise ValueError(f"Status tidak valid. Pilih dari: {KATEGORI_STATUS}")
        if not isinstance(tanggal_lamar, datetime.date):
            raise TypeError("Format tanggal tidak valid.")

        self.id = id_pekerjaan
        self.nama_perusahaan = str(nama_perusahaan)
        self.status = status
        self.tanggal_lamar = tanggal_lamar
        self.catatan = str(catatan)
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Latitude dan Longitude harus berupa angka yang valid.")

    def __repr__(self):
        return (f"Pekerjaan(ID: {self.id}, Perusahaan: '{self.nama_perusahaan}', "
                f"Status: {self.status}, Tanggal: {self.tanggal_lamar})")