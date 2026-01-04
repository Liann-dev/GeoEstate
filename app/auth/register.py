import csv
import os
import re
import random

FILE_USERS = "data/users.csv"

def register():
    print(f"\n--- Register GeoEstate ---")

    # Pastikan file CSV ada
    if not os.path.exists(FILE_USERS):
        with open(FILE_USERS, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "email", "password", "role", "user_verified"])

    # Input username
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

        username_dipakai = False
        with open(FILE_USERS, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user["username"] == username:
                    print("❌ Username sudah dipakai, silakan coba lagi.\n")
                    username_dipakai = True
                    break

        if username_dipakai:
            continue

        break

    # Input email
    print("""\nSyarat Email :
1) Maksimal terdiri dari 32 karakter
2) Format email yaitu 'karakter' + '@' + 'karakter' + '.' + 'karakter' + ...
   Contoh : user@domain.com | user@mail.co.id
3) Tidak boleh sama dengan email yang sudah ada""")
    
    while True:
        email = input("Masukkan Email (ENTER untuk batal): ").strip()
        if email == "":
            return False

        if not (len(username) <= 32):
            print("❌ Email maksmimal terdiri dari 32 karakter.\n")
            continue

        # Regex email optimal
        pattern = r'^[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{1,}$'
        if not re.match(pattern, email):
            print("Email tidak valid! Contoh email valid: user@domain.com, user@mail.co.id\n")
            continue

        # Cek email sudah dipakai
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
    print("""\nSyarat Password :
1) Terdiri dari 8-32 karakter
2) Terdiri dari huruf dan angka""")
    
    while True:
        password = input("Masukkan Password (ENTER untuk batal): ")
        if password == "":
            return False

        if not (8 <= len(password) <= 32):
            print("Password harus terdiri dari 8 hingga 32 karakter!\n")
            continue

        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            print("Password harus mengandung huruf dan angka!\n")
            continue

        break

    # Konfirmasi password
    sisa = 3
    while True:
        konfirmasi_password = input("Konfirmasi Password (ENTER untuk batal): ")
        if konfirmasi_password == "":
            return False

        if konfirmasi_password == password:
            break

        sisa -= 1
        if sisa == 0:
            print("\nKonfirmasi password gagal. Registrasi dibatalkan.")
            input("Tekan ENTER untuk kembali ke halaman awal...")
            return False

        print(f"Password tidak sama! Kesempatan tersisa: {sisa}\n")

    otp_code = str(random.randint(1000,9999))

    print("\n"+ "="*40)
    print("Verifikasi Kode OTP")
    print(f"\n Kode OTP telah dikirim ke email {email}")
    print(f" Kode OTP Anda adalah: {otp_code}")
    print("="*40+"\n")

    sisa_percobaan_otp = 3

    while sisa_percobaan_otp > 0:
        input_otp = input("Masukka 4 digit Kode OTP: ").strip()

        if input_otp == "":
            print("Input tidak boleh kosong! Silahkan masukkan Kode OTP.\n")
            continue

        if len(input_otp) != 4 or not input_otp.isdigit():
            print("Kode OTP harus terdiri dari 4 digit angka!\n")
            continue

        if input_otp == otp_code:
            role = "user"
            with open(FILE_USERS, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, email, password, role, "false"])
                
                print(f"\nRegister berhasil!")
                input("Tekan ENTER untuk kembali ke halaman awal...")
                return True
        else:
            sisa_percobaan_otp -= 1
            if sisa_percobaan_otp > 0:
                print(f"Kode OTP salah! Kesempatan tersisa: {sisa_percobaan_otp}\n")
            else:
                print("\nVerifikasi OTP gagal. Registrasi dibatalkan.")
                input("Tekan ENTER untuk kembali ke halaman awal...")
                return False



    # role = "user"

    # # Simpan ke CSV
    # with open(FILE_USERS, mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([username, email, password, role, "false"])

    # print(f"\nRegister berhasil!")
    # input("Tekan ENTER untuk kembali ke halaman awal...")
    # return True
