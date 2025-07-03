# manajer_pekerjaan.py
import pandas as pd
import database
from model import Pekerjaan

class ManajerPekerjaan:
    """Mengelola logika bisnis untuk lamaran pekerjaan."""
    def tambah_pekerjaan(self, pekerjaan: Pekerjaan):
        """Menyimpan data pekerjaan baru ke database."""
        sql = "INSERT INTO pekerjaan (nama_perusahaan, latitude, longitude, status, tanggal_lamar, catatan) VALUES (?, ?, ?, ?, ?, ?)"
        tanggal_str = pekerjaan.tanggal_lamar.strftime('%Y-%m-%d')
        params = (pekerjaan.nama_perusahaan, pekerjaan.latitude, pekerjaan.longitude, pekerjaan.status, tanggal_str, pekerjaan.catatan)
        last_id = database.execute_query(sql, params)
        if last_id is not None:
            pekerjaan.id = last_id
            return True
        return False

    def get_semua_pekerjaan(self):
        """Mengambil semua data pekerjaan dari database."""
        query = "SELECT id, nama_perusahaan, tanggal_lamar as 'Tanggal Lamar', status, catatan, latitude, longitude FROM pekerjaan ORDER BY tanggal_lamar DESC, id DESC"
        df = database.get_dataframe(query)
        return df
    
    def get_pekerjaan_by_id(self, id_pekerjaan: int):
        """Mengambil satu data pekerjaan berdasarkan ID."""
        query = "SELECT * FROM pekerjaan WHERE id = ?"
        params = (id_pekerjaan,)
        
        df = database.get_dataframe(query, params=params)

        if not df.empty:
            row = df.iloc[0]
            
            try:
                import datetime
                # Format di DB adalah YYYY-MM-DD
                tgl_lamar_obj = datetime.datetime.strptime(row['tanggal_lamar'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                tgl_lamar_obj = datetime.date.today() # Fallback jika format salah

            return Pekerjaan(
                id_pekerjaan=int(row['id']),
                nama_perusahaan=row['nama_perusahaan'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                status=row['status'],
                tanggal_lamar=tgl_lamar_obj,
                catatan=row['catatan']
            )
        return None
        
    def hapus_pekerjaan(self, id_pekerjaan: int):
        """Menghapus data pekerjaan berdasarkan ID."""
        sql = "DELETE FROM pekerjaan WHERE id = ?"
        params = (id_pekerjaan,)
        try:
            database.execute_query(sql, params)
            return True
        except Exception as e:
            print(f"Error saat menghapus: {e}")
            return False
    
    def update_pekerjaan(self, id_pekerjaan: int, pekerjaan: Pekerjaan):
        """Memperbarui semua data lamaran pekerjaan berdasarkan ID."""
        sql = """UPDATE pekerjaan SET 
                    nama_perusahaan = ?,
                    tanggal_lamar = ?,
                    status = ?,
                    latitude = ?,
                    longitude = ?,
                    catatan = ?
                 WHERE id = ?"""
        params = (
            pekerjaan.nama_perusahaan,
            pekerjaan.tanggal_lamar.strftime('%Y-%m-%d'),
            pekerjaan.status,
            pekerjaan.latitude,
            pekerjaan.longitude,
            pekerjaan.catatan,
            id_pekerjaan
        )
        try:
            database.execute_query(sql, params)
            return True
        except Exception as e:
            print(f"Error saat memperbarui data: {e}")
            return False
            
    def get_ringkasan_status(self):
        """Menghitung jumlah pekerjaan untuk setiap status."""
        query = "SELECT status, COUNT(*) as jumlah FROM pekerjaan GROUP BY status"
        df = database.get_dataframe(query)
        if df.empty:
            return {}
        return pd.Series(df.jumlah.values, index=df.status).to_dict()