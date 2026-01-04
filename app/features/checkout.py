import csv
import os
import random
from datetime import datetime

TRANSAKSI_FILE = "data/transaksi.csv"

def checkout(username, p):
    print("\n=== BOOKING PROPERTI ===")

    harga = p.get("harga", 0)
    penjual = p.get("penjual", "Naufal")  # sementara

    print(f"Properti : {p['nama']}")
    print(f"Harga    : Rp {harga}")

    tanggal_booking = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_transaksi = f"GES-{random.randint(1000, 9999)}"

    transaksi_exists = os.path.exists(TRANSAKSI_FILE)

    with open(TRANSAKSI_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # HEADER (TAMBAH session)
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

        # ================= BARIS UNTUK PEMBELI =================
        writer.writerow([
            id_transaksi,
            username,           # pembeli
            penjual,
            p["id"],
            p["nama"],
            harga,
            tanggal_booking,
            "booking",
            "Menunggu Konfirmasi",
            username             # session pembeli
        ])

        # ================= BARIS UNTUK PENJUAL =================
        writer.writerow([
            id_transaksi,
            username,           # pembeli tetap sama
            penjual,
            p["id"],
            p["nama"],
            harga,
            tanggal_booking,
            "booking",
            "Menunggu Konfirmasi",
            penjual              # session penjual
        ])

    print("\n✅ Booking berhasil!")
    print("📌 Status: Menunggu Konfirmasi")
    input("Tekan ENTER untuk kembali...")
