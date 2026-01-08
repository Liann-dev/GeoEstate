import csv
import os

from app.features.booking import booking
from app.features.wishlist import tambah_ke_wishlist
from app.features.jadwal_survey import survey
from app.features.chat import buka_chat, normalize_session
from app.features.notifikasi_helper import simpan_notifikasi

FILE_USERS = "data/users.csv"
FILE_TRANSAKSI = "data/transaksi.csv"


# =========================
# USER VERIFIED
# =========================
def get_user_verified(username):
    if not os.path.exists(FILE_USERS):
        return False

    with open(FILE_USERS, newline="", encoding="utf-8") as f:
        for user in csv.DictReader(f):
            if user["username"].lower() == username.lower():
                return user.get("user_verified", "").lower() == "true"
    return False


# =========================
# CEK BOOKING AKTIF BUYER
# =========================
def get_booking_aktif(username, id_properti):
    if not os.path.exists(FILE_TRANSAKSI):
        return None

    with open(FILE_TRANSAKSI, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (
                row["username_pembeli"] == username
                and row["id_properti"] == id_properti
                and row["status"] == "Booked"
            ):
                return row
    return None


# =========================
# AJUKAN PEMBELIAN
# =========================
def ajukan_pembelian(booking_row):
    if not os.path.exists(FILE_TRANSAKSI):
        return False

    with open(FILE_TRANSAKSI, newline="", encoding="utf-8") as f:
        semua = list(csv.DictReader(f))

    for r in semua:
        if r["id_transaksi"] == booking_row["id_transaksi"]:
            r["status"] = "Menunggu Pembayaran"

    with open(FILE_TRANSAKSI, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=semua[0].keys())
        writer.writeheader()
        writer.writerows(semua)

    # 🔔 Notifikasi ke seller
    simpan_notifikasi(
        booking_row["penjual"],
        "seller",
        f"Buyer {booking_row['username_pembeli']} mengajukan pembelian properti '{booking_row['nama_properti']}'",
        redirect="transaksi_seller"
    )

    return True


# =========================
# DETAIL PROPERTI
# =========================
def detail_properti(username, p):
    harga_txt = f"Rp {int(p['harga']):,}".replace(",", ".")
    status = p.get("status", "available")

    status_label = {
        "available": "🟢 Tersedia",
        "booked": "🟡 Sedang Dibooking",
        "sold": "🔴 Terjual"
    }.get(status, status)

    while True:
        print("\n" * 50)
        print("========================================")
        print("           DETAIL PROPERTI               ")
        print("========================================")
        print(f" 🏠 {p['nama']}")
        print(f" 📍 {p['lokasi']}")
        print(f" 💰 {harga_txt}")
        print(f" 📦 Status  : {status_label}")
        print(f" 👤 Penjual : {p['penjual']}")
        print("========================================")

        print("\n[ OPSI ]")

        if status != "sold":
            print("1. 📅 Jadwalkan Survei")

        if status == "available":
            print("2. 🛒 Booking")

        booking_user = get_booking_aktif(username, p["id"])
        if status == "booked" and booking_user:
            print("3. 💰 Beli Properti")

        if status != "sold":
            print("4. ➕ Tambahkan ke Wishlist")

        print("5. 💬 Chat Penjual")
        print("0. 🔙 Kembali")
        print("----------------------------------------")

        pilihan = input(">> Pilih opsi: ").strip()

        # ===== SURVEY =====
        if pilihan == "1":
            if not get_user_verified(username):
                print("❌ Anda belum terverifikasi.")
                input("ENTER...")
                continue

            if username == p["penjual"]:
                print("❌ Tidak bisa survei properti sendiri.")
                input("ENTER...")
                continue

            survey(username, p)

        # ===== BOOKING =====
        elif pilihan == "2" and status == "available":
            if not get_user_verified(username):
                print("❌ Anda belum terverifikasi.")
                input("ENTER...")
                continue

            if username == p["penjual"]:
                print("❌ Tidak bisa booking properti sendiri.")
                input("ENTER...")
                continue

            booking(username, p)

        # ===== BELI PROPERTI =====
        elif pilihan == "3" and status == "booked" and booking_user:
            sukses = ajukan_pembelian(booking_user)

            if sukses:
                print("\n📢 Permintaan pembelian berhasil dikirim.")
                print("⏳ Menunggu konfirmasi seller...")
            else:
                print("❌ Gagal mengajukan pembelian.")

            input("ENTER...")

        # ===== WISHLIST =====
        elif pilihan == "4":
            tambah_ke_wishlist(username, p["id"])

        # ===== CHAT =====
        elif pilihan == "5":
            if username == p["penjual"]:
                print("❌ Tidak bisa chat diri sendiri.")
                input("ENTER...")
                continue

            session = normalize_session(username, p["penjual"])
            buka_chat(username, session, p["penjual"])

        elif pilihan == "0":
            return

        else:
            print("❌ Opsi tidak valid.")
            input("ENTER...")
