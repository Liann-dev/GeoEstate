import csv
import os
import uuid
from datetime import datetime

NOTIF_FILE = "data/notifikasi.csv"


def init_notif_file():
    if not os.path.exists(NOTIF_FILE):
        os.makedirs(os.path.dirname(NOTIF_FILE), exist_ok=True)
        with open(NOTIF_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id",
                "username",
                "role",
                "pesan",
                "status",
                "timestamp"
            ])


def tambah_notifikasi(username, pesan, role="seller"):
    init_notif_file()

    with open(NOTIF_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            f"NTF-{uuid.uuid4().hex[:8]}",
            username,
            role,
            pesan,
            "unread",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])


def get_unread_notifikasi(username):
    init_notif_file()
    notifikasi = []

    with open(NOTIF_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row.get("username") == username
                and row.get("status") == "unread"
            ):
                notifikasi.append(row)

    return notifikasi


def tandai_semua_read(username):
    init_notif_file()
    data = []

    with open(NOTIF_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                row["status"] = "read"
            data.append(row)

    with open(NOTIF_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "username", "role", "pesan", "status", "timestamp"]
        )
        writer.writeheader()
        writer.writerows(data)
