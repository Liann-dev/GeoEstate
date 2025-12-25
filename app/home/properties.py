import csv
import os

from app.home.detail_properti import detail_properti
from app.features.transaksi_penjual import sedang_dalam_transaksi

FILE_PROPERTI = "data/properti.csv"
FILE_RIWAYAT = "data/properti_dimiliki.csv"

def to_bool(val):
    return str(val).strip().lower() == "true"

def print_card(p):
    harga_txt = f"Rp {int(p['harga']):,}"
    tersedia = to_bool(p.get('tersedia', 'true'))
    status = "✅ TERSEDIA" if tersedia else "❌ TERJUAL"

    print(f" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']:<10}{status:>20} |")
    print(f" +--------------------------------------+")

def get_properti_milik_user(username):
    properti_dimiliki = set()

    if not os.path.exists(FILE_RIWAYAT):
        return properti_dimiliki

    with open(FILE_RIWAYAT, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                properti_dimiliki.add(row['id'])

    return properti_dimiliki

def lihat_properti(username):
    if not os.path.exists(FILE_PROPERTI):
        print("Belum ada data properti.")
        return []

    semua_properti = []
    with open(FILE_PROPERTI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for p in reader:
            semua_properti.append(p)

    print("\n=== Properti Tersedia ===")
    properti_terverifikasi = []

    for p in semua_properti:
        if to_bool(p['doc_verified']):
            print_card(p)
            properti_terverifikasi.append(p)

    if not properti_terverifikasi:
        print("Belum ada properti yang terverifikasi saat ini.")
        input("Tekan ENTER untuk kembali...")

    return properti_terverifikasi

def pilih_properti(username):
    while True:
        properti_terverifikasi = lihat_properti(username)
        if not properti_terverifikasi:
            return

        properti_milik_user = get_properti_milik_user(username)

        print("----------------------------------------")
        print("Ketik ID Properti untuk Detail, Survei & Beli")
        print("Atau tekan ENTER langsung untuk Kembali")
        print("----------------------------------------")

        pilihan = input(">> Pilih ID Properti: ").strip()
        if not pilihan:
            break

        item_pilih = next(
            (item for item in properti_terverifikasi if item['id'] == pilihan),
            None
        )

        if not item_pilih:
            print("❌ Tidak ada properti dengan ID tersebut.")
            input("Tekan ENTER untuk kembali...")
            continue

        # ❌ Properti tidak tersedia
        if not to_bool(item_pilih.get('tersedia', 'true')):
            print("\n❌ Properti ini sudah terjual dan tidak tersedia.")
            input("Tekan ENTER untuk kembali...")
            continue

        # ❌ Sudah dimiliki user
        if pilihan in properti_milik_user:
            print("\n❌ Anda sudah memiliki properti ini.")
            input("Tekan ENTER untuk kembali...")
            continue

        # ❌ Sedang dalam transaksi
        if sedang_dalam_transaksi(username, pilihan):
            print("\n⏳ Properti ini sedang dalam proses transaksi Anda.")
            print("   Silakan tunggu hingga transaksi selesai.")
            input("Tekan ENTER untuk kembali...")
            continue

        # ✅ Aman → detail
        detail_properti(username, item_pilih)
