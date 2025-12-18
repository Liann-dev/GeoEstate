import csv
import os
from app.home.history_transaksi import history_transaksi

FILE_USERS = "data/users.csv"


def profile(username):
    

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
    status_verif = "✅ Terverifikasi" if user_data.get('user_verified') == 'true' else "⚠️ Belum Verifikasi"
    print(f"Status  : {status_verif}")
    print("----------------------------------------")
    print(" [I] Informasi Pribadi")
    print(" [H] History Transaksi")
    print(" [K] Keamanan dan Password")
    print(" [P] Properti Saya (Dimiliki)")

    pilihan = input("Pilih menu (I/H/K/P): ").lower()
    if pilihan  == "i":
        print("Coming Soon: Informasi Pribadi")
    elif pilihan == "h":
        history_transaksi(username)
    elif pilihan == "k":
        print("Coming Soon: Keamanan dan Password")
    elif pilihan == "p":
        # properti_saya(username)
        print("Coming Soon: Properti Saya")


    print("\n========================================")
    input("Tekan ENTER untuk kembali ke menu utama...")