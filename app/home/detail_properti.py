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


# ===================== ULASAN SELLER =====================
def lihat_ulasan_seller(username_seller):
    if not os.path.exists(REVIEW_FILE):
        print("\n📭 Belum ada ulasan.")
        input("ENTER...")
        return

    with open(REVIEW_FILE, newline="", encoding="utf-8") as f:
        reviews = list(csv.DictReader(f))

    data = [r for r in reviews if r.get("penjual") == username_seller]

    if not data:
        print(f"\n📭 Seller '{username_seller}' belum memiliki ulasan.")
        input("ENTER...")
        return

    print(f"\n=== ULASAN SELLER: {username_seller} ===\n")
    for i, r in enumerate(data, 1):
        print(f"[{i}]")
        print(f"⭐ Rating   : {r.get('rating','-')}/5")
        print(f"💬 Komentar : {r.get('review_text','-')}")
        print(f"🕒 Tanggal  : {r.get('tanggal_review','-')}")
        print("-" * 40)

    input("ENTER...")


# ===================== USER VERIFIED =====================
def get_user_verified(username):
    if not os.path.exists(FILE_USERS):
        return False

    with open(FILE_USERS, newline="", encoding="utf-8") as f:
        for user in csv.DictReader(f):
            if user["username"].lower() == username.lower():
                return user.get("user_verified", "").lower() == "true"
    return False


# ===================== TRANSAKSI AKTIF =====================
def get_booking_aktif(id_properti):
    """Mengambil transaksi aktif (Booked / Menunggu Pembayaran) berdasarkan properti"""
    if not os.path.exists(FILE_TRANSAKSI):
        return None

    with open(FILE_TRANSAKSI, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["id_properti"] == str(id_properti):
                if row["status"] in ("Booked", "Menunggu Pembayaran"):
                    return row
    return None


# ===================== AJUKAN PEMBELIAN =====================
def ajukan_pembelian(trx):
    if not os.path.exists(FILE_TRANSAKSI):
        return False

    with open(FILE_TRANSAKSI, newline="", encoding="utf-8") as f:
        semua = list(csv.DictReader(f))

    for r in semua:
        if r["id_transaksi"] == trx["id_transaksi"]:
            r["status"] = "Menunggu Pembayaran"

    with open(FILE_TRANSAKSI, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=semua[0].keys())
        writer.writeheader()
        writer.writerows(semua)

    simpan_notifikasi(
        trx["penjual"],
        "seller",
        f"Buyer {trx['username_pembeli']} mengajukan pembelian properti '{trx['nama_properti']}'",
        redirect="transaksi_seller"
    )

    return True


# ===================== DETAIL PROPERTI =====================
def detail_properti(username, p):
    harga_txt = f"Rp {int(p['harga']):,}".replace(",", ".")
    rating = rating_seller(p["penjual"])

    trx = get_booking_aktif(p["id"])

    # ===== STATUS FINAL =====
    if p["status"].lower() == "sold":
        status = "sold"
    elif trx:
        if trx["username_pembeli"] == username:
            status = "booked_owner"
        else:
            status = "booked_other"
    else:
        status = "available"

    status_label = {
        "available": "🟢 Tersedia",
        "booked_owner": "🟡 Dibooking (Anda)",
        "booked_other": "🟡 Sedang Dibooking",
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
        print(f" ⭐ Rating Penjual : {rating}")
        print("========================================")

        print("\n[ OPSI ]")

        if status == "available":
            print("1. 📅 Jadwalkan Survei")
            print("2. 🛒 Booking")
            print("4. ➕ Tambahkan ke Wishlist")

        elif status == "booked_owner":
            print("3. 💰 Beli Properti")

        elif status == "booked_other":
            print("4. ➕ Tambahkan ke Wishlist")

        print("5. 💬 Chat Penjual")
        print("6. 💯 Lihat Ulasan Seller")
        print("0. 🔙 Kembali")
        print("----------------------------------------")

        pilihan = input(">> Pilih opsi: ").strip()

        if pilihan == "1" and status == "available":
            if not get_user_verified(username):
                print("❌ Anda belum terverifikasi.")
                input("ENTER...")
                continue
            if username == p["penjual"]:
                print("❌ Tidak bisa menjadwalkan survei untuk properti sendiri.")
                input("ENTER...")
                continue
            survey(username, p)

        elif pilihan == "2" and status == "available":
            if not get_user_verified(username):
                print("❌ Anda belum terverifikasi.")
                input("ENTER...")
                continue
            if username == p["penjual"]:
                print("❌ Tidak bisa mem-booking properti milik sendiri.")
                input("ENTER...")
                continue
            booking(username, p)
            return

        elif pilihan == "3" and status == "booked_owner":
            if ajukan_pembelian(trx):
                print("\n📢 Permintaan pembelian berhasil dikirim.")
            else:
                print("❌ Gagal mengajukan pembelian.")
            input("ENTER...")
            return

        elif pilihan == "4" and status != "sold":
            if username == p["penjual"]:
                print("❌ Tidak bisa menambahkan wishlist properti milik sendiri.")
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
