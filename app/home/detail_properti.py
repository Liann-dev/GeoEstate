import csv
import os
from app.home.review_user import rating_seller
from app.features.booking import booking
from app.features.wishlist import tambah_ke_wishlist
from app.features.jadwal_survey import survey
from app.features.chat import buka_chat, normalize_session
from app.features.notifikasi_helper import simpan_notifikasi

FILE_USERS = "data/users.csv"
FILE_TRANSAKSI = "data/transaksi.csv"
REVIEW_FILE = "data/reviews.csv"


# =========================
# LIHAT ULASAN SELLER
# =========================
def lihat_ulasan_seller(username_seller):
    if not os.path.exists(REVIEW_FILE):
        print("\n📭 Belum ada ulasan.")
        input("ENTER...")
        return

    with open(REVIEW_FILE, newline="", encoding="utf-8") as f:
        reviews = list(csv.DictReader(f))

    data = [r for r in reviews if r["seller"] == username_seller]

    if not data:
        print("\n📭 Seller ini belum memiliki ulasan.")
        input("ENTER...")
        return

    print(f"\n=== ULASAN SELLER: {username_seller} ===\n")

    for i, r in enumerate(data, 1):
        print(f"[{i}]")
        print(f"⭐ Rating   : {r['rating']}/5")
        print(f"💬 Komentar : {r['komentar']}")
        print(f"🕒 Tanggal  : {r['tanggal']}")
        print("-" * 40)

    input("ENTER...")


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
# CEK BOOKING AKTIF
# =========================
def get_booking_aktif(username, id_properti):
    if not os.path.exists(FILE_TRANSAKSI):
        return None

    with open(FILE_TRANSAKSI, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (
                row["id_properti"] == id_properti
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
    rating = rating_seller(p["penjual"])

    # 🔑 CEK STATUS REAL DARI TRANSAKSI
    booking_row = get_booking_aktif(username, p["id"])

    if not p.get("tersedia", "true").lower() == "true":
        status = "sold"
    elif booking_row:
        status = "booked"
    else:
        status = "available"

    status_label = {
        "available": "🟢 Tersedia",
        "booked": "🟡 Sedang Dibooking",
        "sold": "🔴 Terjual"
    }[status]

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
        print(f" ⭐ Rating  : {rating}")
        print("========================================")

        print("\n[ OPSI ]")

        if status != "sold":
            print("1. 📅 Jadwalkan Survei")

        if status == "available":
            print("2. 🛒 Booking")

        if status == "booked" and booking_row and booking_row["username_pembeli"] == username:
            print("3. 💰 Beli Properti")

        if status != "sold":
            print("4. ➕ Tambahkan ke Wishlist")

        print("5. 💬 Chat Penjual")
        print("6. 💯 Lihat Ulasan Seller")
        print("0. 🔙 Kembali")
        print("----------------------------------------")

        pilihan = input(">> Pilih opsi: ").strip()

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
            return  # refresh status saat masuk ulang

        elif pilihan == "3" and status == "booked" and booking_row and booking_row["username_pembeli"] == username:
            sukses = ajukan_pembelian(booking_row)
            if sukses:
                print("\n📢 Permintaan pembelian berhasil dikirim.")
            else:
                print("❌ Gagal mengajukan pembelian.")
            input("ENTER...")
            return

        elif pilihan == "4":
            if username == p["penjual"]:
                print("❌ Tidak bisa wishlist properti sendiri.")
                input("ENTER...")
                continue
            tambah_ke_wishlist(username, p["id"])

        elif pilihan == "5":
            if username == p["penjual"]:
                print("❌ Tidak bisa chat diri sendiri.")
                input("ENTER...")
                continue
            session = normalize_session(username, p["penjual"])
            buka_chat(username, session, p["penjual"])

        elif pilihan == "6":
            lihat_ulasan_seller(p["penjual"])

        elif pilihan == "0":
            return

        else:
            print("❌ Opsi tidak valid.")
            input("ENTER...")
