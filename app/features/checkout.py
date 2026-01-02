import csv
import os
import uuid
import random
from datetime import datetime

TRANSAKSI_FILE = "data/transaksi.csv"
SCHEDULE_FILE = "data/booking_schedule.csv"


def input_schedule():
    while True:
        schedule = input("Masukkan jadwal (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(schedule, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Format tanggal salah. Contoh: 2025-01-10")


def checkout(username, p):
    print("\n=== BOOKING PROPERTI ===")

    harga = p.get("harga", 0)
    penjual = p.get("penjual", "Naufal")  # sementara

    print(f"Properti : {p['nama']}")
    print(f"Harga    : Rp {harga}")

    # ================= INPUT SCHEDULE =================
    schedule = input_schedule()

    tanggal_booking = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_transaksi = f"GES-{random.randint(1000, 9999)}"

    # ================= SIMPAN TRANSAKSI =================
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
                "status"
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
            "Menunggu Konfirmasi"
        ])

    # ================= SIMPAN SCHEDULE =================
    schedule_exists = os.path.exists(SCHEDULE_FILE)

    with open(SCHEDULE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not schedule_exists:
            writer.writerow([
                "id_transaksi",
                "schedule"
            ])

        writer.writerow([
            id_transaksi,
            schedule.strftime("%Y-%m-%d")
        ])

    print("\n✅ Booking berhasil!")
    print(f"📅 Jadwal: {schedule}")
    print("📌 Status: Menunggu Konfirmasi")
    while True:
        input("Tekan ENTER untuk kembali...")
        break