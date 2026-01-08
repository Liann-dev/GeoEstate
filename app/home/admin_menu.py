import csv
import os
from app.features.seller_management import menu_kelola_seller
from app.features.admin_feedback import lihat_feedback
from app.features.user_verification import menu_verifikasi_user

def admin_menu(username):
    while True:
        print("\n" * 50) 
        print("===== MENU ADMIN =====")
        print("1. Verifikasi Data User")
        print("2. Kelola Data Seller")
        print("3. Lihat Feedback")
        print("0. Keluar / Logout")
        pilihan = input(f"\nPilih menu (0-3): ")

        if pilihan == "1":
            menu_verifikasi_user()
        elif pilihan == "2":
            menu_kelola_seller()
        elif pilihan == "3":
            lihat_feedback()
        elif pilihan == "0":
            print("\nLogout berhasil!")
            input("Tekan ENTER untuk kembali ke halaman awal...")
            print("\n" * 25)
            return
        else:
            print("Pilihan tidak valid.\n")