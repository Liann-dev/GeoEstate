import csv
import os
import time
from app.home.history_transaksi import history_transaksi
from app.home.jual_properti import jual_kembali_properti
from app.features.seller_register import seller_registration_menu
from app.features.biometric_toggle import toggle_biometrik
from app.auth.lupa_password import ganti_password

FILE_USERS = "data/users.csv"
FILE_RIWAYAT = "data/properti_dimiliki.csv"
FILE_BIODATA = "data/biodata.csv"

def properti_saya(username):
    if not os.path.exists(FILE_RIWAYAT):
        print("\nBelum ada riwayat pembelian.")
        input("Tekan ENTER untuk kembali...")
        return

    hasil = []

    with open(FILE_RIWAYAT, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                hasil.append(row)

    if not hasil:
        print("\nAnda belum membeli properti apa pun.")
        input("Tekan ENTER untuk kembali...")
        return

    print(f"\n=== PROPERTI YANG SUDAH ANDA BELI ===")

    for i, p in enumerate(hasil, start=1):
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
        pilihan = input("\n>> Pilih opsi: ")
        
        if pilihan == '1':
            jual_kembali_properti(username)
            return
        elif pilihan == '0':
            return
        else:
            print("Pilihan tidak valid!")
            continue

def informasi_pribadi(username):

    with open(FILE_BIODATA, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print()
            print("=" * 40)
            print("        INFORMASI PRIBADI USER")
            print("=" * 40)
            print(f"NIK               : {row['nik']}")
            print(f"Nama              : {row['nama_lengkap']}")
            print(f"Jenis Kelamin     : {row['jenis_kelamin']}")
            print(f"Alamat            : {row['alamat']}")
            print(f"Agama             : {row['agama']}")
            print(f"Status Perkawinan : {row['status_kawin']}")
            print(f"Pekerjaan         : {row['pekerjaan']}")
            print(f"Kewarganegaraan   : {row['kewarganegaraan']}")
            print("-" * 40)
            print(f"Username          : {row['username']}")
            print(f"Email             : {row['email']}")
            print(f"No. Telepon       : {row['no_telepon']}")
            print(f"Role              : {row['role']}")
            print(f"User Verified     : {row['user_verified']}")
            print("=" * 40)
            print()
            input("Tekan ENTER untuk kembali...")

def profile(username):
    
    while True:
        user_data = None
        if os.path.exists(FILE_USERS):
            with open(FILE_USERS, mode='r') as file:
                reader = csv.DictReader(file)
                for user in reader:
                    if user['username'] == username:
                        user_data = user
                        break
        
        if not user_data:
            print("Data pengguna error.")
            return

        print("\n========================================")
        print("              PROFIL SAYA               ")
        print("========================================")
        print(f"👤 Nama    : {user_data['username']}")

        print(f"🛡️  Role    : {user_data['role'].capitalize()}")
        status_verif = "✅  Terverifikasi" if user_data.get('user_verified') == 'true' else "⚠️  Belum Verifikasi"
        print(f"Status     : {status_verif}")
        print("----------------------------------------")
        print(" [I] Informasi Pribadi")
        print(" [H] History Transaksi")
        print(" [K] Keamanan dan Password")
        print(" [P] Properti Saya (Dimiliki)")
        if user_data['role'] == "user":
            print(" [M] Daftar Sebagai Seller")
        # if user_data['role']
        if user_data['user_verified'] == "false":
            print(" [V] Ajukan Verifikasi User")
        print(" [B] Kembali")

        if user_data['role'] == "user" and user_data['user_verified'] == "false":
            pilihan = input("Pilih menu (I/H/K/P/M/V/B): ").lower()
        elif user_data['role'] == "user":
            pilihan = input("Pilih menu (I/H/K/P/M/B): ").lower()
        else:
            pilihan = input("Pilih menu (I/H/K/P/B): ").lower()

        if pilihan  == "i":
            informasi_pribadi(username)
            continue
        elif pilihan == "h":
            history_transaksi(username)
            continue
        elif pilihan == "k":
            while True:
                print("\n===== Keamanan & Password =====")
                print("1. Ganti Password")
                print("2. Login Biometrik")
                print("0. Kembali")

                while True:
                    pilih = input("\nPilih menu: ")

                    if pilih == "1":
                        P = ganti_password()
                        if P == "EXIT":
                            print("Mengembalikan user ke halaman awal...")
                            time.sleep(2)
                            return "EXIT"
                        else:
                            break
                    elif pilih == "2":
                        toggle_biometrik(username)
                        time.sleep(2)
                        break
                    elif pilih == "0":
                        break
                    else:
                        print("Pilihan tidak valid!")
                        continue
                if pilih == "0":
                    break
        elif pilihan == "p":
            properti_saya(username)
            continue
        elif pilihan == 'm':
            if user_data['role'] == "user":
                if user_data['user_verified'] == "true":
                    seller_registration_menu(username)
                else:
                    print("Akun anda belum terverifikasi!")
                    input("Tekan ENTER untuk kembali...")
            else:
                print("Pilihan tidak valid!")
            continue
        elif pilihan == "v":
            if user_data['user_verified'] == "false":
                print("Coming Soon: Fitur Ajukan Verifikasi User")
                time.sleep(2)
            else:
                print("Pilihan tidak valid!")
            continue
        elif pilihan == "b":
            break
        else:
            print("Pilihan tidak valid!")