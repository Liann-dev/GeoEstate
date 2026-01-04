import csv
import uuid
from datetime import datetime

NOTIF_FILE = "data/notifikasi.csv"

def simpan_notifikasi(username, role, pesan):
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