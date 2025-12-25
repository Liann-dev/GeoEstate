import csv
import os
import time
from app.features.transaksi_penjual import sedang_dalam_transaksi
from app.home.detail_properti import detail_properti
from app.home.properties import get_properti_milik_user

FILE_PROPERTI = 'data/properti.csv'

def to_bool_cari(val):
    return str(val).strip().lower() == "true"

def load_properties():
    data = []
    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    return data

def cari_properti(username):
    cari = input("Masukkan kata kunci lokasi atau nama properti: ").lower()
    semua_properti = load_properties()

    hasil_cari = [
        p for p in semua_properti
        if (cari in p['nama'].lower() or cari in p['lokasi'].lower())
        and to_bool_cari(p['doc_verified'])
    ]

    print("\n=== Hasil Pencarian ===")
    if not hasil_cari:
        print("Tidak ada properti yang sesuai dengan pencarian Anda.")
        input("Tekan ENTER untuk kembali...")
        return

    properti_milik_user = get_properti_milik_user(username)

    # =======================
    # TAMPILKAN CARD PROPERTI
    # =======================
    for p in hasil_cari:
        harga_txt = f"Rp {int(p['harga']):,}"
        tersedia = to_bool_cari(p['tersedia'])
        status = "✅ TERSEDIA" if tersedia else "❌ TERJUAL"

        print(f" +--------------------------------------+")
        print(f" | 🏠 {p['nama']:<32} |")
        print(f" | 📍 {p['lokasi']:<32} |")
        print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
        print(f" | ID: {p['id']:<10}{status:>20} |")
        print(f" +--------------------------------------+")

    print("----------------------------------------")
    print("Ketik ID Properti untuk Detail, Survei & Beli")
    print("Atau tekan ENTER langsung untuk Kembali")
    print("----------------------------------------")

    pilihan = input(">> Pilih ID Properti: ").strip()
    if not pilihan:
        return

    properti_dipilih = next((p for p in hasil_cari if p['id'] == pilihan), None)

    if not properti_dipilih:
        print("❌ Tidak ada properti dengan ID tersebut.")
        input("Tekan ENTER untuk kembali...")
        return

    # =======================
    # VALIDASI PEMBELIAN
    # =======================
    if not to_bool_cari(properti_dipilih['tersedia']):
        print("\n❌ Properti ini sudah terjual dan tidak tersedia.")
        input("Tekan ENTER untuk kembali...")
        return

    if pilihan in properti_milik_user:
        print("\n❌ Anda sudah memiliki properti ini.")
        input("Tekan ENTER untuk kembali...")
        return

    if sedang_dalam_transaksi(username, pilihan):
        print("\n⏳ Properti ini sedang dalam proses transaksi Anda.")
        print("   Silakan tunggu hingga transaksi selesai.")
        input("Tekan ENTER untuk kembali...")
        return

    # =======================
    # LANJUT KE DETAIL
    # =======================
    detail_properti(username, properti_dipilih)