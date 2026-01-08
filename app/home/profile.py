import csv
import os
import time

from app.home.history_transaksi import history_transaksi
from app.features.seller_register import seller_registration_menu
from app.features.biometric_toggle import toggle_biometrik
from app.auth.lupa_password import ganti_password
from app.home.seller_menu import seller_menu
from app.Utils.animation import loading_seller_transition

FILE_USERS = "data/users.csv"
FILE_RIWAYAT = "data/properti_dibeli.csv"
FILE_BIODATA = "data/biodata.csv"
FILE_REQUEST = "data/user_verification_requests.csv"


# =========================
# UTIL - REQUEST TERAKHIR
# =========================
def get_latest_verification_request(username):
    if not os.path.exists(FILE_REQUEST):
        return None

    latest = None
    with open(FILE_REQUEST, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                latest = row
    return latest


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
    input("\nTekan ENTER untuk kembali...")


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
# PROFILE MENU (FINAL)
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

        # ===== STATUS VERIFIKASI =====
        verification_status = ""
        admin_note = None
        request = get_latest_verification_request(username)

        if user_data["user_verified"] == "true":
            verification_status = "✅ Terverifikasi"
        else:
            if request:
                if request["status"] == "pending":
                    verification_status = "⏳ Verifikasi sedang diproses"
                elif request["status"] == "rejected":
                    verification_status = "❌ Verifikasi ditolak"
                    admin_note = request.get("admin_note")
                else:
                    verification_status = "⚠️  Belum Terverifikasi"
            else:
                verification_status = "⚠️  Belum Terverifikasi"

        print("\n========================================")
        print("              PROFIL SAYA               ")
        print("========================================")
        print(f"👤 Username : {user_data['username']}")
        print(f"🛡️  Role     : {user_data['role'].capitalize()}")
        print(f"📌 Status   : {verification_status}")

        if admin_note:
            print(f"📝 Catatan  : {admin_note}")

        print("----------------------------------------")
        print(" [I] Informasi Pribadi")
        print(" [H] History Transaksi")
        print(" [P] Properti yang Pernah Dibeli")
        print(" [K] Keamanan & Password")

        if user_data["user_verified"] == "false":
            if not request or request["status"] != "pending":
                print(" [V] Ajukan Verifikasi Data User")

        if user_data["role"] == "user":
            print(" [M] Daftar Sebagai Seller")
        elif user_data["role"] == "seller":
            print(" [M] Menu Seller")

        print(" [B] Kembali")
        pilihan = input("\nPilih menu: ").lower().strip()

        if pilihan == "i":
            if user_data["user_verified"] == "false":
                print("\n⚠️  Data Anda belum terverifikasi.")
                input("Tekan ENTER untuk kembali ke menu Profil...")
                continue
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
            from app.features.user_verification_request import (
                has_active_request,
                ajukan_verifikasi_user
            )
            if has_active_request(username):
                print("\n⏳ Verifikasi Anda sedang diproses Admin.")
                input("Tekan ENTER...")
            else:
                ajukan_verifikasi_user(username)

        elif pilihan == "m":
            if user_data["role"] == "user" and user_data["user_verified"] == "false":
                print("\n⚠️  Data Anda belum terverifikasi.")
                input("Tekan ENTER...")
            elif user_data["role"] == "user":
                seller_registration_menu(username)
            elif user_data["role"] == "seller":
                print("\n" * 25)
                loading_seller_transition()
                print("\n" * 25)
                seller_menu(username)

        elif pilihan == "b":
            break

        else:
            print("Pilihan tidak valid!")
