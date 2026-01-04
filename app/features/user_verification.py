import csv
import os

FILE_USERS = "data/users.csv"
FILE_REQUEST = "data/user_verification_requests.csv"


# =========================
# UTIL
# =========================
def load_users():
    with open(FILE_USERS, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_users(data):
    with open(FILE_USERS, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def load_requests():
    if not os.path.exists(FILE_REQUEST):
        return []
    with open(FILE_REQUEST, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_requests(data):
    with open(FILE_REQUEST, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["request_id", "username", "status", "timestamp", "admin_note"]
        )
        writer.writeheader()
        writer.writerows(data)


# =========================
# VIEW
# =========================
def tampilkan_request():
    data = load_requests()

    if not data:
        print("\nBelum ada request verifikasi.\n")
        input("Tekan ENTER...")
        return

    print("\n=== DAFTAR REQUEST VERIFIKASI USER ===")
    print("-" * 80)
    print(f"{'USERNAME':<15}{'STATUS':<15}{'TIMESTAMP':<25}{'CATATAN'}")
    print("-" * 80)

    for r in data:
        note = r["admin_note"] if r["admin_note"] else "-"
        print(f"{r['username']:<15}{r['status']:<15}{r['timestamp']:<25}{note}")

    print("-" * 80)


# =========================
# ACTION
# =========================
def set_user_verified(username, value):
    users = load_users()
    found = False

    for u in users:
        if u["username"] == username:
            u["user_verified"] = "true" if value else "false"
            found = True
            break

    if found:
        save_users(users)


def proses_request(status_target):
    requests = load_requests()
    pending = [r for r in requests if r["status"] == "pending"]

    if not pending:
        print("\nTidak ada request pending.\n")
        input("Tekan ENTER...")
        return

    tampilkan_request()
    username = input("\nMasukkan username (ENTER untuk batal): ").strip()
    if not username:
        return

    for r in requests:
        if r["username"] == username and r["status"] == "pending":
            print(f"\nMemproses request user: {username}")
            note = input("Catatan admin (opsional): ").strip()

            r["status"] = status_target
            r["admin_note"] = note

            if status_target == "approved":
                set_user_verified(username, True)

            save_requests(requests)

            print(f"\n✅ Request berhasil di-{status_target}.")
            input("Tekan ENTER...")
            return

    print("\n❌ Request pending tidak ditemukan.")
    input("Tekan ENTER...")


# =========================
# MENU
# =========================
def menu_verifikasi_user():
    while True:
        print("""
=== MENU VERIFIKASI USER (ADMIN) ===
1. Lihat Request Verifikasi
2. Setujui Verifikasi User
3. Tolak Verifikasi User
0. Kembali
""")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            tampilkan_request()
            input("Tekan ENTER...")
        elif pilih == "2":
            proses_request("approved")
        elif pilih == "3":
            proses_request("rejected")
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.\n")
