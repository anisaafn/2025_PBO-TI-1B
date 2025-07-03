# app.py
import streamlit as st
import pandas as pd
import folium
import datetime
from streamlit_folium import st_folium
from manajer_pekerjaan import ManajerPekerjaan
from model import Pekerjaan
from konfigurasi import KATEGORI_STATUS

# --- Konfigurasi Halaman & Inisialisasi ---
st.set_page_config(page_title="Pelacak Lamaran", layout="wide")
manajer = ManajerPekerjaan()

# Pemetaan status ke warna marker untuk peta
WARNA_MARKER = { "Rencana Dilamar": "blue", "Sudah Apply": "orange", "Ditolak": "red", "Diterima": "green" }

# --- Sidebar untuk Input & Kontrol ---
with st.sidebar:
    daftar_pekerjaan_sidebar = manajer.get_semua_pekerjaan()

    st.header("📌 Tambah Lamaran Baru")
    with st.form("form_tambah", clear_on_submit=True):
        nama_perusahaan = st.text_input("Nama Perusahaan*", placeholder="Contoh: PT Herco Digital")
        tanggal_lamar = st.date_input("Tanggal Melamar*", value=datetime.date.today())
        status = st.selectbox("Status Awal*", KATEGORI_STATUS)
        with st.expander("Data Opsional"):
            latitude = st.text_input("Latitude", placeholder="-6.984369")
            longitude = st.text_input("Longitude", placeholder="110.431240")
            catatan = st.text_area("Catatan", placeholder="Contoh: Perlu siapkan CV dan portofolio data scientist.")
        
        if st.form_submit_button("Simpan Lamaran", use_container_width=True):
            lat_val = latitude if latitude else "0"
            lon_val = longitude if longitude else "0"
            try:
                pekerjaan_baru = Pekerjaan(nama_perusahaan, lat_val, lon_val, status, tanggal_lamar, catatan)
                if manajer.tambah_pekerjaan(pekerjaan_baru):
                    st.success("Lamaran berhasil disimpan!")
            except (ValueError, TypeError) as e:
                st.error(f"Error: {e}")

    st.divider()

    # --- Edit Data ---
    st.header("✏️ Edit Lamaran")
    if daftar_pekerjaan_sidebar.empty:
        st.info("Tidak ada data untuk diubah.")
    else:
        pilihan_lamaran_edit = [f"{row['id']} - {row['nama_perusahaan']}" for _, row in daftar_pekerjaan_sidebar.iterrows()]
        id_edit_pilihan = st.selectbox("Pilih lamaran untuk diedit", pilihan_lamaran_edit, index=None, placeholder="Pilih lamaran...")

        if id_edit_pilihan:
            id_to_edit = int(id_edit_pilihan.split(" - ")[0])
            data_lama = manajer.get_pekerjaan_by_id(id_to_edit)

            if data_lama:
                with st.form("form_edit"):
                    st.subheader(f"Mengedit: {data_lama.nama_perusahaan}")
                    edit_nama = st.text_input("Nama Perusahaan", value=data_lama.nama_perusahaan)
                    edit_tanggal = st.date_input("Tanggal Lamar", value=data_lama.tanggal_lamar)
                    edit_status = st.selectbox("Status Lamaran", KATEGORI_STATUS, index=KATEGORI_STATUS.index(data_lama.status))
                    edit_lat = st.text_input("Latitude", value=str(data_lama.latitude))
                    edit_lon = st.text_input("Longitude", value=str(data_lama.longitude))
                    edit_catatan = st.text_area("Catatan", value=data_lama.catatan)

                    if st.form_submit_button("Simpan Perubahan", use_container_width=True, type="primary"):
                        try:
                            pekerjaan_diperbarui = Pekerjaan(edit_nama, edit_lat, edit_lon, edit_status, edit_tanggal, edit_catatan)
                            if manajer.update_pekerjaan(id_to_edit, pekerjaan_diperbarui):
                                st.success("Data berhasil diperbarui!")
                                st.rerun()
                            else:
                                st.error("Gagal memperbarui data.")
                        except (ValueError, TypeError) as e:
                            st.error(f"Error: {e}")
    st.divider()

    # --- Hapus Data ---
    st.header("🗑️ Hapus Lamaran")
    if daftar_pekerjaan_sidebar.empty:
        st.info("Tidak ada data untuk dihapus.")
    else:
        pilihan_lamaran_hapus = [f"{row['id']} - {row['nama_perusahaan']}" for _, row in daftar_pekerjaan_sidebar.iterrows()]
        id_hapus_pilihan = st.selectbox("Pilih lamaran untuk dihapus", pilihan_lamaran_hapus, index=None, placeholder="Pilih lamaran...")
        
        if id_hapus_pilihan:
            id_to_delete = int(id_hapus_pilihan.split(" - ")[0])
            if st.button("Hapus Lamaran Terpilih", use_container_width=True, type="secondary"):
                st.session_state.id_confirm_delete = id_to_delete

# --- Tampilan Utama dengan Tabs ---
st.title("🗂️ Pelacak Lamaran Pekerjaan")

tab1, tab2, tab3 = st.tabs(["📊 Papan Status", "📜 Riwayat Lengkap", "🗺️ Peta Lamaran"])

with tab1:
    st.header("Ringkasan Status Lamaran")
    ringkasan = manajer.get_ringkasan_status()
    total_rencana = ringkasan.get("Rencana Dilamar", 0)
    total_apply = ringkasan.get("Sudah Apply", 0)
    total_diterima = ringkasan.get("Diterima", 0)
    total_ditolak = ringkasan.get("Ditolak", 0)

    col_met1, col_met2, col_met3, col_met4 = st.columns(4)
    col_met1.metric("Rencana Dilamar 📝", total_rencana)
    col_met2.metric("Sudah Apply 📩", total_apply)
    col_met3.metric("Diterima 🎉", total_diterima)
    col_met4.metric("Ditolak 😔", total_ditolak)
    
    # Logika konfirmasi penghapusan
    if 'id_confirm_delete' in st.session_state and st.session_state.id_confirm_delete:
        id_delete = st.session_state.id_confirm_delete
        nama_perusahaan_delete = manajer.get_pekerjaan_by_id(id_delete).nama_perusahaan
        st.warning(f"Anda yakin ingin menghapus lamaran untuk **{nama_perusahaan_delete}** (ID: {id_delete})?")
        col_confirm, col_cancel = st.columns(2)
        if col_confirm.button("Ya, Konfirmasi Hapus", type="primary", use_container_width=True):
            if manajer.hapus_pekerjaan(id_delete):
                del st.session_state.id_confirm_delete
                st.rerun()
        if col_cancel.button("Batal", use_container_width=True):
            del st.session_state.id_confirm_delete
            st.rerun()

with tab2:
    st.header("Riwayat Lengkap Lamaran")
    daftar_pekerjaan = manajer.get_semua_pekerjaan()
    if daftar_pekerjaan.empty:
        st.info("Belum ada data lamaran yang tercatat.")
    else:
        st.dataframe(daftar_pekerjaan.drop(columns=['latitude', 'longitude']), use_container_width=True, hide_index=True)

with tab3:
    st.header("Peta Sebaran Lokasi Lamaran")
    peta_pekerjaan = manajer.get_semua_pekerjaan()
    peta_pekerjaan_valid = peta_pekerjaan[(peta_pekerjaan['latitude'] != 0.0) & (peta_pekerjaan['longitude'] != 0.0)]
    
    # --- Fitur Pencarian Peta ---
    nama_perusahaan_list = ["Semua Lokasi"] + peta_pekerjaan_valid['nama_perusahaan'].tolist()
    cari_perusahaan = st.selectbox("Cari Alamat Lamaran", nama_perusahaan_list)
    
    # Tentukan pusat peta
    map_center = [-6.9175, 107.6191] # Default Bandung
    zoom_level = 9
    
    if cari_perusahaan != "Semua Lokasi":
        lokasi_terpilih = peta_pekerjaan_valid[peta_pekerjaan_valid['nama_perusahaan'] == cari_perusahaan].iloc[0]
        map_center = [lokasi_terpilih['latitude'], lokasi_terpilih['longitude']]
        zoom_level = 15 # Zoom lebih dekat saat mencari
    elif not peta_pekerjaan_valid.empty:
        map_center = [peta_pekerjaan_valid.iloc[0]['latitude'], peta_pekerjaan_valid.iloc[0]['longitude']]
        zoom_level = 11

    # Buat Peta Folium
    m = folium.Map(location=map_center, zoom_start=zoom_level)

    # Tambahkan marker ke peta
    if not peta_pekerjaan_valid.empty:
        for _, row in peta_pekerjaan_valid.iterrows():
            warna_ikon = WARNA_MARKER.get(row['status'], 'gray')
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"<b>{row['nama_perusahaan']}</b><br>Status: {row['status']}",
                tooltip=f"{row['nama_perusahaan']} ({row['status']})",
                icon=folium.Icon(color=warna_ikon, icon='briefcase', prefix='fa')
            ).add_to(m)
    
    st_folium(m, use_container_width=True, height=600)