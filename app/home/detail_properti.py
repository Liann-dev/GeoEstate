import csv
import os

from app.features.checkout import checkout
from app.features.wishlist import tambah_ke_wishlist
from app.features.jadwal_survey import survey
from app.features.chat import buka_chat, normalize_session

FILE_USERS = "data/users.csv"


# =========================
# USER VERIFIED
# =========================
def get_user_verified(username):
    if not os.path.exists(FILE_USERS):
        return False

    with open(FILE_USERS, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user["username"].lower() == username.lower():
                return user.get("user_verified", "").lower() == "true"
    return False


# =========================
# DETAIL PROPERTI
# =========================
def detail_properti(username, p):
    harga_txt = f"Rp {int(p['harga']):,}"

    print("\n" * 50)
    print("========================================")
    print("           DETAIL PROPERTI               ")
    print("========================================")
    print(f" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']:<35}|")
    print(f" +--------------------------------------+")
    print(" | Status  : ✅ Terverifikasi           |")
    print(f" | Penjual : {p['penjual']:<27} |")
    print(f" +--------------------------------------+")

    print("\n[ OPSI ]")
    print("1. 📅 Jadwalkan Survei")
    print("2. 🛒 Booking")
    print("3. ➕ Tambahkan ke Wishlist")
    print("4. 💬 Chat Penjual")
    print("0. 🔙 Kembali")
    print("----------------------------------------")

    while True:
        pilihan = input(">> Pilih opsi: ").strip()

        if pilihan == "1":
            if not get_user_verified(username):
                print("❌ Anda belum terverifikasi!")
                input("Tekan ENTER...")
                return

            if username == p["penjual"]:
                print("❌ Tidak bisa survei properti sendiri!")
                input("Tekan ENTER...")
                return

            survey(username, p)
            return

        elif pilihan == "2":
            if not get_user_verified(username):
                print("❌ Anda belum terverifikasi!")
                input("Tekan ENTER...")
                return

            if username == p["penjual"]:
                print("❌ Tidak bisa membeli properti sendiri!")
                input("Tekan ENTER...")
                return

            checkout(username, p)
            return

        elif pilihan == "3":
            if not get_user_verified(username):
                print("❌ Anda belum terverifikasi!")
                input("Tekan ENTER...")
                return

            if username == p["penjual"]:
                print("❌ Tidak bisa wishlist properti sendiri!")
                input("Tekan ENTER...")
                return

            tambah_ke_wishlist(username, p["id"])
            return

        elif pilihan == "4":
            if username == p["penjual"]:
                print("❌ Anda tidak bisa chat diri sendiri!")
                input("Tekan ENTER...")
                return

            session_id = normalize_session(username, p["penjual"])
            buka_chat(username, session_id, p["penjual"])
            return

        elif pilihan == "0":
            return

        else:
            print("❌ Opsi tidak valid!")
