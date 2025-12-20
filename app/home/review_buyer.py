import csv
import os
from datetime import datetime

TRANSAKSI_FILE = "data/transaksi.csv"
REVIEW_FILE = "data/reviews.csv"


def init_review_file():
    if not os.path.exists(REVIEW_FILE):
        with open(REVIEW_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id_transaksi",
                "username_pembeli",
                "penjual",
                "id_properti",
                "rating",
                "review_text",
                "tanggal_review"
            ])
            f.write("\n")


def get_valid_transaction(username, id_transaksi):
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row["id_transaksi"] == id_transaksi and
                row["username_pembeli"] == username and
                row["status"] == "Lunas / Selesai"
            ):
                return row
    return None


def already_reviewed(id_transaksi, username):
    if not os.path.exists(REVIEW_FILE):
        return False

    with open(REVIEW_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row["id_transaksi"] == id_transaksi and
                row["username_pembeli"] == username
            ):
                return True
    return False

def tampilkan_transaksi_selesai(username):
    print("\n========================================")
    print("   TRANSAKSI SELESAI YANG BISA DIREVIEW  ")
    print("========================================\n")

    ditemukan = False

    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            if (
                row["username_pembeli"] == username and
                row["status"] == "Lunas / Selesai"
            ):
                print(f"{i}. 🧾 {row['id_transaksi']} | 🏠 {row['nama_properti']}")
                ditemukan = True

    if not ditemukan:
        print("⚠️  Tidak ada transaksi selesai yang bisa direview.")

    print("\n----------------------------------------")

def buyer_review(username):
    init_review_file()

    while True:
        print("\n=== MENU REVIEW BUYER ===")
        print("1. Tambah Review")
        print("2. Lihat Review Saya")
        print("3. Kembali")

        pilihan = input("Pilih menu: ")

        # =============================
        # TAMBAH REVIEW
        # =============================
        if pilihan == "1":
            tampilkan_transaksi_selesai(username)
            id_transaksi = input("Masukkan ID Transaksi: ")

            trx = get_valid_transaction(username, id_transaksi)
            if not trx:
                print("❌ Transaksi tidak valid atau belum selesai.")
                input("Tekan ENTER untuk kembali...")
                continue

            if already_reviewed(id_transaksi, username):
                print("❌ Transaksi ini sudah direview sebelumnya.")
                input("Tekan ENTER untuk kembali...")
                continue

            rating = int(input("Rating (1-5): "))
            review_text = input("Ulasan: ")

            with open(REVIEW_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    trx["id_transaksi"],
                    username,
                    trx["penjual"],
                    trx["id_properti"],
                    rating,
                    review_text,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])

            print("✅ Review berhasil ditambahkan!")
            input("Tekan ENTER untuk kembali...")

        # =============================
        # LIHAT REVIEW SAYA
        # =============================
        elif pilihan == "2":
            print("\n========================================")
            print("            REVIEW SAYA                 ")
            print("========================================\n")

            reviews = []

            with open(REVIEW_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["username_pembeli"] == username:
                        reviews.append(row)

            if not reviews:
                print("⚠️  Belum ada review.")
                input("\nTekan ENTER untuk kembali...")
                continue

            for i, review in enumerate(reviews, start=1):
                print(f"[{i}]")
                print(f"🧾 ID Transaksi  : {review['id_transaksi']}")
                print(f"🏠 ID Properti   : {review['id_properti']}")
                print(f"👤 Penjual       : {review['penjual']}")
                print(f"⭐ Rating        : {review['rating']} / 5")
                print(f"💬 Ulasan        : {review['review_text']}")
                print(f"🕒 Tanggal      : {review['tanggal_review']}")
                print("\n----------------------------------------\n")

            input("Tekan ENTER untuk kembali...")

        elif pilihan == "3":
            break