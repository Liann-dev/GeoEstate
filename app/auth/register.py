import csv
import os
import re
import random

FILE_USERS = "data/users.csv"

def register():
    print(f"\n--- Register GeoEstate ---")

    if not os.path.exists(FILE_USERS):
        with open(FILE_USERS, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "email", "password", "role", "user_verified", "suspend"])

    print("""Syarat Username :
1) Terdiri dari 1-32 karakter
2) Hanya terdiri dari angka, huruf, titik(.), dan underscore(_)
3) Tidak boleh sama dengan username yang sudah ada""")

    while True:
        username = input("Masukkan Username (ENTER untuk batal): ").strip()
        if username == "":
            return False

        if not (1 <= len(username) <= 32):
            print("❌ Username harus 1–32 karakter.\n")
            continue

        if not re.fullmatch(r"[A-Za-z0-9._]+", username):
            print("❌ Username hanya boleh berisi huruf, angka, titik (.), dan underscore (_).\n")
            continue

        with open(FILE_USERS, newline='') as f:
            for u in csv.DictReader(f):
                if u["username"] == username:
                    print("❌ Username sudah dipakai.\n")
                    break
            else:
                break

    print("""\nSyarat Email :
1) Maksimal 32 karakter
2) Format valid
3) Tidak boleh sama dengan email yang sudah ada""")

    while True:
        email = input("Masukkan Email (ENTER untuk batal): ").strip().lower()
        if email == "":
            return False

        if len(email) > 32:
            print("❌ Email maksimal 32 karakter.\n")
            continue

        if not re.match(r'^[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{1,}$', email):
            print("❌ Email tidak valid.\n")
            continue

        with open(FILE_USERS, newline='') as f:
            for u in csv.DictReader(f):
                if u["email"] == email:
                    print("❌ Email sudah dipakai.\n")
                    break
            else:
                break

    print("""\nSyarat Password :
1) 8–32 karakter
2) Mengandung huruf & angka
3) Boleh simbol
4) Tidak boleh ada spasi""")

    while True:
        password = input("Masukkan Password (ENTER untuk batal): ")
        if password == "":
            return False

        if not (8 <= len(password) <= 32):
            print("❌ Password harus 8–32 karakter.\n")
            continue

        if " " in password:
            print("❌ Password tidak boleh mengandung spasi.\n")
            continue

        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            print("❌ Password harus mengandung huruf dan angka.\n")
            continue
        break

    sisa = 3
    while True:
        confirm = input("Konfirmasi Password (ENTER untuk batal): ")
        if confirm == "":
            return False

        if confirm == password:
            break

        sisa -= 1
        if sisa == 0:
            print("\nKonfirmasi gagal. Registrasi dibatalkan.")
            input("Tekan ENTER untuk kembali...")
            return False

        print(f"❌ Password tidak sama. Sisa: {sisa}\n")

    otp = str(random.randint(1000, 9999))

    print("\n========================================")
    print("Verifikasi OTP")
    print(f"Kode OTP Anda: {otp}")
    print("========================================\n")

    chance = 3
    while chance > 0:
        inp = input("Masukkan 4 digit OTP: ").strip()

        if len(inp) != 4 or not inp.isdigit():
            print("❌ OTP harus 4 digit angka.\n")
            continue

        if inp == otp:
            with open(FILE_USERS, 'a', newline='') as f:
                csv.writer(f).writerow([username, email, password, "user", "false", "false"])
            print("\n✅ Registrasi berhasil!")
            input("Tekan ENTER untuk kembali...")
            return True

        chance -= 1
        print(f"❌ OTP salah. Sisa: {chance}\n")

    print("❌ Verifikasi OTP gagal.")
    input("Tekan ENTER untuk kembali...")
    return False
