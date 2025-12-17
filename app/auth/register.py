import csv
import os

FILE_USERS = "data/users.csv"

def register():
    print("--- Register GeoEstate ---")
    username = input("Masukkan Username: ")

    # Pastikan file CSV ada
    if not os.path.exists(FILE_USERS):
        with open(FILE_USERS, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password", "role", "verified"])

    # Cek username sudah ada atau belum
    with open(FILE_USERS, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user["username"] == username:
                print("Username sudah dipakai, silakan coba lagi.\n")
                return False

    password = input("Masukkan Password: ")

    print("Pilih peran Anda:")
    print("1. Pembeli")
    print("2. Penjual")
    role_choice = input("Masukkan pilihan (1/2): ")

    if role_choice == "1":
        role = "pembeli"
    elif role_choice == "2":
        role = "penjual"
    else:
        print("Pilihan tidak valid.\n")
        return False

    # Simpan ke CSV
    with open(FILE_USERS, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, role, False])

    print(f"Register berhasil sebagai {role}!\n")
    return True
