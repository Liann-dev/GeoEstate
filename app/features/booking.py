import csv
import os
import random
from datetime import datetime
from app.features.notifikasi_service import tambah_notifikasi

TRANSAKSI_FILE = "data/transaksi.csv"
PROPERTI_FILE = "data/properti.csv"


# =========================
# UTIL: LOAD PROPERTI
# =========================
def load_properti():
    if not os.path.exists(PROPERTI_FILE):
        return []
    with open(PROPERTI_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def update_status_properti(id_properti, status_baru):
    data = load_properti()
    for p in data:
        if p["id"] == id_properti:
            p["status"] = status_baru
            break

    with open(PROPERTI_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


# =========================
# CEK PROPERTI SEDANG BOOKING
# =========================
def properti_tidak_available(id_properti):
    for p in load_properti():
        if p["id"] == id_properti:
            return p["status"] != "available"
    return False


# =========================
# CEK BUYER SUDAH BOOKING
# =========================
def buyer_sudah_booking(username, id_properti):
    if not os.path.exists(TRANSAKSI_FILE):
        return False

    with open(TRANSAKSI_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (
                row["username_pembeli"] == username
                and row["id_properti"] == id_properti
                and row["status"] not in ("Lunas / Selesai", "Dibatalkan")
            ):
                return True
    return False


# =========================
# BOOKING PROPERTI
# =========================
def booking(username, p):
    print("\n=== BOOKING PROPERTI ===")

    # ===== VALIDASI DASAR =====
    if properti_tidak_available(p["id"]):
        print("❌ Properti sedang di-booking / tidak tersedia.")
        input("Tekan ENTER...")
        return

    if buyer_sudah_booking(username, p["id"]):
        print("❌ Anda sudah memiliki booking aktif untuk properti ini.")
        input("Tekan ENTER...")
        return

    if username == p["penjual"]:
        print("❌ Tidak bisa booking properti sendiri.")
        input("Tekan ENTER...")
        return

    # ===== DATA TRANSAKSI =====
    id_transaksi = f"GES-{random.randint(1000, 9999)}"
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs(os.path.dirname(TRANSAKSI_FILE), exist_ok=True)
    file_exists = os.path.exists(TRANSAKSI_FILE)

    with open(TRANSAKSI_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

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
                "status",
                "session"
            ])

        # session buyer
        writer.writerow([
            id_transaksi,
            username,
            p["penjual"],
            p["id"],
            p["nama"],
            p["harga"],
            tanggal,
            "booking",
            "Menunggu Konfirmasi",
            username
        ])

        # session seller
        writer.writerow([
            id_transaksi,
            username,
            p["penjual"],
            p["id"],
            p["nama"],
            p["harga"],
            tanggal,
            "booking",
            "Menunggu Konfirmasi",
            p["penjual"]
        ])

    # ===== UPDATE STATUS PROPERTI =====
    update_status_properti(p["id"], "pending")

    # ===== NOTIFIKASI SELLER =====
    tambah_notifikasi(
        p["penjual"],
        f"📌 Permintaan booking baru untuk properti '{p['nama']}' dari buyer {username}",
        role="seller",
        redirect="transaksi_seller"
    )

    print("\n✅ Booking berhasil diajukan.")
    print("⏳ Menunggu konfirmasi dari seller.")
    input("Tekan ENTER untuk kembali...")
