import os
import time
import csv
from app.features.checkout import checkout
from app.features.wishlist import tambah_ke_wishlist

FILE_RIWAYAT = "data/properti_dimiliki.csv"

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

def detail_properti(username,p):

    harga_txt = f"Rp {int(p['harga']):,}" 
    print("\n" * 50)
    print("========================================")
    print("           DETAIL PROPERTI             ")
    print("========================================")
    print(f" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']} {' '*30}|")
    print(f" +--------------------------------------+")
    print(" | Status: ✅ Terverifikasi             |")
    print(f" | Penjual: {p['penjual']:<27} |")
    print(f" +--------------------------------------+")
    
    
    print("\n[ OPSI ]")
    print("1. 📅 Jadwalkan Survei")
    print("2. 🛒 Beli Sekarang (Checkout)")
    print("3. ➕ Tambahkan Ke Wishlist")
    print("0. 🔙 Kembali")
    print("----------------------------------------")
    
    while True:
        pilihan = input(">> Pilih opsi: ")
        
        if pilihan == '1':
            print("COMING SOON: Fitur Jadwalkan Survei Properti!")
            time.sleep(2)
            input("Tekan ENTER untuk kembali...")
            return
        elif pilihan == '2':
            if username == p['penjual']:
                print("Anda tidak bisa membeli properti anda sendiri!")
                input("Tekan ENTER untuk kembali...")
                return
            checkout(username,p)
            return
        elif pilihan == '3':
            if username == p['penjual']:
                print("Anda tidak bisa menambahkan properti anda sendiri ke Wishlist!")
                input("Tekan ENTER untuk kembali...")
                return
            tambah_ke_wishlist(username, p['id'])
            return
        elif pilihan == '0':
            return 
        else:
            print("Opsi tidak ditemukan!")
            continue