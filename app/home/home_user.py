import csv
import os
from app.home.profile import profile
from app.home.properties import pilih_properti
from app.home.information import info
from app.home.detail_properti import detail_properti
<<<<<<< HEAD
from app.home.review_user import user_review
=======
from app.home.review_user import history_transaksi
>>>>>>> 593d3b75b4db0a525cf73050b6927cd6aae4ca89
from app.features.feedback import collect_feedback
from app.features.chat import menu_chat
from app.features.wishlist import menu_wishlist
from app.features.jadwal_survey import lihat_jadwal_survey

from app.features.notifikasi_service import get_unread_notifikasi
from app.features.notifikasi_inbox_user import tampilkan_notifikasi_inbox

FILE_PROPERTI = 'data/properti.csv'


def load_properties():
    data = []
    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='r') as file:
            reader = csv.DictReader(file)
            data.extend(reader)
    return data


def home_user(username):
    while True:
        semua_properti = load_properties()

        # ===== HITUNG UNREAD NOTIFIKASI =====
        unread = get_unread_notifikasi(username)
        jumlah = len(unread)

        print("\n" * 50)
        print(f" Halo, {username} 👋")
        print("========================================")

        print(" 🔥 REKOMENDASI UNTUKMU:")
        if not semua_properti:
            print("    (Belum ada data properti)")
        else:
            for p in semua_properti[:3]:
                harga_txt = f"Rp {int(p['harga']):,}"
                print(f" +--------------------------------------+")
                print(f" | 🏠 {p['nama']:<32} |")
                print(f" | 📍 {p['lokasi']:<32} |")
                print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
                print(f" | ID: {p['id']} {' '*30}|")
                print(f" +--------------------------------------+")

        print("----------------------------------------")

        if jumlah > 0:
            print(f" [N] Notifikasi Inbox [Ada {jumlah} Notifikasi]")
        else:
            print(" [N] Notifikasi Inbox")

        print(" [L] Lihat Semua Properti")
        print(" [P] Profil Saya")
        print(" [I] Informasi Umum")
        print(" [C] Kirim Pesan (Chat)")
        print(" [U] Ulasan Pembelian")
        print(" [J] Jadwal Survei")
        print(" [F] Feedback")
        print(" [W] Wishlist")
        print(" [K] Keluar / Logout")
        print("========================================")
        print(" KETIK: Huruf menu atau Angka ID Properti")

        pilihan = input(">> ").lower()

        if pilihan == 'n':
            tampilkan_notifikasi_inbox(username)

        elif pilihan == 'l':
            pilih_properti(username)

        elif pilihan == 'p':
            if profile(username) == "EXIT":
                return

        elif pilihan == 'i':
            info()
<<<<<<< HEAD
        elif pilihan == 'u':  # U = Ulasan
            user_review(username)
        elif pilihan == 'c':  # C = Chat
=======

        elif pilihan == 'c':
>>>>>>> 593d3b75b4db0a525cf73050b6927cd6aae4ca89
            menu_chat(username)

        elif pilihan == 'u':
            history_transaksi(username)

        elif pilihan == 'j':
            lihat_jadwal_survey(username)

        elif pilihan == 'f':
            collect_feedback(username, 'user')

        elif pilihan == 'w':
            menu_wishlist(username)

        elif pilihan == 'k':
            print("\nTerima kasih telah menggunakan GeoEstate.")
            input("Tekan ENTER untuk kembali...")
            return

        else:
            item = next((p for p in semua_properti if p['id'] == pilihan), None)
            if item:
                detail_properti(username, item)
            else:
                print("[!] Menu tidak dikenali.")
                input("Tekan ENTER...")
