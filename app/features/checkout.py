import csv
import os
import random
from datetime import datetime
from app.features.notifikasi_service import tambah_notifikasi


TRANSAKSI_FILE = "data/transaksi.csv"

def checkout(username, p):
    print("\n=== BOOKING PROPERTI ===")

    harga = p.get("harga", 0)
    penjual = p.get("penjual")
    if not penjual:
        print("❌ ERROR: Properti tidak memiliki penjual.")
        input("Tekan ENTER...")
        return

    print(f"Properti : {p['nama']}")
    print(f"Harga    : Rp {harga}")

    tanggal_booking = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_transaksi = f"GES-{random.randint(1000, 9999)}"

    os.makedirs(os.path.dirname(TRANSAKSI_FILE), exist_ok=True)
    transaksi_exists = os.path.exists(TRANSAKSI_FILE)

    with open(TRANSAKSI_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not transaksi_exists:
            writer.writerow([
                "id_transaksi",
                "username_pembeli",
                "penjual",
                "id_properti",
                "nama_properti",
                "harga",
                "tanggal",
                "transaksi",
                "status",
                "session"
            ])

        writer.writerow([
            id_transaksi,
            username,
            penjual,
            p["id"],
            p["nama"],
            harga,
            tanggal_booking,
            "booking",
            "Menunggu Konfirmasi",
            username
        ])

        writer.writerow([
            id_transaksi,
            username,
            penjual,
            p["id"],
            p["nama"],
            harga,
            tanggal_booking,
            "booking",
            "Menunggu Konfirmasi",
            penjual
        ])

        print("\n✅ Booking berhasil!")
    print("📌 Status: Menunggu Konfirmasi")

    tambah_notifikasi(
        penjual,
        f"📌 Booking baru untuk properti '{p['nama']}' dari buyer {username}"
    )

    input("Tekan ENTER untuk kembali...")
