import csv
import os

REVIEW_FILE = "data/reviews.csv"

def seller_review(username):
    print("\n========================================")
    print("        ULASAN MENGENAI ANDA             ")
    print("========================================\n")

    if not os.path.exists(REVIEW_FILE):
        print("⚠️  Belum ada review.")
        input("\nTekan ENTER untuk kembali...")
        return

    with open(REVIEW_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reviews = [row for row in reader if row["penjual"] == username]

    if not reviews:
        print("⚠️  Belum ada review untuk properti Anda.")
        input("\nTekan ENTER untuk kembali...")
        return

    for i, review in enumerate(reviews, start=1):
        print(f"[{i}]")
        print(f"🧾 ID Transaksi  : {review['id_transaksi']}")
        print(f"👤 Nama Pembeli  : {review['username_pembeli']}")
        print(f"💲 Nama Penjual  : {review['penjual']}")
        print(f"🏠 ID Properti   : {review['id_properti']}")
        print(f"⭐ Rating        : {review['rating']} / 5")
        print(f"💬 Ulasan        : {review['review_text']}")
        print(f"🕒 Tanggal       : {review['tanggal_review']}")
        print("\n----------------------------------------\n")

    input("Tekan ENTER untuk kembali...")