import csv
import os
from datetime import datetime

REVIEW_FILE = "data/reviews.csv"
TRANSAKSI_FILE = "data/transaksi.csv"


def baca_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def simpan_csv(path, data_baru, append=True):
    file_ada = os.path.exists(path)
    mode = "a" if append and file_ada else "w"

    with open(path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data_baru[0].keys())
        if not file_ada or not append:
            writer.writeheader()
        writer.writerows(data_baru)


# =========================
# CEK SUDAH REVIEW
# =========================
def cek_sudah_review(id_transaksi, username):
    reviews = baca_csv(REVIEW_FILE)
    for r in reviews:
        if r.get("id_transaksi") == id_transaksi and r.get("username_pembeli") == username:
            return True
    return False


# =========================
# CARI TRANSAKSI VALID
# =========================
def cari_transaksi_valid(username, id_transaksi):
    transaksi = baca_csv(TRANSAKSI_FILE)
    for t in transaksi:
        if (
            t["id_transaksi"] == id_transaksi
            and t["session"] == username
            and t["status"] == "Sold"
        ):
            return t
    return None


# =========================
# INPUT ULASAN
# =========================
def proses_input_ulasan(username, id_transaksi):
    trx = cari_transaksi_valid(username, id_transaksi)

    if not trx:
        print("\n❌ Transaksi tidak valid atau belum selesai.")
        input("ENTER...")
        return

    if cek_sudah_review(id_transaksi, username):
        print("\n⚠️ Kamu sudah memberi ulasan untuk transaksi ini.")
        input("ENTER...")
        return

    print("\n=== FORM ULASAN ===")
    print(f"ID Transaksi : {id_transaksi}")
    print(f"Properti     : {trx['nama_properti']}")
    print(f"Seller       : {trx['penjual']}")

    while True:
        try:
            rating = int(input("Rating (1-5): "))
            if 1 <= rating <= 5:
                break
            print("Masukkan angka 1–5.")
        except ValueError:
            print("Rating harus angka.")

    komentar = input("Komentar      : ")

    review_baru = [{
        "id_transaksi": id_transaksi,
        "username_pembeli": username,
        "penjual": trx["penjual"],
        "id_properti": trx["id_properti"],
        "rating": str(rating),
        "review_text": komentar,
        "tanggal_review": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }]

    simpan_csv(REVIEW_FILE, review_baru, append=True)

    print("\n✅ Ulasan berhasil disimpan.")
    input("ENTER...")


# =========================
# LIHAT ULASAN SAYA
# =========================
def lihat_ulasan_saya(username):
    reviews = baca_csv(REVIEW_FILE)
    data = [r for r in reviews if r["username_pembeli"] == username]

    if not data:
        print("\n📭 Kamu belum punya ulasan.")
        input("ENTER...")
        return

    print("\n=== ULASAN SAYA ===\n")
    for i, r in enumerate(data, 1):
        print(f"[{i}] ID Transaksi : {r['id_transaksi']}")
        print(f"⭐ Rating       : {r['rating']}/5")
        print(f"💬 Komentar     : {r['review_text']}")
        print(f"🕒 Tanggal      : {r['tanggal_review']}")
        print("-" * 40)

    input("ENTER...")


# =========================
# LIHAT ULASAN SELLER
# =========================
def lihat_ulasan_seller(username_seller):
    reviews = baca_csv(REVIEW_FILE)
    data = [r for r in reviews if r["penjual"] == username_seller]

    if not data:
        print(f"\n📭 Seller '{username_seller}' belum punya ulasan.")
        input("ENTER...")
        return

    print(f"\n=== ULASAN SELLER: {username_seller} ===\n")
    for i, r in enumerate(data, 1):
        print(f"[{i}] ID Transaksi : {r['id_transaksi']}")
        print(f"⭐ Rating       : {r['rating']}/5")
        print(f"💬 Ulasan       : {r['review_text']}")
        print(f"🕒 Tanggal      : {r['tanggal_review']}")
        print("-" * 40)

    input("ENTER...")


# =========================
# RATING SELLER
# =========================
def rating_seller(username_seller):
    reviews = baca_csv(REVIEW_FILE)
    ratings = [int(r["rating"]) for r in reviews if r["penjual"] == username_seller]

    if not ratings:
        return "Belum ada ulasan"

    avg = sum(ratings) / len(ratings)
    return f"{avg:.1f}/5 dari {len(ratings)} ulasan"
