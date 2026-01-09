import csv
import os
from app.features.notifikasi_service import tambah_notifikasi

FILE_USERS = "data/users.csv"
FILE_REQUEST = "data/user_verification_requests.csv"
FILE_BIODATA = "data/biodata.csv"

# =========================
# UTIL LOAD / SAVE
# =========================
def load_users():
    with open(FILE_USERS, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_users(data):
    with open(FILE_USERS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def load_requests():
    if not os.path.exists(FILE_REQUEST):
        return []
    with open(FILE_REQUEST, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_requests(data):
    with open(FILE_REQUEST, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["request_id", "username", "status", "timestamp", "admin_note"]
        )
        writer.writeheader()
        writer.writerows(data)

def get_biodata(username):
    if not os.path.exists(FILE_BIODATA):
        return None
    with open(FILE_BIODATA, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["username"] == username:
                return row
    return None

def hapus_biodata(username):
    if not os.path.exists(FILE_BIODATA):
        return

    with open(FILE_BIODATA, newline="", encoding="utf-8") as f:
        data = list(csv.DictReader(f))

    data_baru = [row for row in data if row["username"] != username]

    if len(data) == len(data_baru):
        return  # tidak ada data yg dihapus

    with open(FILE_BIODATA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data_baru[0].keys() if data_baru else data[0].keys())
        writer.writeheader()
        writer.writerows(data_baru)


# =========================
# VIEW
# =========================
def tampilkan_pending():
    data = [r for r in load_requests() if r["status"] == "pending"]

    if not data:
        print("\nTidak ada request pending.")
        input("Tekan ENTER...")
        return []

    print("\n=== REQUEST VERIFIKASI (PENDING) ===")
    print("-" * 70)
    print(f"{'USERNAME':<15}{'STATUS':<12}{'TIMESTAMP'}")
    print("-" * 70)

    for r in data:
        print(f"{r['username']:<15}{r['status']:<12}{r['timestamp']}")

    print("-" * 70)
    return data

def tampilkan_history():
    data = [r for r in load_requests() if r["status"] != "pending"]

    if not data:
        print("\nBelum ada history verifikasi.")
        input("Tekan ENTER...")
        return

    print("\n=== HISTORY VERIFIKASI USER ===")
    print("-" * 90)
    print(f"{'USERNAME':<15}{'STATUS':<12}{'TIMESTAMP':<25}{'CATATAN'}")
    print("-" * 90)

    for r in data:
        note = r["admin_note"] if r["admin_note"] else "-"
        print(f"{r['username']:<15}{r['status']:<12}{r['timestamp']:<25}{note}")

    print("-" * 90)
    input("Tekan ENTER...")

# =========================
# ACTION
# =========================
def set_user_verified(username, value):
    users = load_users()
    for u in users:
        if u["username"] == username:
            u["user_verified"] = "true" if value else "false"
            break
    save_users(users)

def tampilkan_biodata(username):
    biodata = get_biodata(username)
    if not biodata:
        print("\n❌ Biodata user tidak ditemukan.")
        return False

    print("\n======= DATA KTP USER =======")
    for k, v in biodata.items():
        print(f"{k.replace('_',' ').title():<22}: {v}")
    print("=" * 35)
    return True

def proses_request_pending():
    pending = tampilkan_pending()
    if not pending:
        return

    username = input("\nMasukkan username (ENTER batal): ").strip()
    if not username:
        return

    requests = load_requests()

    for r in requests:
        if r["username"] == username and r["status"] == "pending":
            if not tampilkan_biodata(username):
                input("Tekan ENTER...")
                return

            print("\n[ 1 ] Approve")
            print("[ 2 ] Decline")
            print("[ 0 ] Batal")
            pilih = input("Pilih keputusan: ").strip()

            if pilih == "0":
                print("\n❎ Proses dibatalkan.")
                input("Tekan ENTER...")
                return

            elif pilih == "1":
                r["status"] = "approved"
                r["admin_note"] = ""
                set_user_verified(username, True)
                tambah_notifikasi(
                    username=username,
                    pesan="✅ Akun Anda telah berhasil diverifikasi oleh Admin.",
                    role="user",
                    redirect="profile"
                )

            elif pilih == "2":
                note = input("Alasan penolakan (wajib): ").strip()
                if not note:
                    print("❌ Catatan wajib diisi.")
                    input("Tekan ENTER...")
                    return
                r["status"] = "rejected"
                r["admin_note"] = note
                hapus_biodata(username) 
                tambah_notifikasi(
                    username=username,
                    pesan=f"❌ Verifikasi akun Anda ditolak. Alasan: {note}",
                    role="user",
                    redirect="profile"
                )

            else:
                print("Pilihan tidak valid.")
                input("Tekan ENTER...")
                return

            save_requests(requests)
            print("\n✅ Request berhasil diproses.")
            input("Tekan ENTER...")
            return

    print("\n❌ Request tidak ditemukan.")
    input("Tekan ENTER...")

# =========================
# MENU ADMIN
# =========================
def menu_verifikasi_user():
    while True:
        print("""
=== MENU VERIFIKASI USER (ADMIN) ===
1. Lihat Request Verifikasi User
2. Lihat History Verifikasi User
0. Kembali
""")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            proses_request_pending()
        elif pilih == "2":
            tampilkan_history()
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")
