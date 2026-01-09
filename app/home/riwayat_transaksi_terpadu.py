import csv
import os
from app.home.detail_properti import detail_properti
from app.home.review_user import proses_input_ulasan, cek_sudah_review, lihat_ulasan_seller

TRANSAKSI_FILE = "data/transaksi.csv"
REVIEW_FILE = "data/reviews.csv"
PROPERTI_FILE = "data/properti.csv"
FILE_BOOKING = "data/booking.csv"

def get_tanggal_booking_terakhir(id_transaksi):
    if not os.path.exists(FILE_BOOKING):
        return None

    terakhir = None
    with open(FILE_BOOKING, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["id_transaksi"] == id_transaksi:
                terakhir = r["tanggal"]
    return terakhir

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

    if status == "Booked":
        tgl = get_tanggal_booking_terakhir(trx["id_transaksi"])
        if tgl:
            return f"⏳ Berlaku hingga {tgl}"
        return "Dalam Masa Booking"

    if status == "Menunggu Pembayaran":
        return "💰 Menunggu Konfirmasi Pembelian"

    if status == "Sold":
        if cek_sudah_review(trx["id_transaksi"], username):
            return "✅ Sudah Diulas"
        return "⭐ Bisa Diulas"

    if "Batal" in status:
        return "❌ Dibatalkan"

    return "-"


def label_status(status):
    if status == "Booked":
        return "Booking"
    if status == "Menunggu Pembayaran":
        return "Menunggu Pembayaran"
    if status == "Sold":
        return "Selesai"
    if "Batal" in status:
        return "Dibatalkan"
    return status


def riwayat_transaksi_terpadu(username):
    prioritas = {"Booked": 3, "Menunggu Pembayaran": 2, "Sold": 1, "Menunggu Konfirmasi": 0}

    while True:
        semua = load_csv(TRANSAKSI_FILE)
        transaksi_map = {}

        for trx in semua:
            if trx.get("session") != username:
                continue

            id_trx = trx["id_transaksi"]
            if id_trx not in transaksi_map or prioritas.get(trx["status"], 0) > prioritas.get(transaksi_map[id_trx]["status"], 0):
                transaksi_map[id_trx] = trx

        transaksi = list(transaksi_map.values())

        if not transaksi:
            print("\n📭 Belum ada transaksi.")
            input("ENTER...")
            return

        os.system("cls" if os.name == "nt" else "clear")
        print("\n=== RIWAYAT TRANSAKSI SAYA ===\n")
        print("-" * 100)
        print(f"{'No':<3} | {'ID Transaksi':<12} | {'Properti':<25} | {'Status':<20} | Keterangan")
        print("-" * 100)

        for i, trx in enumerate(transaksi, 1):
            print(f"{i:<3} | {trx['id_transaksi']:<12} | {trx['nama_properti']:<25} | {label_status(trx['status']):<20} | {status_keterangan(trx, username)}")

        print("-" * 100)
        print("\n[No] Pilih Transaksi")
        print("[U]  Lihat Ulasan Saya")
        print("[0]  Kembali")
        pilihan = input("Pilih: ").strip()

        if pilihan == "0":
            return

        if pilihan.upper() == "U":
            from app.home.review_user import lihat_ulasan_saya
            lihat_ulasan_saya(username)
            continue

        if not pilihan.isdigit():
            print("\n❌ Input tidak valid.")
            input("ENTER...")
            continue

        idx = int(pilihan)
        if idx < 1 or idx > len(transaksi):
            print("\n❌ Nomor transaksi tidak tersedia.")
            input("ENTER...")
            continue

        trx = transaksi[idx - 1]

        # Jika transaksi sudah Sold dan bisa diulas → masuk menu review
        if trx["status"] == "Sold" and not cek_sudah_review(trx["id_transaksi"], username):
            print(f"\n⭐ Memberikan ulasan untuk seller '{trx['penjual']}'")
            proses_input_ulasan(username, trx["id_transaksi"])
            # setelah selesai ulas, langsung tampilkan review seller
            lihat_ulasan_seller(trx["penjual"])
        else:
            p = get_properti_by_id(trx["id_properti"])
            if p:
                detail_properti(username, p)
            else:
                print("\n❌ Data properti tidak ditemukan.")
                input("ENTER...")
