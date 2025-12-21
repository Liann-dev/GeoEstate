import csv
import os
import re

FILE_USERS = "data/users.csv"

def register():
    print(f"\n--- Register GeoEstate ---")

    # Pastikan file CSV ada
    if not os.path.exists(FILE_USERS):
        with open(FILE_USERS, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "email", "password", "role", "verified"])

    # Input username
    while True:
        username = input("Masukkan Username: ").strip()

        if not username:
            print("Username tidak boleh kosong!\n")
            continue

        username_dipakai = False

        with open(FILE_USERS, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user["username"] == username:
                    print("Username sudah dipakai, silakan coba lagi.\n")
                    username_dipakai = True
                    break

        if username_dipakai:
            continue

        break

    # Input email
    while True:
        email = input("Masukkan Email: ").strip()

        if not email:
            print("Email tidak boleh kosong!\n")
            continue

        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$'

        if not re.match(pattern, email):
            print("Email tidak valid!")
            continue

        email_dipakai = False

        with open(FILE_USERS, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user["email"] == email:
                    print("Email sudah dipakai, silakan coba lagi.\n")
                    email_dipakai = True
                    break

        if email_dipakai:
            continue

        break

    # Input password
    while True:
        password = input("Masukkan Password: ")

        if not password:
            print("Password tidak boleh kosong!\n")
            continue

        if not (8 <= len(password) <= 32):
            print("Password harus terdiri dari 8 hingga 32 karakter!\n")
            continue

        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            print("Password harus mengandung huruf dan angka!\n")
            continue

        break


    while True:
        sisa = 3
        konfirmasi_password = input("Konfirmasi Password: ")
        if konfirmasi_password == password:
            break
        if not konfirmasi_password:
            print("Konfirmasi password tidak boleh kosong!\n")
            continue
        if konfirmasi_password != password:
            print(f"Password tidak sama! Kesempatan tersisa: {sisa - 1}\n")
        if sisa == 0:
            print("Konfirmasi password gagal. Registrasi dibatalkan.")
            input("Tekan ENTER untuk kembali ke halaman awal...")
            return False

    role = "user"

    # Simpan ke CSV
    with open(FILE_USERS, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, email, password, role, False])

    print(f"Register berhasil!")
    input("Tekan ENTER untuk kembali ke halaman awal...")
    return True