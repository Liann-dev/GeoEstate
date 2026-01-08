import csv
import os
from app.home.profile import profile
from app.home.properties import pilih_properti
from app.home.information import info
from app.home.detail_properti import detail_properti
from app.home.review_user import user_review
from app.features.feedback import collect_feedback
from app.features.chat import menu_chat
from app.features.wishlist import menu_wishlist
from app.features.jadwal_survey import lihat_jadwal_survey
from app.features.notifikasi_service import get_unread_notifikasi
from app.features.notifikasi_inbox_user import tampilkan_notifikasi_inbox
from app.features.transaksi_penjual import auto_expire_booking
import random

FILE_USERS = "data/users.csv"
FILE_PROPERTI = 'data/properti.csv'


def load_properties():
    data = []
    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, newline="", mode='r') as file:
            reader = csv.DictReader(file)
            data.extend(reader)
    return data


def home_user(username):
    while True:
        auto_expire_booking()
        semua_properti = load_properties()

        # ===== HITUNG UNREAD NOTIFIKASI =====
        unread = get_unread_notifikasi(username)
        jumlah = len(unread)

        print("\n" * 50)
        print(f" Halo, {username} 👋")
        print("========================================")

        
        # ===== FILTER PROPERTI AVAILABLE =====
        available_properti = [
            p for p in semua_properti
            if p.get("status", "").lower() == "available"
        ]

        # ===== RANDOM 3 REKOMENDASI =====
        rekomendasi = random.sample(
            available_properti,
            k=min(3, len(available_properti))
        )

        rekomendasi_ids = [p["id"] for p in rekomendasi]

        if rekomendasi:
            print(" 🔥 REKOMENDASI UNTUKMU:")
            for p in rekomendasi:
                harga_txt = f"Rp {int(p['harga']):,}"
                print(f" +--------------------------------------+")
                print(f" | 🏠 {p['nama']:<32} |")
                print(f" | 📍 {p['lokasi']:<32} |")
                print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
                print(f" | ID: {p['id']} {' '*30}|")
                print(f" +--------------------------------------+")
        else:
            print(" ⚠️  Belum ada properti tersedia saat ini.")


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

        elif pilihan == 'u':  # U = Ulasan
            user_review(username)

        elif pilihan == 'c':
            menu_chat(username)

        elif pilihan == 'u':
            user_review(username)

        elif pilihan == 'j':
            lihat_jadwal_survey(username)

        elif pilihan == 'f':
            collect_feedback(username)

        elif pilihan == 'w':
            menu_wishlist(username)

        elif pilihan == 'k':
            print("\nTerima kasih telah menggunakan GeoEstate.")
            input("Tekan ENTER untuk kembali...")
            return

        # ===== INPUT ANGKA (ID PROPERTI) =====
        elif pilihan.isdigit():
            if pilihan not in rekomendasi_ids:
                print(
                    "\n❌ ID Properti yang kamu ketik tidak ada di daftar Rekomendasi."
                    "\n👉 Coba cari tau lebih lanjut di [L] Lihat Semua Properti!"
                )
                input("Tekan ENTER...")
                continue

            item = next((p for p in rekomendasi if p["id"] == pilihan), None)
            if item:
                detail_properti(username, item)
            else:
                print("❌ Properti tidak ditemukan.")
                input("Tekan ENTER...")
        else:
            print("[!] Menu tidak dikenali.")
            input("Tekan ENTER...")

