import csv
import os
import time
from app.features.checkout import checkout
from app.features.wishlist import tambah_ke_wishlist

FILE_PROPERTI = 'data/properti.csv'

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
    item for item in semua_properti
    if (cari in item['nama'].lower() or cari in item['lokasi'].lower())
    and item['doc_verified'].strip().lower() == "true"
]

    print("\n=== Hasil Pencarian ===")
    if not hasil_cari:
        print("Tidak ada properti yang sesuai dengan pencarian Anda.")
        input("Tekan ENTER untuk kembali...")
    else:
        for p in hasil_cari:
            harga_txt = f"Rp {int(p['harga']):,}"
            print(f" +--------------------------------------+")
            print(f" | 🏠 {p['nama']:<32} |")
            print(f" | 📍 {p['lokasi']:<32} |")
            print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
            print(f" | ID: {p['id']} {' '*30}|")
            print(f" +--------------------------------------+")
    
    print("\n[ OPSI ]")
    print("1. 📅 Jadwalkan Survei")
    print("2. 🛒 Beli Sekarang (Checkout)")
    print("3. ➕ Tambahkan Ke Wishlist")
    print("0. 🔙 Kembali")
    print("----------------------------------------")
    
    pilihan = input(">> Pilih opsi: ")
    
    if pilihan == '1':
       print("COMING SOON: Fitur Jadwalkan Survei Properti!")
       time.sleep(2)
       input("Tekan ENTER untuk kembali...")
       return
    elif pilihan == '2':
        checkout(username,p)
    elif pilihan == '3':
        tambah_ke_wishlist(username, p['id'])
    elif pilihan == '0':
        return 

