import csv
import os
import random

WITHDRAW_FILE = "data/merchdraw.csv"
USERS_FILE = "data/users.csv"

def get_user_by_username(username):
    with open(USERS_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user["username"] == username:
                return user
    return None

def init_withdraw_file():
    if not os.path.exists(WITHDRAW_FILE):
        with open(WITHDRAW_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["wd_id", "username", "email", "reason", "status"])

def generate_wd_id(existing_ids):
    while True:
        wd_id = f"WD-{random.randint(1000, 9999)}"
        if wd_id not in existing_ids:
            return wd_id

def merchant_withdraw_menu(current_user):
    init_withdraw_file()
    
    user_data = get_user_by_username(current_user)
    if not user_data:
        print("Data user tidak ditemukan.\n")
        return

    print("\n=== Pengunduran Diri Merchant ===")

    # === EMAIL ===
    while True:
        email = input("Masukkan Email (Tekan ENTER untuk membatalkan): ").strip()
        if not email:
            return
        if email != user_data["email"]:
            print("Email tidak sesuai dengan akun yang sedang login.\n")
            continue
        break

    # === PASSWORD ===
    while True:
        password = input("Masukkan Password (Tekan ENTER untuk membatalkan): ").strip()
        if not password:
            return
        if password != user_data["password"]:
            print("Password salah.\n")
            continue
        break
    
    # === KONFIRMASI PASSWORD ===
    while True:
        confirm_password = input("Konfirmasi Password (Tekan ENTER untuk membatalkan): ").strip()
        if not confirm_password:
            return

        if confirm_password != password:
            print("Konfirmasi password tidak sesuai.\n")
            continue
        break

    # === ALASAN ===
    while True:
        reason = input("Alasan pengunduran diri (Tekan ENTER untuk membatalkan): ").strip()
        if not reason:
            return
        break

    # === CEK SUDAH PERNAH AJUKAN ===
    existing_ids = []
    with open(WITHDRAW_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_ids.append(row["wd_id"])
            if row["username"] == current_user and row["status"] == "pending":
                print("Anda sudah mengajukan pengunduran diri.\n")
                input("Tekan ENTER untuk kembali...")
                return

    wd_id = generate_wd_id(existing_ids)

    with open(WITHDRAW_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([wd_id, current_user, email, password, reason, "pending"])

    print("\nPengajuan pengunduran diri berhasil.")
    print(f"ID Pengajuan: {wd_id}")
    print("Menunggu persetujuan admin.\n")
    input("Tekan ENTER untuk kembali...")