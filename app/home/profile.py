
import csv
import os

FILE_USERS = "data/users.csv"

def profile(username):
    if not os.path.exists(FILE_USERS):
        print("Data pengguna tidak ditemukan.")
        return

    with open(FILE_USERS, mode='r', newline='') as file:
        reader = csv.DictReader(file)

        for user in reader:
            if user['username'] == username:
                print("\n=== PROFIL PENGGUNA ===")
                print(f"Username  : {user['username']}")
                print(f"Role      : {user['role'].capitalize()}")

                status = "Terverifikasi" if user['user_verified'].lower() == "true" else "Belum Terverifikasi"
                print(f"Status    : {status}\n")
                return

    print("Profil pengguna tidak ditemukan.\n")
