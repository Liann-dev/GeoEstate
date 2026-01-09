import csv
import os
from app.features.notifikasi_service import tambah_notifikasi

USERS_FILE = "data/users.csv"
SELLER_FILE = "data/sellreg.csv"

def read_csv(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, mode="r", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(file_path, fieldnames, data):
    clean_data = []

    for row in data:
        clean_row = {key: row.get(key, "") for key in fieldnames}
        clean_data.append(clean_row)

    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_data)

def tampilkan_daftar_seller():
    users = read_csv(USERS_FILE)

    seller = [u for u in users if u.get("role") == "seller"]

    if not seller:
        print("Belum ada user dengan role seller.\n")
        input("Tekan ENTER untuk kembali...\n")
        return

    print("\n=== Daftar User Seller ===")
    print("-" * 70)
    print(f"{'No':<5}{'Username':<20}{'Email':<30}{'Verified User'}")
    print("-" * 70)

    for i, user in enumerate(seller, start=1):
        print(
            f"{i:<5}"
            f"{user.get('username', ''):<20}"
            f"{user.get('email', ''):<30}"
            f"{user.get('user_verified', '')}"
        )

    print("-" * 70)
    input("Tekan ENTER untuk kembali...\n")

def tampilkan_sellreg(data):
    if not data:
        print("Belum ada pendaftaran seller.\n")
        return

    print("\n=== Daftar Pendaftaran Seller ===")
    print("-" * 90)
    print(f"{'REG ID':<12}{'Username':<15}{'Email':<30}{'Status':<10}")
    print("-" * 90)

    for row in data:
        print(f"{row['reg_id']:<12}{row['username']:<15}{row['email']:<30}{row['status']:<10}")

    print("-" * 90)

def update_user_role(username, new_role):
    users = read_csv(USERS_FILE)

    for user in users:
        if user["username"] == username:
            user["role"] = new_role

    write_csv(
        USERS_FILE,
        ["username", "email", "password", "role", "user_verified", "suspend"],
        users
    )

def verifikasi_seller():
    data = read_csv(SELLER_FILE)

    # ===============================
    # FILTER HANYA YANG PENDING
    # ===============================
    pending_data = [row for row in data if row.get("status") == "pending"]

    if not pending_data:
        print("Tidak ada pendaftaran seller yang menunggu verifikasi.\n")
        input("Tekan ENTER untuk kembali...\n")
        return

    tampilkan_sellreg(pending_data)

    reg_id = input("Masukkan REG ID (Tekan ENTER untuk kembali): ").strip()
    if not reg_id:
        return

    for row in data:  # tetap pakai data asli untuk update
        if row["reg_id"] == reg_id:
            if row["status"] != "pending":
                print("Registrasi ini sudah diproses.")
                input("Tekan ENTER untuk kembali...\n")
                return

            # ===============================
            # DETAIL REGISTRASI
            # ===============================
            print("\n=== Detail Pendaftaran Seller ===")
            print(f"REG ID   : {row['reg_id']}")
            print(f"Username : {row['username']}")
            print(f"Email    : {row['email']}")
            print(f"Alasan   : {row['reason']}")
            print(f"Status   : {row['status']}")
            print("-" * 40)

            keputusan = input("Setujui registrasi? (y/n): ").lower()

            if keputusan == "y":
                row["status"] = "approved"
                update_user_role(row["username"], "seller")

                tambah_notifikasi(
                    username=row["username"],
                    pesan="🎉 Pengajuan Anda sebagai SELLER telah DISETUJUI oleh Admin.",
                    role="user",
                    redirect="profile"
                )

                print("Seller diterima.\n")
                input("Tekan ENTER untuk kembali...\n")


            elif keputusan == "n":
                row["status"] = "rejected"

                tambah_notifikasi(
                    username=row["username"],
                    pesan="❌ Pengajuan Anda sebagai SELLER DITOLAK oleh Admin.",
                    role="user",
                    redirect="profile"
                )

                print("Seller ditolak.\n")
                input("Tekan ENTER untuk kembali...\n")


            else:
                print("Pilihan tidak valid.")
                input("Tekan ENTER untuk kembali...\n")
                return

            write_csv(
                SELLER_FILE,
                ["reg_id", "username", "email", "reason", "status"],
                data
            )
            return

    print("REG ID tidak ditemukan.")
    input("Tekan ENTER untuk kembali...\n")

def menu_kelola_seller():
    while True:
        print("""
=== Menu Pengelolaan Seller ===
1. Lihat Daftar Seller
2. Verifikasi Pendaftaran Seller
0. Kembali           
""")

        pilihan = input("Pilih menu (0-2): ").strip()

        if pilihan == "1":
            tampilkan_daftar_seller()
        elif pilihan == "2":
            verifikasi_seller()
        elif pilihan == "0":
            return
        else:
            print("Pilihan tidak valid.\n")