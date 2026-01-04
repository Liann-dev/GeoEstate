import csv
import os
import time

from app.features.checkout import checkout
from app.features.wishlist import tambah_ke_wishlist
from app.features.jadwal_survey import survey

FILE_USERS = "data/users.csv"

def to_bool(val):
    return str(val).strip().lower() == "true"

def get_user_verified(username):
    if not os.path.exists(FILE_USERS):
        return False

    with open(FILE_USERS, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user['username'].strip().lower() == username.strip().lower():
                return user.get('user_verified', '').strip().lower() == 'true'

    return False

def detail_properti(username, p):

    tersedia = to_bool(p.get('tersedia', 'true'))
    harga_txt = f"Rp {int(p['harga']):,}"

    print("\n" * 50)
    print("========================================")
    print("           DETAIL PROPERTI               ")
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
    print("2. 🛒 Booking")
    print("3. ➕ Tambahkan Ke Wishlist")
    print("0. 🔙 Kembali")
    print("----------------------------------------")

    while True:
        pilihan = input(">> Pilih opsi: ")

        if pilihan == '1':
            
            if not get_user_verified(username):
                print("Anda belum terverifikasi!")
                input("Tekan ENTER untuk kembali...")
                return
            
            if not tersedia:
                print("❌ Properti sudah terjual.")
                input("Tekan ENTER untuk kembali...")
                continue

            if username == p['penjual']:
                print("Anda tidak bisa menjadwalkan survei properti anda sendiri!")
                input("Tekan ENTER untuk kembali...")
                return
            
            survey(username, p)
            return


        elif pilihan == '2':

            if not get_user_verified(username):
                print("Anda belum terverifikasi!")
                input("Tekan ENTER untuk kembali...")
                return

            if not tersedia:
                print("❌ Properti sudah terjual.")
                input("Tekan ENTER untuk kembali...")
                continue

            if username == p['penjual']:
                print("Anda tidak bisa membeli properti anda sendiri!")
                input("Tekan ENTER untuk kembali...")
                return

            checkout(username, p)
            return

        elif pilihan == '3':

            if not get_user_verified(username):
                print("Anda belum terverifikasi!")
                input("Tekan ENTER untuk kembali...")
                return
  
            if not tersedia:
                print("❌ Properti sudah terjual.")
                input("Tekan ENTER untuk kembali...")
                continue

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
