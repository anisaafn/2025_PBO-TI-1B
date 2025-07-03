# mini_project_sig.py

import pandas as pd
import folium
from abc import ABC, abstractmethod

class Lokasi(ABC):
    """Kelas dasar abstrak untuk semua jenis lokasi."""
    def __init__(self, nama: str, latitude: float, longitude: float):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude, self.longitude = float(latitude), float(longitude)
        except (ValueError, TypeError):
            self.latitude, self.longitude = 0.0, 0.0
    
    def get_koordinat(self) -> tuple:
        return (self.latitude, self.longitude)
    
    @abstractmethod
    def get_info_popup(self) -> str:
        """Metode abstrak untuk mendapatkan konten popup HTML."""
        pass
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}(nama='{self.nama}', lat={self.latitude:.4f}, lon={self.longitude:.4f})"

class TempatWisata(Lokasi):
    """Representasi untuk lokasi wisata."""
    def __init__(self, nama: str, latitude: float, longitude: float, jenis: str, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi."
    
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}<br><br><b>Koordinat:</b> ({self.latitude:.4f}, {self.longitude:.4f})"

class Kuliner(Lokasi):
    """Representasi untuk lokasi kuliner."""
    def __init__(self, nama: str, latitude: float, longitude: float, menu_andalan: str):
        super().__init__(nama, latitude, longitude)
        self.menu_andalan = str(menu_andalan) if menu_andalan else "Tidak diketahui"
    
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br><b>Menu Andalan:</b> {self.menu_andalan}<br><br><b>Koordinat:</b> ({self.latitude:.4f}, {self.longitude:.4f})"

class TempatIbadah(Lokasi):
    """Representasi untuk tempat ibadah."""
    def __init__(self, nama: str, latitude: float, longitude: float, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Ibadah"
        
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah</i><br><br>{self.deskripsi}<br><br><b>Koordinat:</b> ({self.latitude:.4f}, {self.longitude:.4f})"

# Kelas baru 
class Museum(Lokasi):
    """Representasi untuk lokasi museum."""
    def __init__(self, nama: str, latitude: float, longitude: float, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Informasi museum tidak tersedia."

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Museum</i><br><br>{self.deskripsi}<br><br><b>Koordinat:</b> ({self.latitude:.4f}, {self.longitude:.4f})"

# Kelas baru sesuai penugasan
class Kantor(Lokasi):
    """Representasi untuk lokasi kantor."""
    def __init__(self, nama: str, latitude: float, longitude: float, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Informasi kantor tidak tersedia."

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kantor Pemerintahan</i><br><br>{self.deskripsi}<br><br><b>Koordinat:</b> ({self.latitude:.4f}, {self.longitude:.4f})"



def baca_konfigurasi_peta(file_config: str) -> tuple:
    """Membaca konfigurasi peta [lat, lon, zoom] dari file teks."""
    # Nilai default jika file tidak ada atau error
    lat_default, lon_default, zoom_default = -6.9929, 110.4200, 12
    
    try:
        with open(file_config, 'r') as f:
            lines = f.readlines()
            lat = float(lines[0].strip())
            lon = float(lines[1].strip())
            zoom = int(lines[2].strip())
            print(f"Info: Konfigurasi peta berhasil dibaca dari '{file_config}'.")
            return (lat, lon, zoom)
    except FileNotFoundError:
        print(f"Peringatan: File '{file_config}' tidak ditemukan. Menggunakan nilai default.")
        return (lat_default, lon_default, zoom_default)
    except (ValueError, IndexError) as e:
        print(f"Peringatan: Error membaca '{file_config}' ({e}). Menggunakan nilai default.")
        return (lat_default, lon_default, zoom_default)



def baca_data_lokasi(nama_file: str) -> pd.DataFrame | None:
    """Membaca data lokasi dari file CSV menggunakan Pandas."""
    try:
        dataframe = pd.read_csv(nama_file)
        print(f"Info: File CSV '{nama_file}' berhasil dibaca.")
        return dataframe
    except FileNotFoundError:
        print(f"ERROR: File '{nama_file}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"ERROR saat membaca file CSV: {e}")
        return None

def buat_objek_lokasi_dari_df(dataframe: pd.DataFrame) -> list:
    """Mengiterasi DataFrame dan membuat list berisi objek lokasi."""
    list_objek_lokasi = []
    if dataframe is None or dataframe.empty:
        print("Peringatan: DataFrame kosong, tidak ada objek dibuat.")
        return list_objek_lokasi

    print("Info: Memulai pembuatan objek dari DataFrame...")
    for _, row in dataframe.iterrows():
        nama = row.get('Nama')
        lat = row.get('Latitude')
        lon = row.get('Longitude')
        tipe = row.get('Tipe', 'Lainnya')
        deskripsi = row.get('Deskripsi', '')
        
        if not all([nama, lat, lon]):
            continue

        objek = None
        if 'Wisata' in tipe or tipe in ['Landmark', 'Taman Kota']:
            objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
        elif tipe == 'Kuliner':
            objek = Kuliner(nama, lat, lon, deskripsi)
        elif tipe == 'Tempat Ibadah':
            objek = TempatIbadah(nama, lat, lon, deskripsi)
        elif tipe == 'Museum': # Pengenalan tipe baru
            objek = Museum(nama, lat, lon, deskripsi)
        elif tipe == 'Kantor Pemerintahan': # Pengenalan tipe baru
            objek = Kantor(nama, lat, lon, deskripsi)
        
        if objek:
            list_objek_lokasi.append(objek)
            
    print(f"Info: {len(list_objek_lokasi)} objek lokasi berhasil dibuat.")
    return list_objek_lokasi

def buat_peta_lokasi_folium(list_objek: list, file_output: str, file_config: str):
    """Membuat peta Folium interaktif dengan marker yang dikustomisasi."""
    
    # Membaca konfigurasi peta dari file
    lat_tengah, lon_tengah, zoom_awal = baca_konfigurasi_peta(file_config)
    
    if not list_objek:
        print("ERROR: Tidak ada objek lokasi untuk dipetakan.")
        return

    # Membuat objek peta dasar
    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=zoom_awal, tiles="OpenStreetMap")
    print(f"Info: Peta dibuat berpusat di ({lat_tengah}, {lon_tengah}) dengan zoom {zoom_awal}.")

    # B. KUSTOMISASI MARKER FOLIUM
    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat == (0.0, 0.0):
            continue

        # Menentukan ikon dan warna berdasarkan tipe objek
        icon_color, icon_name = 'gray', 'info-sign' # Default
        if isinstance(lok, TempatWisata):
            icon_color, icon_name = 'blue', 'camera'
        elif isinstance(lok, Kuliner):
            icon_color, icon_name = 'red', 'cutlery' # 'cutlery' adalah nama ikon dari Font Awesome
        elif isinstance(lok, TempatIbadah):
            icon_color, icon_name = 'green', 'home'
        elif isinstance(lok, Museum):
            icon_color, icon_name = 'darkblue', 'building'
        elif isinstance(lok, Kantor):
            icon_color, icon_name = 'cadetblue', 'briefcase'

        # Membuat marker dengan ikon kustom
        folium.Marker(
            location=koordinat,
            popup=folium.Popup(lok.get_info_popup(), max_width=300),
            tooltip=lok.nama,
            icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa') # prefix 'fa' untuk Font Awesome
        ).add_to(peta)
    
    try:
        peta.save(file_output)
        print(f"Info: Peta berhasil disimpan sebagai '{file_output}'.")
    except Exception as e:
        print(f"ERROR saat menyimpan peta: {e}")


# ----- Kode Utama ------
if __name__ == "__main__":
    NAMA_FILE_CSV = "lokasi_semarang_update.csv"
    NAMA_FILE_PETA = "peta_semarang_final.html"
    NAMA_FILE_CONFIG = "config_peta.txt"

    print("--- MEMULAI MINI PROJECT SISTEM INFORMASI GEOGRAFIS ---")
    
    # 1. Baca data dari CSV
    df_lokasi = baca_data_lokasi(NAMA_FILE_CSV)
    
    # 2. Buat objek dari data
    list_semua_lokasi = buat_objek_lokasi_dari_df(df_lokasi)
    
    # 3. Buat peta interaktif dari list objek
    buat_peta_lokasi_folium(list_semua_lokasi, NAMA_FILE_PETA, NAMA_FILE_CONFIG)
    
    print(f"\nProses selesai. Silakan buka file '{NAMA_FILE_PETA}' di browser Anda.")
    print("--- PROGRAM SELESAI ---")