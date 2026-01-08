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


def print_card(p):
    harga_txt = f"Rp {int(p['harga']):,}"
    tersedia = to_bool(p.get('tersedia', 'true'))
    status = "✅ TERSEDIA" if tersedia else "❌ TERJUAL"

    print(f" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']:<10}{status:>20} |")
    print(f" +--------------------------------------+")


def get_properti_milik_user(username):
    properti_dimiliki = set()

    if not os.path.exists(FILE_RIWAYAT):
        return properti_dimiliki

    with open(FILE_RIWAYAT, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                properti_dimiliki.add(row['id'])

    return properti_dimiliki


# =========================
# LOAD & FILTER
# =========================
def load_properti():
    if not os.path.exists(FILE_PROPERTI):
        return []

    data = []
    with open(FILE_PROPERTI, newline='') as file:
        reader = csv.DictReader(file)
        for p in reader:
            data.append(p)

    return data


def filter_properti(data, status=None, harga_min=None, harga_max=None, kategori=None):
    hasil = []

    for p in data:
        harga = int(p['harga'])
        tersedia = to_bool(p.get('tersedia', 'true'))

        if status == "tersedia" and not tersedia:
            continue
        if status == "terjual" and tersedia:
            continue
        if harga_min is not None and harga < harga_min:
            continue
        if harga_max is not None and harga > harga_max:
            continue
        if kategori and p['kategori'].lower() != kategori.lower():
            continue

        hasil.append(p)

    return hasil


def sort_properti(data, mode):
    if mode == "1":      # harga termurah
        return sorted(data, key=lambda x: int(x['harga']))
    elif mode == "2":    # harga termahal
        return sorted(data, key=lambda x: int(x['harga']), reverse=True)
    elif mode == "3":    # nama A-Z
        return sorted(data, key=lambda x: x['nama'].lower())
    return data


def search_properti(data, keyword):
    keyword = keyword.lower()
    hasil = []

    for p in data:
        if keyword in p['nama'].lower() or keyword in p['lokasi'].lower():
            hasil.append(p)

    return hasil


# =========================
# MAIN FLOW
# =========================
def pilih_properti(username):
    semua_properti = load_properti()
    properti_milik_user = get_properti_milik_user(username)

    if not semua_properti:
        print("\nBelum ada properti terverifikasi.")
        input("Tekan ENTER untuk kembali...")
        return

    data_tampil = semua_properti

    while True:
        print("\n" * 50)
        print("=========== LIHAT PROPERTI ===========")

        if not data_tampil:
            print("⚠️  Tidak ada properti sesuai filter.")
        else:
            for p in data_tampil:
                print_card(p)

        print("-------------------------------------")
        print("[F] Filter Properti")
        print("[S] Sorting")
        print("[C] Cari Properti")
        print("[0] Kembali")
        print("Atau ketik ID Properti untuk melihat detailnya")
        print("-------------------------------------")

        pilihan = input(">> ").strip().lower()

        # =====================
        # KEMBALI
        # =====================
        if pilihan == "0":
            return

        # =====================
        # FILTER
        # =====================
        if pilihan == "f":

            # =====================
            # FILTER STATUS
            # =====================
            while True:
                print("\nFilter Status:")
                print("1. Tersedia")
                print("2. Terjual")
                print("3. Semua")
                print("0. Batal")
                st = input("Pilih (0-3): ").strip()

                if st in ("1", "2", "3", "0"):
                    break
                print("❌ Pilihan tidak valid. Masukkan angka 1-3.")

            status = None
            if st == "1":
                status = "tersedia"
            elif st == "2":
                status = "terjual"
            elif st == "0":
                continue

            # =====================
            # FILTER HARGA
            # =====================
            while True:
                print("\nFilter Harga:")
                h_min = input("Harga minimum (ENTER jika tidak ada): ").strip()
                h_max = input("Harga maksimum (ENTER jika tidak ada): ").strip()
                try:
                    h_min = int(h_min) if h_min else None
                    h_max = int(h_max) if h_max else None
                    if h_min is not None and h_max is not None and h_min > h_max:
                        print("❌ Harga minimum tidak boleh lebih besar daripada harga maksimum.")
                        input("Tekan ENTER...")
                        continue
                    break
                except ValueError:
                    print("❌ Harga harus berupa angka.")
                    input("Tekan ENTER...")

            # =====================
            # FILTER JENIS PROPERTI
            # =====================
            while True:
                print("\nFilter Jenis Properti:")
                print("1. Rumah")
                print("2. Villa")
                print("3. Resort")
                print("4. Semua")
                print("0. Batal")
                kp = input("Pilih (1-4): ").strip()

                if kp in ("1", "2", "3", "4", "0"):
                    break
                print("❌ Pilihan tidak valid. Masukkan angka 1-4.")

            kategori = None
            if kp == "1":
                kategori = "Rumah"
            elif kp == "2":
                kategori = "Villa"
            elif kp == "3":
                kategori = "Resort"
            elif kp == "0":
                continue

            # =====================
            # APPLY FILTER
            # =====================
            data_tampil = filter_properti(
                semua_properti,
                status=status,
                harga_min=h_min,
                harga_max=h_max,
                kategori=kategori
            )
            continue


        # =====================
        # SORTING
        # =====================
        if pilihan == "s":
            print("\nSorting:")
            print("1. Harga Termurah")
            print("2. Harga Termahal")
            print("3. Nama A-Z")
            mode = input("Pilih (Langsung klik ENTER untuk batal): ").strip()

            data_tampil = sort_properti(data_tampil, mode)
            continue


        # =====================
        # SEARCH PROPERTI
        # ===================== h_max

        if pilihan == "c":
            keyword = input("Masukkan kata kunci (nama/lokasi): ").strip()

            if not keyword:
                print("❌ Kata kunci tidak boleh kosong.")
                input("Tekan ENTER...")
                continue

            hasil = search_properti(semua_properti, keyword)

            if not hasil:
                print("⚠️ Tidak ditemukan properti dengan kata kunci tersebut.")
                input("Tekan ENTER...")
                continue

            data_tampil = hasil
            continue


        # =====================
        # PILIH ID PROPERTI
        # =====================
        item = next((p for p in data_tampil if p['id'] == pilihan), None)

        if not item:
            print("❌ ID Properti tidak ditemukan.")
            input("Tekan ENTER...")
            continue

        if pilihan in properti_milik_user:
            print("❌ Anda sudah memiliki properti ini.")
            input("Tekan ENTER...")
            continue

        if sedang_dalam_transaksi(username, pilihan):
            print("⏳ Properti sedang dalam transaksi.")
            input("Tekan ENTER...")
            continue

        detail_properti(username, item)
