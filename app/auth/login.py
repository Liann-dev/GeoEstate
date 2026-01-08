import csv
import os
import pwinput  # Import library pwinput

FILE_USERS = "data/users.csv"

def login():
    kesempatan = 3

    if not os.path.exists(FILE_USERS):
        print("Belum ada user terdaftar.\n")
        return None

    while kesempatan > 0:
        print(f"\n--- Login GeoEstate ---")

        login_input = input("Masukkan Username atau Email (ENTER untuk batal): ").strip()

        if not login_input:
            return
        
        # MENGGUNAKAN PWINPUT UNTUK PASSWORD
        password = pwinput.pwinput(prompt="Masukkan Password: ", mask="*").strip()

        # Validasi jika input kosong agar tidak langsung mengurangi kesempatan
        if login_input == "" or password == "":
            print("Username/Email dan Password tidak boleh kosong!")
            continue

        user_found = None
        with open(FILE_USERS, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user["username"] == login_input or user["email"] == login_input:
                    user_found = user
                    break

        # Cek jika username tidak ditemukan
        if not user_found or user_found['role'] == "admin":
            kesempatan -= 1
            print(f"Username atau Email salah. Kesempatan tersisa: {kesempatan}\n")
            if kesempatan == 0: break
            continue

        # Cek jika password salah
        if user_found["password"] != password:
            kesempatan -= 1
            print(f"Password salah. Kesempatan tersisa: {kesempatan}\n")
            if kesempatan == 0: 
                print("Login gagal. Jatah percobaan Anda telah habis.")
                break
            continue
        
        # Cek jika user di-suspend
        if user_found['suspend'] == 'true':
            print("❌ Akun Anda disuspend. Silakan hubungi admin.")
            break
        
        # Login berhasil
        print(f"\nLogin berhasil. Selamat datang {user_found['username']}!")
        return user_found

    # Hanya bisa sampai ke sini jika kesempatan sudah 0 (sudah mengisi tapi salah)
    input("Tekan ENTER untuk kembali ke halaman awal...")
    return None

def login_admin():
    kesempatan = 3

    if not os.path.exists(FILE_USERS):
        print("Belum ada admin terdaftar.\n")
        return None

    while kesempatan > 0:
        print(f"\n--- Login Admin GeoEstate ---")

        login_input = input("Masukkan Username atau Email: ").strip()
        
        # MENGGUNAKAN PWINPUT UNTUK PASSWORD ADMIN
        password = pwinput.pwinput(prompt="Masukkan Password: ", mask="*").strip()

        # Validasi jika input kosong agar tidak langsung mengurangi kesempatan
        if login_input == "" or password == "":
            print("Username/Email dan Password tidak boleh kosong!")
            continue

        user_found = None
        with open(FILE_USERS, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user["username"] == login_input or user["email"] == login_input:
                    user_found = user
                    break

        # Cek jika username tidak ditemukan
        if not user_found:
            kesempatan -= 1
            print(f"Username atau Email salah. Kesempatan tersisa: {kesempatan}\n")
            if kesempatan == 0: break
            continue

        # Cek jika password salah
        if user_found["password"] != password:
            kesempatan -= 1
            print(f"Password salah. Kesempatan tersisa: {kesempatan}\n")
            if kesempatan == 0: break
            continue
        
        # Login selesai
        return user_found

    # Hanya bisa sampai ke sini jika kesempatan sudah 0 (sudah mengisi tapi salah)
    print("Login gagal. Jatah percobaan Anda telah habis.")
    input("Tekan ENTER untuk kembali ke halaman awal...")
    return None