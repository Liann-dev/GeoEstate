import csv
import os

from app.home.detail_properti import detail_properti
from app.features.transaksi_penjual import sedang_dalam_transaksi

FILE_PROPERTI = "data/properti.csv"
FILE_RIWAYAT = "data/properti_dibeli.csv"


# =========================
# UTIL
# =========================
def to_bool(val):
    return str(val).strip().lower() == "true"


def print_card(p, is_booking=False):
    harga_txt = f"Rp {int(p['harga']):,}".replace(",", ".")
    tersedia = to_bool(p.get("tersedia", "true"))

    if not tersedia:
        status = "❌ TERJUAL"
    elif is_booking:
        status = "⏳ DI-BOOKING"
    else:
        status = "✅ TERSEDIA"

    print(" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']:<10}{status:>20} |")
    print(" +--------------------------------------+")


def get_properti_milik_user(username):
    properti_dimiliki = set()

    if not os.path.exists(FILE_RIWAYAT):
        return properti_dimiliki

    with open(FILE_RIWAYAT, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                properti_dimiliki.add(row["id"])

    return properti_dimiliki


# =========================
# LOAD & FILTER
# =========================
def load_properti():
    if not os.path.exists(FILE_PROPERTI):
        return []

    with open(FILE_PROPERTI, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_properti(
    data,
    username,
    status=None,
    harga_min=None,
    harga_max=None,
    kategori=None
):
    hasil = []

    for p in data:
        harga = int(p["harga"])
        tersedia = to_bool(p.get("tersedia", "true"))
        is_booking = sedang_dalam_transaksi(username, p["id"])

        # FILTER STATUS
        if status == "tersedia" and (not tersedia or is_booking):
            continue
        if status == "dibooking" and not is_booking:
            continue
        if status == "terjual" and tersedia:
            continue

        # FILTER HARGA
        if harga_min is not None and harga < harga_min:
            continue
        if harga_max is not None and harga > harga_max:
            continue

        # FILTER KATEGORI
        if kategori and p["kategori"].lower() != kategori.lower():
            continue

        hasil.append(p)

    return hasil


def sort_properti(data, mode):
    if mode == "1":
        return sorted(data, key=lambda x: int(x["harga"]))
    elif mode == "2":
        return sorted(data, key=lambda x: int(x["harga"]), reverse=True)
    elif mode == "3":
        return sorted(data, key=lambda x: x["nama"].lower())
    return data


def search_properti(data, keyword):
    keyword = keyword.lower()
    return [
        p for p in data
        if keyword in p["nama"].lower()
        or keyword in p["lokasi"].lower()
    ]


# =========================
# MAIN FLOW
# =========================
def pilih_properti(username):
    semua_properti = load_properti()
    properti_milik_user = get_properti_milik_user(username)

    if not semua_properti:
        print("\nBelum ada properti terverifikasi.")
        input("Tekan ENTER...")
        return

    data_tampil = semua_properti

    while True:
        print("\n" * 50)
        print("=========== LIHAT PROPERTI ===========")

        if not data_tampil:
            print("⚠️  Tidak ada properti sesuai filter.")
        else:
            for p in data_tampil:
                is_booking = sedang_dalam_transaksi(username, p["id"])
                print_card(p, is_booking)

        print("-------------------------------------")
        print("[F] Filter Properti")
        print("[S] Sorting")
        print("[C] Cari Properti")
        print("[0] Kembali")
        print("Atau ketik ID Properti untuk melihat detailnya")
        print("-------------------------------------")

        pilihan = input(">> ").strip().lower()

        # KEMBALI
        if pilihan == "0":
            return

        # FILTER
        if pilihan == "f":
            while True:
                print("\nFilter Status:")
                print("1. Tersedia")
                print("2. Di-booking")
                print("3. Terjual")
                print("4. Semua")
                print("0. Batal")
                st = input("Pilih (0-4): ").strip()
                if st in ("0", "1", "2", "3", "4"):
                    break
                print("❌ Pilihan tidak valid.")

            if st == "0":
                continue

            status = {
                "1": "tersedia",
                "2": "dibooking",
                "3": "terjual"
            }.get(st)

            # FILTER HARGA
            while True:
                try:
                    h_min = input("Harga minimum (ENTER jika tidak ada): ").strip()
                    h_max = input("Harga maksimum (ENTER jika tidak ada): ").strip()
                    h_min = int(h_min) if h_min else None
                    h_max = int(h_max) if h_max else None
                    if h_min and h_max and h_min > h_max:
                        raise ValueError
                    break
                except ValueError:
                    print("❌ Input harga tidak valid.")

            # FILTER KATEGORI
            while True:
                print("\nFilter Jenis Properti:")
                print("1. Rumah")
                print("2. Villa")
                print("3. Resort")
                print("4. Semua")
                print("0. Batal")
                kp = input("Pilih (1-4): ").strip()
                if kp in ("0", "1", "2", "3", "4"):
                    break
                print("❌ Pilihan tidak valid.")

            if kp == "0":
                continue

            kategori = {
                "1": "Rumah",
                "2": "Villa",
                "3": "Resort"
            }.get(kp)

            data_tampil = filter_properti(
                semua_properti,
                username=username,
                status=status,
                harga_min=h_min,
                harga_max=h_max,
                kategori=kategori
            )
            continue

        # SORTING
        if pilihan == "s":
            print("\nSorting:")
            print("1. Harga Termurah")
            print("2. Harga Termahal")
            print("3. Nama A-Z")
            mode = input("Pilih: ").strip()
            data_tampil = sort_properti(data_tampil, mode)
            continue

        # SEARCH
        if pilihan == "c":
            keyword = input("Masukkan kata kunci: ").strip()
            if not keyword:
                print("❌ Kata kunci kosong.")
                input("ENTER...")
                continue

            hasil = search_properti(semua_properti, keyword)
            if not hasil:
                print("⚠️ Tidak ditemukan.")
                input("ENTER...")
                continue

            data_tampil = hasil
            continue

        # PILIH ID
        item = next((p for p in data_tampil if p["id"] == pilihan), None)

        if not item:
            print("❌ ID Properti tidak ditemukan.")
            input("ENTER...")
            continue

        if pilihan in properti_milik_user:
            print("❌ Anda sudah memiliki properti ini.")
            input("ENTER...")
            continue

        # ⬇️ TETAP MASUK DETAIL
        detail_properti(username, item)
