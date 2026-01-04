import csv
import os

TRANSAKSI_FILE = "data/transaksi.csv"

def notifikasi_seller(username):
    notifikasi = []

    if not os.path.exists(TRANSAKSI_FILE):
        return notifikasi

    with open(TRANSAKSI_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # 🔑 FILTER PALING PENTING
            if row.get("session") != username:
                continue

            status = row.get("status", "")
            nama = row.get("nama_properti", "-")

            if status == "Menunggu Konfirmasi":
                notifikasi.append(f"📌 Booking baru untuk '{nama}'")

            elif status == "Dibatalkan":
                notifikasi.append(f"❌ Booking '{nama}' dibatalkan buyer")

            elif status == "Lunas / Selesai":
                notifikasi.append(f"🎉 Properti '{nama}' berhasil dijual")

    return notifikasi
