import csv
import os

USERS_FILE = "data/users.csv"
MERCH_FILE = "data/sellreg.csv"
WITHDRAW_FILE = "data/selldraw.csv"

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

    merchants = [u for u in users if u.get("role") == "merchant"]

    if not merchants:
        print("Belum ada user dengan role merchant.\n")
        return

    print("\n=== Daftar User Merchant ===")
    print("-" * 70)
    print(f"{'No':<5}{'Username':<20}{'Email':<30}{'Verified User'}")
    print("-" * 70)

    for i, user in enumerate(merchants, start=1):
        print(
            f"{i:<5}"
            f"{user.get('username', ''):<20}"
            f"{user.get('email', ''):<30}"
            f"{user.get('user_verified', '')}"
        )

    print("-" * 70)
    input(f"Tekan ENTER untuk kembali...\n")

#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================

def tampilkan_sellreg(data):
    if not data:
        print("Belum ada pendaftaran merchant.\n")
        return

    print("\n=== Daftar Pendaftaran Merchant ===")
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
        ["username", "email", "password", "role", "user_verified"],
        users
    )

def verifikasi_seller():
    data = read_csv(MERCH_FILE)
    tampilkan_sellreg(data)

    if not data:
        return

    reg_id = input("Masukkan REG ID (0 untuk batal): ").strip()
    if reg_id == "0":
        return

    for row in data:
        if row["reg_id"] == reg_id:
            if row["status"] != "pending":
                print("Registrasi ini sudah diproses.")
                input(f"Tekan ENTER untuk kembali...\n")
                return

            keputusan = input("Setujui registrasi? (y/n): ").lower()

            if keputusan == "y":
                row["status"] = "approved"
                update_user_role(row["username"], "merchant")
                print("Merchant diterima.\n")
                input(f"Tekan ENTER untuk kembali...\n")

            elif keputusan == "n":
                row["status"] = "rejected"
                print("Merchant ditolak.\n")
                input(f"Tekan ENTER untuk kembali...\n")

            else:
                print("Pilihan tidak valid.\n")
                input(f"Tekan ENTER untuk kembali...\n")
                return

            write_csv(
                MERCH_FILE,
                ["reg_id", "username", "email", "reason", "status"],
                data
            )
            return

    print("REG ID tidak ditemukan.\n")

#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================

def tampilkan_withdraw(data):
    if not data:
        print("Belum ada pengajuan pengunduran diri.\n")
        return

    print("\n=== Daftar Pengunduran Diri Seller ===")
    print("-" * 70)
    print(f"{'WD ID':<12}{'Username':<15}{'Email':<30}{'Status':<10}")
    print("-" * 70)

    for row in data:
        print(f"{row['wd_id']:<12}{row['username']:<15}{row['email']:<30}{row['status']:<10}")

    print("-" * 70)

def verifikasi_withdraw():
    data = read_csv(WITHDRAW_FILE)
    tampilkan_withdraw(data)

    if not data:
        return

    wd_id = input("Masukkan WD ID (0 untuk batal): ").strip()
    if wd_id == "0":
        return

    for row in data:
        if row["wd_id"] == wd_id:
            if row["status"] != "pending":
                print("Pengajuan ini sudah diproses.")
                input(f"Tekan ENTER untuk kembali...\n")
                return

            keputusan = input("Setujui pengunduran diri? (y/n): ").lower()

            if keputusan == "y":
                row["status"] = "approved"
                update_user_role(row["username"], "user")
                print("Pengunduran diri disetujui.\n")
                input(f"Tekan ENTER untuk kembali...\n")

            elif keputusan == "n":
                row["status"] = "rejected"
                print("Pengunduran diri ditolak.\n")
                input(f"Tekan ENTER untuk kembali...\n")

            else:
                print("Pilihan tidak valid.\n")
                input(f"Tekan ENTER untuk kembali...\n")
                return

            write_csv(
                WITHDRAW_FILE,
                ["wd_id", "username", "reason", "status"],
                data
            )
            return

    print("WD ID tidak ditemukan.\n")

def menu_kelola_seller():
    while True:
        print("""
=== Menu Pengelolaan Merchant ===
1. Lihat Daftar Merchant
2. Verifikasi Pendaftaran Merchant
3. Data Pengunduran Diri Merchant
4. Kembali           
""")

        pilihan = input("Pilih menu (1-4): ").strip()

        if pilihan == "1":
            tampilkan_daftar_seller()
        elif pilihan == "2":
            verifikasi_seller()
        elif pilihan == "3":
            verifikasi_withdraw()
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid.\n")