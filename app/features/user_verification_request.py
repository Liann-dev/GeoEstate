import csv
import os
import uuid
from datetime import datetime

FILE_REQUEST = "data/user_verification_requests.csv"


# =========================
# INIT FILE
# =========================
def init_request_file():
    if not os.path.exists(FILE_REQUEST):
        with open(FILE_REQUEST, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "request_id",
                "username",
                "status",
                "timestamp",
                "admin_note"
            ])


# =========================
# GET LATEST REQUEST
# =========================
def get_verification_status(username):
    """
    Return:
    - None -> belum pernah ajukan
    - dict -> request terbaru user
    """
    if not os.path.exists(FILE_REQUEST):
        return None

    with open(FILE_REQUEST, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = [r for r in reader if r["username"] == username]

    if not data:
        return None

    # ambil request TERBARU
    data.sort(key=lambda x: x["timestamp"], reverse=True)
    return data[0]


# =========================
# CHECK ACTIVE REQUEST
# =========================
def has_active_request(username):
    """
    True jika user masih pending
    """
    req = get_verification_status(username)
    return req is not None and req["status"] == "pending"


# =========================
# AJUKAN VERIFIKASI
# =========================
def ajukan_verifikasi_user(username):
    init_request_file()

    # Cegah double request
    if has_active_request(username):
        print("❌ Anda sudah mengajukan verifikasi dan sedang diproses.")
        input("Tekan ENTER untuk kembali...")
        return

    request_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE_REQUEST, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
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
