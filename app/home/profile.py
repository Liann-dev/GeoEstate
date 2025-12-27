import csv
import os
import time
from app.home.history_transaksi import history_transaksi
from app.home.jual_properti import jual_kembali_properti

FILE_USERS = "data/users.csv"
FILE_RIWAYAT = "data/properti_dimiliki.csv"

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
    print("1. 💲 Jual / Kembalikan Properti")
    print("0. 🔙 Kembali")
    
    pilihan = input("\n>> Pilih opsi: ")
    
    if pilihan == '1':
        jual_kembali_properti(username)
    elif pilihan == '2':
        input("Tekan ENTER untuk kembali...")
        return
    else:
        print("Pilihan tidak valid!")
        input("Tekan ENTER untuk kembali...")
        return

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
        print(" [B] Kembali")

        pilihan = input("Pilih menu (I/H/K/P/B): ").lower()
        if pilihan  == "i":
            print("Coming Soon: Informasi Pribadi")
            time.sleep(2)
            continue
        elif pilihan == "h":
            history_transaksi(username)
            continue
        elif pilihan == "k":
            print("Coming Soon: Keamanan dan Password")
            time.sleep(2)
            continue
        elif pilihan == "p":
            properti_saya(username)
            continue
        elif pilihan == "b":
            break