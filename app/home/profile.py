import csv
import os
import time

from app.home.history_transaksi import history_transaksi
from app.home.jual_properti import jual_kembali_properti
from app.features.seller_register import seller_registration_menu
from app.features.biometric_toggle import toggle_biometrik
from app.auth.lupa_password import ganti_password
from app.home.seller_menu import seller_menu
from app.Utils.animation import loading_seller_transition 

FILE_USERS = "data/users.csv"
FILE_RIWAYAT = "data/properti_dimiliki.csv"
FILE_BIODATA = "data/biodata.csv"


# =========================
# PROPERTI DIMILIKI
# =========================
def properti_saya(username):
    if not os.path.exists(FILE_RIWAYAT):
        print("\nBelum ada riwayat pembelian.")
        input("Tekan ENTER untuk kembali...")
        return

    hasil = []
    with open(FILE_RIWAYAT, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                hasil.append(row)

    if not hasil:
        print("\nAnda belum membeli properti apa pun.")
        input("Tekan ENTER untuk kembali...")
        return

    print("\n=== PROPERTI YANG TELAH ANDA BELI ===")
    for i, p in enumerate(hasil, 1):
        print("-" * 50)
        print(f"{i}. {p['nama']} ({p['kategori']})")
        print(f"   ID Properti  : {p['id']}")
        print(f"   Lokasi       : {p['lokasi']}")
        print(f"   Harga        : Rp {int(p['harga']):,}")
        print(f"   Penjual      : {p['penjual']}")
        print(f"   ID Transaksi : {p['id_transaksi']}")
        print(f"   Tanggal Beli : {p['tanggal']}")

    print("-" * 50)
    print("\n[ OPSI ]")
    print("1. 💲 Jual Kembali Properti")
    print("0. 🔙 Kembali")

    while True:
        pilihan = input("\n>> Pilih opsi: ").strip()
        if pilihan == "1":
            jual_kembali_properti(username)
            return
        elif pilihan == "0":
            return
        else:
            print("Pilihan tidak valid!")


# =========================
# INFORMASI PRIBADI
# =========================
def informasi_pribadi(username):
    if not os.path.exists(FILE_BIODATA):
        print("\n❌ Data biodata belum tersedia.")
        input("Tekan ENTER untuk kembali...")
        return

    with open(FILE_BIODATA, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                print("\n=== INFORMASI PRIBADI ===")
                for k, v in row.items():
                    print(f"{k.replace('_',' ').title():<22}: {v}")
                input("\nTekan ENTER untuk kembali...")
                return

    print("\n❌ Data biodata belum ditemukan.")
    print("Silakan ajukan verifikasi data terlebih dahulu.")
    input("Tekan ENTER untuk kembali...")


# =========================
# PROFILE MENU
# =========================
def profile(username):
    while True:
        user_data = None

        if os.path.exists(FILE_USERS):
            with open(FILE_USERS, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for user in reader:
                    if user["username"] == username:
                        user_data = user
                        break

        if not user_data:
            print("❌ Data pengguna tidak ditemukan.")
            return

        print("\n========================================")
        print("              PROFIL SAYA               ")
        print("========================================")
        print(f"👤 Username : {user_data['username']}")
        print(f"🛡️  Role     : {user_data['role'].capitalize()}")

        status = "✅ Terverifikasi" if user_data["user_verified"] == "true" else "Belum Terverifikasi ⚠️"
        print(f"📌 Status   : {status}")
        print("----------------------------------------")

        print(" [I] Informasi Pribadi")
        print(" [H] History Transaksi")
        print(" [P] Properti Saya")
        print(" [K] Keamanan & Password")
        if user_data["user_verified"] == "false":
            print(" [V] Ajukan Verifikasi Data User")
        if user_data["role"] == "user":
            print(" [M] Daftar Sebagai Seller")
        if user_data['role'] == "seller":
            print(" [M] Menu Seller")
        print(" [B] Kembali")
        pilihan = input("\nPilih menu: ").lower().strip()

        # =========================
        # INFORMASI PRIBADI (FIX UX)
        # =========================
        if pilihan == "i":
            if user_data["user_verified"] == "false":
                print("\n⚠️  Data Anda belum terverifikasi.")
                print("Silakan ajukan verifikasi terlebih dahulu.")
                input("Tekan ENTER untuk kembali ke menu Profil...")
                continue  # ✅ KEMBALI KE PROFILE, BUKAN HOME
            informasi_pribadi(username)

        elif pilihan == "h":
            history_transaksi(username)

        elif pilihan == "p":
            properti_saya(username)

        elif pilihan == "k":
            while True:
                print("\n===== Keamanan & Password =====")
                print("1. Ganti Password")
                print("2. Login Biometrik")
                print("0. Kembali")

                pilih = input("Pilih menu: ").strip()
                if pilih == "1":
                    result = ganti_password()
                    if result == "EXIT":
                        return "EXIT"
                elif pilih == "2":
                    toggle_biometrik(username)
                elif pilih == "0":
                    break
                else:
                    print("Pilihan tidak valid!")

        elif pilihan == "v":
            if user_data["user_verified"] == "false":
                from app.features.user_verification_request import (
                    has_active_request,
                    ajukan_verifikasi_user
                )
                if has_active_request(username):
                    print("\n❌ Anda sudah mengajukan verifikasi dan sedang diproses oleh Admin.")
                    input("Tekan ENTER...")
                else:
                    ajukan_verifikasi_user(username)

        elif pilihan == "m":
            if user_data["role"] == "user" and user_data["user_verified"] == "false" :
                print("\n❌ Akun belum terverifikasi.")
                print("Silakan lakukan verifikasi data terlebih dahulu")
                input("Tekan ENTER...")
                continue
            elif user_data['role'] == "user" and user_data["user_verified"] == "true":
                seller_registration_menu(username)
            elif user_data['role'] == "seller":
                loading_seller_transition()
                seller_menu(username)
            else:
                print("Pilihan tidak valid!")

        elif pilihan == "b":
            break

        else:
            print("Pilihan tidak valid!")
