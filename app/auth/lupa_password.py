import time
import csv
import random

FILE_USERS = "data/users.csv"
reset_sessions = {}  
# format:
# {
#   "username": {
#       "pin": "123456",
#       "expires_at": 1700000000
#   }
# }

def generate_otp():
    return ''.join(random.choices("0123456789", k=6))

def validate_user(username, email):
    with open(FILE_USERS, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for user in reader:
            if user['username'] == username and user['email'] == email:
                return user
    return None

def lupa_password():
    print("\n===== RESET PASSWORD =====")

    # tahap 1: identitas
    while True:
        username = input("Username (ENTER untuk batal): ").strip()
        if not username:
            print("Proses dibatalkan.")
            input("Tekan ENTER untuk kembali...")
            return

        email = input("Email: ").strip()
        if not email:
            print("Email tidak boleh kosong!\n")
            continue

        user = validate_user(username, email)
        if not user:
            print("Username atau email tidak cocok!\n")
            continue
        break

    # tahap 2: buat Kode OTP session
    otp = generate_otp()
    duration = 180  # 3 menit
    reset_sessions[username] = {
        "otp": otp,
        "expires_at": time.time() + duration
    }

    print("\nKode OTP reset password kamu:", otp)
    print(f"Kode OTP berlaku selama {duration} detik")
    print("Ketika program dihentikan, Kode OTP akan otomatis dihapus.\n")

    # tahap 3: verifikasi Kode OTP
    kesempatan = 3

    while True:
        remaining = int(reset_sessions[username]["expires_at"] - time.time())

        if remaining <= 0:
            print("\nWaktu Kode OTP telah habis.")
            print("Silakan ulangi proses lupa password.")
            reset_sessions.pop(username, None)
            input("Tekan ENTER untuk kembali...")
            return

        if kesempatan == 0:
            print("Kesempatan habis.")
            print("Silakan ulangi proses lupa password.")
            reset_sessions.pop(username, None)
            input("Tekan ENTER untuk kembali...")
            return
        
        input_otp = input(f"Masukkan Kode OTP (sisa {remaining} detik, ENTER untuk batal): ").strip()

        if not input_otp:
            print("Proses dibatalkan.")
            reset_sessions.pop(username, None)
            input("Tekan ENTER untuk kembali...")
            return

        session = reset_sessions.get(username)
        if not session or time.time() > session['expires_at']:
            print("Kode OTP sudah tidak berlaku.")
            reset_sessions.pop(username, None)
            input("Tekan ENTER untuk kembali...")
            return
        
        if input_otp != session['otp']:
            kesempatan -= 1
            print("Kode OTP salah!")
            print(f"Sisa waktu: {remaining} detik")
            print(f"Kesempatam tersisa: {kesempatan}\n")
            continue

        # tahap 4: password baru
        old_password = user['password']
        print("\n===== BUAT PASSWORD BARU =====")
        while True:
            new_pass = input("Password baru (ENTER untuk batal): ").strip()
            if not new_pass:
                print("Proses dibatalkan.")
                reset_sessions.pop(username, None)
                input("Tekan ENTER untuk kembali...")
                return
            
            if new_pass == old_password:
                print("Password baru harus berbeda dari password lama\n")
                continue

            confirm = input("Konfirmasi password (ENTER untuk batal): ").strip()

            if not confirm:
                return

            if new_pass != confirm:
                print("Password tidak cocok!\n")
                continue
            break

        # update password
        users = []
        with open(FILE_USERS, newline='', encoding='utf-8') as f:
            users = list(csv.DictReader(f))

        for u in users:
            if u['username'] == username:
                u['password'] = new_pass  # atau hash
                break

        with open(FILE_USERS, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['username', 'email', 'password', 'role', 'user_verified']
            )
            writer.writeheader()
            writer.writerows(users)

        reset_sessions.pop(username, None)
        print("\nPassword berhasil direset!")
        input("Tekan ENTER untuk kembali...")
        return

def ganti_password():
    print("\n===== RESET PASSWORD =====")

    # tahap 1: identitas
    while True:
        username = input("Username (ENTER untuk batal): ").strip()
        if not username:
            print("Proses dibatalkan.")
            input("Tekan ENTER untuk kembali...")
            return

        email = input("Email: ").strip()
        if not email:
            print("Email tidak boleh kosong!\n")
            continue

        user = validate_user(username, email)
        if not user:
            print("Username atau email tidak cocok!\n")
            continue
        break

    # tahap 2: buat Kode OTP session
    otp = generate_otp()
    duration = 180  # 3 menit
    reset_sessions[username] = {
        "otp": otp,
        "expires_at": time.time() + duration
    }

    print("\nKode OTP reset password kamu:", otp)
    print(f"Kode OTP berlaku selama {duration} detik")
    print("Ketika program dihentikan, Kode OTP akan otomatis dihapus.\n")

    # tahap 3: verifikasi Kode OTP
    kesempatan = 3

    while True:
        remaining = int(reset_sessions[username]["expires_at"] - time.time())

        if remaining <= 0:
            print("\nWaktu Kode OTP telah habis.")
            print("Silakan ulangi proses lupa password.")
            reset_sessions.pop(username, None)
            input("Tekan ENTER untuk kembali...")
            return

        if kesempatan == 0:
            print("Kesempatan habis.")
            print("Silakan ulangi proses lupa password.")
            reset_sessions.pop(username, None)
            input("Tekan ENTER untuk kembali...")
            return
        
        input_otp = input(f"Masukkan Kode OTP (sisa {remaining} detik, ENTER untuk batal): ").strip()

        if not input_otp:
            print("Proses dibatalkan.")
            reset_sessions.pop(username, None)
            input("Tekan ENTER untuk kembali...")
            return

        session = reset_sessions.get(username)
        if not session or time.time() > session['expires_at']:
            print("Kode OTP sudah tidak berlaku.")
            reset_sessions.pop(username, None)
            input("Tekan ENTER untuk kembali...")
            return
        
        if input_otp != session['otp']:
            kesempatan -= 1
            print("Kode OTP salah!")
            print(f"Sisa waktu: {remaining} detik")
            print(f"Kesempatam tersisa: {kesempatan}\n")
            continue

        # tahap 4: password baru
        old_password = user['password']
        print("\n===== BUAT PASSWORD BARU =====")
        while True:
            new_pass = input("Password baru (ENTER untuk batal): ").strip()
            if not new_pass:
                print("Proses dibatalkan.")
                reset_sessions.pop(username, None)
                input("Tekan ENTER untuk kembali...")
                return
            
            if not (8 <= len(new_pass) <= 32):
                print("Password harus terdiri dari 8 hingga 32 karakter!\n")
                continue

            if not any(c.isalpha() for c in new_pass) or not any(c.isdigit() for c in new_pass):
                print("Password harus mengandung huruf dan angka!\n")
                continue

            if new_pass == old_password:
                print("Password baru harus berbeda dari password lama\n")
                continue

            confirm = input("Konfirmasi password (ENTER untuk batal): ").strip()

            if not confirm:
                return

            if new_pass != confirm:
                print("Password tidak cocok!\n")
                continue
            break

        # update password
        users = []
        with open(FILE_USERS, newline='', encoding='utf-8') as f:
            users = list(csv.DictReader(f))

        for u in users:
            if u['username'] == username:
                u['password'] = new_pass  # atau hash
                break

        with open(FILE_USERS, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['username', 'email', 'password', 'role', 'user_verified']
            )
            writer.writeheader()
            writer.writerows(users)

        reset_sessions.pop(username, None)
        print("\nPassword berhasil direset!")
        print("Mengembalikan user ke halaman awal...")
        time.sleep(2)
        return "EXIT"