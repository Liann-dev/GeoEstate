import csv
import os
from app.home.detail_properti import detail_properti
from app.home.review_user import proses_input_ulasan, cek_sudah_review

TRANSAKSI_FILE = "data/transaksi.csv"
REVIEW_FILE = "data/reviews.csv"
PROPERTI_FILE = "data/properti.csv"


def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_properti_by_id(id_properti):
    for p in load_csv(PROPERTI_FILE):
        if p["id"] == id_properti:
            return p
    return None


def status_keterangan(trx, username):
    status = trx["status"]

    if status == "Menunggu Konfirmasi":
        return "⏳ Menunggu Seller"
    if status == "Booked":
        return "📅 Booking / Proses"
    if status == "Menunggu Pembayaran":
        return "⏳ Menunggu Konfirmasi Beli"
    if status == "Sold":
        if cek_sudah_review(trx["id_transaksi"], username):
            return "✅ Sudah Diulas"
        return "⭐ Bisa Diulas"
    if "Batal" in status:
        return "❌ Dibatalkan"

    return "-"


def riwayat_transaksi_terpadu(username):
    transaksi = [
        t for t in load_csv(TRANSAKSI_FILE)
        if t.get("session") == username
    ]

    if not transaksi:
        print("\n📭 Belum ada transaksi.")
        input("ENTER...")
        return

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== RIWAYAT TRANSAKSI SAYA ===\n")

        # ===== TABEL =====
        print("-" * 100)
        print(
            f"{'No':<3} | {'ID Transaksi':<12} | {'Properti':<25} | "
            f"{'Status':<20} | Keterangan"
        )
        print("-" * 100)

        for i, trx in enumerate(transaksi, 1):
            ket = status_keterangan(trx, username)
            print(
                f"{i:<3} | {trx['id_transaksi']:<12} | "
                f"{trx['nama_properti']:<25} | "
                f"{trx['status']:<20} | {ket}"
            )

        print("-" * 100)
        print("\n[No] Pilih Transaksi")
        print("[U]  Lihat Ulasan Saya")
        print("[0]  Kembali")

        pilihan = input("Pilih: ").strip()

        # ===== KELUAR =====
        if pilihan == "0":
            return

        # ===== LIHAT ULASAN =====
        if pilihan.upper() == "U":
            print("\n📭 Kamu belum punya ulasan.")
            input("ENTER...")
            continue

        # ===== VALIDASI ANGKA =====
        if not pilihan.isdigit():
            print("\n❌ Input tidak valid.")
            input("ENTER...")
            continue

        nomor = int(pilihan)
        if nomor < 1 or nomor > len(transaksi):
            print("\n❌ Nomor transaksi tidak tersedia.")
            input("ENTER...")
            continue

        trx = transaksi[nomor - 1]
        status = trx["status"]

        # ===== REDIRECT =====
        if status in ("Menunggu Konfirmasi", "Booked", "Menunggu Pembayaran"):
            p = get_properti_by_id(trx["id_properti"])
            if p:
                detail_properti(username, p)
            else:
                print("\n❌ Data properti tidak ditemukan.")
                input("ENTER...")
            continue

        if status == "Sold":
            if cek_sudah_review(trx["id_transaksi"], username):
                tampilkan_detail_review(trx["id_transaksi"])
            else:
                proses_input_ulasan(username, trx)
            continue

        print("\nℹ️ Tidak ada aksi untuk transaksi ini.")
        input("ENTER...")


def tampilkan_detail_review(id_transaksi):
    reviews = load_csv(REVIEW_FILE)
    for r in reviews:
        if r["id_transaksi"] == id_transaksi:
            print("\n=== ULASAN TRANSAKSI ===")
            print(f"⭐ Rating  : {r['rating']}/5")
            print(f"💬 Ulasan : {r['komentar']}")
            print(f"🕒 Tanggal: {r['tanggal']}")
            input("ENTER...")
            return
