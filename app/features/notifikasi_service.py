import csv
import os
import uuid
from datetime import datetime

NOTIF_FILE = "data/notifikasi.csv"

FIELDNAMES = [
    "id",
    "username",
    "role",
    "pesan",
    "status",
    "timestamp",
    "redirect"
]


def init_notif_file():
    if not os.path.exists(NOTIF_FILE):
        os.makedirs(os.path.dirname(NOTIF_FILE), exist_ok=True)
        with open(NOTIF_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def tambah_notifikasi(username, pesan, role="user", redirect="-"):
    init_notif_file()

    with open(NOTIF_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "id": f"NTF-{uuid.uuid4().hex[:8]}",
            "username": username,
            "role": role,
            "pesan": pesan,
            "status": "unread",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "redirect": redirect
        })


def get_unread_notifikasi(username):
    init_notif_file()
    hasil = []

    with open(NOTIF_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username and row["status"] == "unread":
                hasil.append(row)

    return hasil


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
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)
