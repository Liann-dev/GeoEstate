import csv
import uuid
from datetime import datetime

NOTIF_FILE = "data/notifikasi.csv"

def simpan_notifikasi(username, role, pesan, redirect="-"):
    with open(NOTIF_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            str(uuid.uuid4()),
            username,
            role,
            pesan,
            "unread",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            redirect
        ])
