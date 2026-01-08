import csv
import uuid
import os
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
            writer = csv.writer(f)
            writer.writerow(FIELDNAMES)

def simpan_notifikasi(username, role, pesan, redirect="-"):
    init_notif_file()

    with open(NOTIF_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            f"NTF-{uuid.uuid4().hex[:8]}",
            username,
            role,
            pesan,
            "unread",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            redirect
        ])
