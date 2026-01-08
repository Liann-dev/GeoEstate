import time
import csv
import random

FILE_USERS = "data/users.csv"
reset_sessions = {}

# =========================
# UTIL
# =========================
def generate_pin():
    return ''.join(random.choices("0123456789", k=6))

def validate_user(username, email):
    with open(FILE_USERS, newline='', encoding='utf-8') as f:
        for u in csv.DictReader(f):
            if u['username'] == username and u['email'] == email:
                return u
    return None

def valid_password(pw):
    if not (8 <= len(pw) <= 32):
        return False, "Password harus 8–32 karakter."
    if " " in pw:
        return False, "Password tidak boleh mengandung spasi."
    if not any(c.isalpha() for c in pw) or not any(c.isdigit() for c in pw):
        return False, "Password harus mengandung huruf dan angka."
    return True, ""

# =========================
# LUPA PASSWORD (DARI LOGIN)
# =========================
def lupa_password():
    print("\n===== RESET PASSWORD =====\n")

    while True:
        username = input("Username (ENTER untuk batal): ").strip()
        if not username:
            return

        email = input("Email: ").strip()
        user = validate_user(username, email)
        if not user:
            print("❌ Username dan email tidak cocok!\n")
            continue
        break

    pin = generate_pin()
    reset_sessions[username] = {
        "pin": pin,
        "expires_at": time.time() + 180
    }

    print("\nKode OTP reset password:", pin)
    print("Berlaku selama 3 menit\n")

    kesempatan = 3
    while kesempatan > 0:
        sisa = int(reset_sessions[username]["expires_at"] - time.time())
        if sisa <= 0:
            print("❌ OTP kadaluarsa.")
            reset_sessions.pop(username, None)
            return

        inp = input(f"Masukkan OTP (sisa {sisa} detik): ").strip()
        if inp != pin:
            kesempatan -= 1
            print(f"❌ OTP salah. Sisa kesempatan: {kesempatan}\n")
            continue
        break
    else:
        reset_sessions.pop(username, None)
        return

    old_password = user['password']

    while True:
        new_pass = input("Password baru (ENTER untuk batal): ").strip()
        if not new_pass:
            reset_sessions.pop(username, None)
            return

        ok, msg = valid_password(new_pass)
        if not ok:
            print("❌", msg, "\n")
            continue

        if new_pass == old_password:
            print("❌ Password baru harus berbeda dari password lama.\n")
            continue

        confirm = input("Konfirmasi password: ").strip()
        if new_pass != confirm:
            print("❌ Password tidak cocok.\n")
            continue
        break

    with open(FILE_USERS, newline='', encoding='utf-8') as f:
        users = list(csv.DictReader(f))

    for u in users:
        if u['username'] == username:
            u['password'] = new_pass

    with open(FILE_USERS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

    reset_sessions.pop(username, None)
    print("\n✅ Password berhasil direset!")
    input("Tekan ENTER untuk kembali...")

# =========================
# GANTI PASSWORD (DARI PROFILE)
# =========================
def ganti_password():
    print("\n===== GANTI PASSWORD =====\n")

    while True:
        username = input("Username (ENTER untuk batal): ").strip()
        if not username:
            return "EXIT"

        email = input("Email: ").strip()
        user = validate_user(username, email)
        if not user:
            print("❌ Username dan email tidak cocok!\n")
            continue
        break

    pin = generate_pin()
    reset_sessions[username] = {
        "pin": pin,
        "expires_at": time.time() + 180
    }

    print("\nKode OTP ganti password:", pin)
    print("Berlaku selama 3 menit\n")

    kesempatan = 3
    while kesempatan > 0:
        sisa = int(reset_sessions[username]["expires_at"] - time.time())
        if sisa <= 0:
            print("❌ OTP kadaluarsa.")
            reset_sessions.pop(username, None)
            return "EXIT"

        inp = input(f"Masukkan OTP (sisa {sisa} detik): ").strip()
        if inp != pin:
            kesempatan -= 1
            print(f"❌ OTP salah. Sisa kesempatan: {kesempatan}\n")
            continue
        break
    else:
        reset_sessions.pop(username, None)
        return "EXIT"

    old_password = user['password']

    while True:
        new_pass = input("Password baru (ENTER untuk batal): ").strip()
        if not new_pass:
            reset_sessions.pop(username, None)
            return "EXIT"

        ok, msg = valid_password(new_pass)
        if not ok:
            print("❌", msg, "\n")
            continue

        if new_pass == old_password:
            print("❌ Password baru harus berbeda dari password lama.\n")
            continue

        confirm = input("Konfirmasi password: ").strip()
        if new_pass != confirm:
            print("❌ Password tidak cocok.\n")
            continue
        break

    with open(FILE_USERS, newline='', encoding='utf-8') as f:
        users = list(csv.DictReader(f))

    for u in users:
        if u['username'] == username:
            u['password'] = new_pass

    with open(FILE_USERS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

    reset_sessions.pop(username, None)
    print("\n✅ Password berhasil diganti!")
    input("Tekan ENTER untuk kembali...")
    return "EXIT"
