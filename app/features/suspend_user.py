import csv
import os

FILE_USERS = "data/users.csv"

def load_users():
    if not os.path.exists(FILE_USERS):
        return []

    with open(FILE_USERS, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_users(users):
    with open(FILE_USERS, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['username', 'email', 'password', 'role', 'user_verified', 'suspend']
        )
        writer.writeheader()
        writer.writerows(users)

def tampilkan_user(users):
    print("\n" + "=" * 70)
    print(" USERNAME        | ROLE     | STATUS")
    print("=" * 70)

    for u in users:
        status = (
            "🚫 SUSPEND" if u['suspend'] == 'true'
            else "✅ AKTIF"
        )
        print(f" {u['username']:<15} | {u['role']:<8} | {status}")

    print("=" * 70)

def proses_suspend():
    users = load_users()
    tampilkan_user(users)

    username = input("\nUsername yang akan disuspend (ENTER untuk batal): ").strip()
    if not username:
        return

    for u in users:
        if u['username'] == username:
            if u['role'] == 'admin':
                print("❌ Admin tidak boleh disuspend.")
                input("ENTER...")
                return

            if u['suspend'] == 'true':
                print("⚠️ User sudah disuspend.")
                input("ENTER...")
                return

            u['suspend'] = 'true'
            save_users(users)
            print("✅ User berhasil disuspend.")
            input("ENTER...")
            return

    print("❌ User tidak ditemukan.")
    input("ENTER...")

def proses_unsuspend():
    users = load_users()
    tampilkan_user(users)

    username = input("\nUsername yang akan diaktifkan kembali (ENTER untuk batal): ").strip()
    if not username:
        return

    for u in users:
        if u['username'] == username:
            if u['suspend'] == 'false':
                print("⚠️ User tidak dalam status suspend.")
                input("ENTER...")
                return

            u['suspend'] = 'false'
            save_users(users)
            print("✅ User berhasil diaktifkan kembali.")
            input("ENTER...")
            return

    print("❌ User tidak ditemukan.")
    input("ENTER...")

def suspend_user():
    while True:
        print("\n=== KELOLA USER ===")
        print("1. 🚫 Suspend User")
        print("2. 🔓 Unsuspend User")
        print("0. 🔙 Kembali")

        pilih = input("\nPilih opsi: ").strip()

        if pilih == "1":
            proses_suspend()

        elif pilih == "2":
            proses_unsuspend()

        elif pilih == "0":
            return

        else:
            print("❌ Pilihan tidak valid!")
