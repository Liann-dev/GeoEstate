import csv
import os

from app.home.detail_properti import detail_properti

FILE_PROPERTI = "data/properti.csv"

def print_card(p):
    harga_txt = f"Rp {int(p['harga']):,}" 
    print(f" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']} {' '*30}|")
    print(f" +--------------------------------------+")

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
        if p['doc_verified'].strip().lower() == "true":
            print_card(p)
            properti_terverifikasi.append(p)

    if not properti_terverifikasi:
        print("Belum ada properti yang terverifikasi saat ini.")
        input("Tekan ENTER untuk kembali...")

    return properti_terverifikasi

def pilih_properti(username):
    while True:
        properti_terverifikasi = lihat_properti(username)  # <-- dipanggil di tiap iterasi
        
        if not properti_terverifikasi:
            return

        print("----------------------------------------")
        print("Ketik ID Properti untuk Detail, Survei & Beli")
        print("Atau tekan ENTER langsung untuk Kembali")
        print("----------------------------------------")

        pilihan = input(">> Pilih ID Properti: ").strip()
        if not pilihan:
            break

        item_pilih = next((item for item in properti_terverifikasi if item['id'] == pilihan), None)

        if item_pilih:
            detail_properti(username, item_pilih)
        else:
            print("❌ Tidak ada properti dengan ID tersebut.")
            input("Tekan ENTER untuk kembali...")
