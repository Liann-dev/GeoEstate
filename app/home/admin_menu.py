import csv
import os
from app.features.seller_management import menu_kelola_seller
from app.features.admin_feedback import lihat_feedback
from app.features.user_verification import menu_verifikasi_user
from app.features.suspend_user import suspend_user

def admin_menu(username):
    while True:
        print("\n" * 50) 
        print("===== MENU ADMIN =====")
        print("1. Kelola Verifikasi User")
        print("2. Kelola Verifikasi Seller")
        print("3. Suspend User/Seller")
        print("4. Lihat Feedback")
        print("0. Keluar / Logout")
        pilihan = input(f"\nPilih menu (0-4): ")

        if pilihan == "1":
            menu_verifikasi_user()
        elif pilihan == "2":
            menu_kelola_seller()
        elif pilihan == "3":
            suspend_user()
        elif pilihan == "4":
            lihat_feedback()
        elif pilihan == "0":
            print("\nLogout berhasil!")
            input("Tekan ENTER untuk kembali ke halaman awal...")
            print("\n" * 25)
            return
        else:
            print("Pilihan tidak valid.\n")