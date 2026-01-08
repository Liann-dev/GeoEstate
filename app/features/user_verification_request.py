import csv
import os
import uuid
from datetime import datetime
from app.features.biodata_input import input_biodata

FILE_REQUEST = "data/user_verification_requests.csv"
FIELDS = ["request_id", "username", "status", "timestamp", "admin_note"]


# =========================
# CHECK ACTIVE REQUEST
# =========================
def has_active_request(username):
    if not os.path.exists(FILE_REQUEST):
        return False

    with open(FILE_REQUEST, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username and row["status"] == "pending":
                return True
    return False


# =========================
# AJUKAN VERIFIKASI (FIXED)
# =========================
def ajukan_verifikasi_user(username):
    # 1 CEGAH DOUBLE REQUEST
    if has_active_request(username):
        print("\n⏳ Anda sudah mengajukan verifikasi.")
        input("Tekan ENTER...")
        return

    # 2 WAJIB INPUT BIODATA KTP
    sukses = input_biodata(username)
    if not sukses:
        print("\n❌ Verifikasi dibatalkan.")
        input("Tekan ENTER...")
        return

    # 3 BUAT REQUEST VERIFIKASI
    request_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_kosong = not os.path.exists(FILE_REQUEST) or os.path.getsize(FILE_REQUEST) == 0

    with open(FILE_REQUEST, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if file_kosong:
            writer.writeheader()

        writer.writerow({
            "request_id": request_id,
            "username": username,
            "status": "pending",
            "timestamp": timestamp,
            "admin_note": ""
        })

    print("\n✅ Permintaan verifikasi berhasil diajukan.")
    print("⏳ Silakan tunggu proses verifikasi dari Admin.")
    input("Tekan ENTER untuk kembali...")
