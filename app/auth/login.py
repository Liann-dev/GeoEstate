import csv
import os

FILE_USERS = "data/users.csv"

#login
def login():
    kesempatan = 3

    if not os.path.exists(FILE_USERS):
        print("Belum ada user terdaftar.\n")
        return None

    while kesempatan > 0:
        print("--- Login GeoEstate ---")
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")

        with open(FILE_USERS, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user["username"] == username and user["password"] == password:
                    print(f"Login berhasil sebagai {user['role']}!\n")
                    return user   # ← penting, return dict

        kesempatan -= 1
        print(f"Username atau Password salah. Kesempatan tersisa: {kesempatan}\n")

    print("Login gagal. Silakan coba lagi nanti.\n")
    return None 
    print("Login gagal.\n")
    return None
