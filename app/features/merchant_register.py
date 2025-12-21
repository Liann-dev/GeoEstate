import csv
import os
import random

MERCHANT_REG_FILE = "data/merchreg.csv"
USERS_FILE = "data/users.csv"

def get_user_by_username(username):
    with open(USERS_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user["username"] == username:
                return user
    return None

def init_merchreg_file():
    if not os.path.exists(MERCHANT_REG_FILE):
        with open(MERCHANT_REG_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["reg_id", "username", "email", "reason", "status"])


def generate_reg_id(existing_ids):
    while True:
        reg_id = f"REG-{random.randint(1000, 9999)}"
        if reg_id not in existing_ids:
            return reg_id

def merchant_registration_menu(current_user):
    init_merchreg_file()

    user_data = get_user_by_username(current_user)
    if not user_data:
        print("Data user tidak ditemukan.\n")
        return

    print("\n=== Pendaftaran Merchant ===")

    # === EMAIL ===
    while True:
        email = input("Masukkan Email: ").strip()
        if not email:
            print("Email tidak boleh kosong\n")
            continue
        if email != user_data["email"]:
            print("Email tidak sesuai dengan akun yang sedang login.\n")
            continue
        break

    # === PASSWORD ===
    while True:
        password = input("Masukkan Password: ").strip()
        if not password:
            print("Password tidak boleh kosong\n")
            continue
        if password != user_data["password"]:
            print("Password salah.\n")
            continue
        break

    # === KONFIRMASI PASSWORD ===
    while True:
        confirm_password = input("Konfirmasi Password: ").strip()
        if confirm_password != password:
            print("Konfirmasi password tidak sesuai.\n")
            continue
        break

    # === ALASAN ===
    while True:
        reason = input("Alasan mendaftar sebagai merchant: ").strip()
        if not reason:
            print("Alasan pendaftaran tidak boleh kosong\n")
            continue
        break

    # === CEK SUDAH DAFTAR ===
    existing_ids = []
    with open(MERCHANT_REG_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_ids.append(row["reg_id"])
            if row["username"] == current_user:
                print("Anda sudah mengajukan pendaftaran merchant.\n")
                input("Tekan ENTER untuk kembali...")
                return

    reg_id = generate_reg_id(existing_ids)

    with open(MERCHANT_REG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([reg_id, current_user, email, password, reason, "pending"])

    print("\nPendaftaran merchant berhasil.")
    print(f"ID Pendaftaran Anda: {reg_id}")
    print("Menunggu verifikasi admin.\n")
    input("Tekan ENTER untuk kembali...")