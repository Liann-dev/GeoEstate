import csv
import os
import uuid
import time
from datetime import datetime

TRANSAKSI_FILE = "data/transaksi.csv"


def checkout(username, p):
    print("\n=== BOOKING PROPERTI ===")

    harga = p.get("harga", 0)
    penjual = p.get("penjual", "Naufal")  # sementara / default

    print(f"Properti : {p['nama']}")
    print(f"Harga    : Rp {harga}")

    tanggal_booking = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    id_transaksi = str(uuid.uuid4())[:8]

    file_exists = os.path.exists(TRANSAKSI_FILE)

    with open(TRANSAKSI_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # HEADER HARUS SAMA PERSIS
        if not file_exists:
            writer.writerow([
                "id_transaksi",
                "username_pembeli",
                "penjual",
                "id_properti",
                "nama_properti",
                "harga",
                "tanggal",
                "transaksi",
                "status"
            ])

        writer.writerow([
            id_transaksi,
            username,           # username_pembeli
            penjual,            # penjual
            p["id"],            # id_properti
            p["nama"],          # nama_properti
            harga,
            tanggal_booking,    # tanggal
            "Booking Properti", # transaksi
            "Menunggu Konfirmasi"
        ])

    print("\n✅ Booking berhasil!")
    print("📌 Status: Menunggu Konfirmasi")
    time.sleep(2)