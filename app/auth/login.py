import csv
import os

FILE_USERS = "data/users.csv"

def login():
    kesempatan = 3

    if not os.path.exists(FILE_USERS):
        print("Belum ada user terdaftar.\n")
        return None

    while kesempatan > 0:
        print(f"\n--- Login GeoEstate ---")

        login_input = input("Masukkan Username atau Email: ").strip()
        password = input("Masukkan Password: ").strip()

        if not login_input:
            print("Username atau Email tidak boleh kosong!\n")
            continue

        if not password:
            print("Password tidak boleh kosong!\n")
            continue

        user_found = None

        with open(FILE_USERS, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user["username"] == login_input or user["email"] == login_input:
                    user_found = user
                    break

        if not user_found:
            kesempatan -= 1
            print(f"Username atau Email salah. Kesempatan tersisa: {kesempatan}\n")
            continue

        if user_found["password"] != password:
            kesempatan -= 1
            print(f"Password salah. Kesempatan tersisa: {kesempatan}\n")
            continue

        # Login berhasil
        print(f"Login berhasil sebagai {user_found['role']}!\n")
        return user_found

    print("Login gagal. Silakan coba lagi nanti.")
    input("Tekan ENTER untuk kembali ke halaman awal...")
    return None