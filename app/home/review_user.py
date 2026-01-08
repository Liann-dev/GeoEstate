import csv
import os
from datetime import datetime

# Lokasi File
TRANSAKSI_FILE = "data/transaksi.csv"
REVIEW_FILE = "data/reviews.csv"

def baca_csv(path):
    if os.path.exists(path):
        file = open(path, mode='r')
        reader = csv.DictReader(file)
        data = list(reader)
        file.close()
        return data
    else:
        return []

def tulis_csv(path, fieldnames, data):
    file_exists = os.path.isfile(path)
    file = open(path, mode='a', newline='')
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    writer.writerows(data)
    file.close()

def cek_sudah_review(id_transaksi, username):
    reviews = baca_csv(REVIEW_FILE)
    for row in reviews:
        if row['id_transaksi'] == id_transaksi and row['username_pembeli'] == username:
            return True
    return False

def cari_transaksi_valid(username, id_transaksi):
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row["id_transaksi"] == id_transaksi
                and row.get("session") == username
                and row["status"] == "Lunas / Selesai"
                and row["transaksi"] == "beli"
            ):
                return row
    return None
  
# Perbaikan: Parameter diganti jadi 'username' (string)
def proses_input_ulasan(username, transaksi):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== TULIS ULASAN ===")
    print("Properti  : " + transaksi['nama_properti'])
    print("Seller    : " + transaksi['penjual'])
    print("-" * 40)

    # Validasi Rating
    rating = 0
    while True:
        input_angka = input("Beri Bintang (1-5) dan (0 untuk keluar): ")
        if input_angka.isdigit():
            angka = int(input_angka)
            if angka >= 1 and angka <= 5:
                rating = angka
                break
            elif input_angka == '0':
                return
            else:
                print("❌ Harap masukkan angka 1 sampai 5.")
        else:
            print("❌ Input harus berupa angka.")

    komentar = input("Tuliskan pengalaman transaksi Anda (ENTER untuk keluar): ")

    if not komentar:
        return
    
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simpan ke CSV
    review_baru = [{
        'id_transaksi': transaksi['id_transaksi'],
        'reviewer': username,           # <-- PERBAIKAN: Langsung pakai variabel string
        'seller': transaksi['penjual'],
        'id_properti': transaksi['id_properti'],
        'rating': rating,
        'komentar': komentar,
        'tanggal': waktu
    }]
    
    header = ['id_transaksi', 'reviewer', 'seller', 'id_properti', 'rating', 'komentar', 'tanggal']
    tulis_csv(REVIEW_FILE, header, review_baru)
    
    print("\n✅ Ulasan berhasil disimpan!")
    input("Tekan Enter untuk kembali...")

# Perbaikan: Parameter diganti jadi 'username' (string)
def user_review(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== RIWAYAT PEMBELIAN SAYA ===")

        semua_transaksi = baca_csv(TRANSAKSI_FILE)

        # ================= FILTER DATA =================
        my_history = [
            trx for trx in semua_transaksi
            if (
                trx.get('session') == username
            )
        ]

        if not my_history:
            print("\nAnda belum memiliki riwayat pembelian properti.")
            input("\nTekan Enter untuk kembali...")
            break

        # ================= TABEL =================
        COL_NO = 3
        COL_ID = 12
        COL_TGL = 12
        COL_NAMA = 22
        COL_STATUS = 20

        print("-" * 100)
        print(
            f"{'No':<{COL_NO}} | "
            f"{'ID Transaksi':<{COL_ID}} | "
            f"{'Tanggal':<{COL_TGL}} | "
            f"{'Nama Properti':<{COL_NAMA}} | "
            f"{'Status':<{COL_STATUS}} | "
            f"Keterangan"
        )
        print("-" * 100)

        nomor = 1
        for trx in my_history:
            tgl_pendek = trx['tanggal'][0:10]
            id_transaksi = trx['id_transaksi']
            status = trx['status']

            info_review = ""

            if "Lunas" in status or "Selesai" in status:
                if cek_sudah_review(trx['id_transaksi'], username):
                    info_review = "✅ Sudah Diulas"
                else:
                    info_review = "⭐ BISA DIULAS"
            elif "Batal" in status or "Dibatalkan" in status:
                info_review = "-"
            else:
                info_review = "⏳ Menunggu"

            print(
            f"{nomor:<{COL_NO}} | "
            f"{id_transaksi:<{COL_ID}} | "
            f"{tgl_pendek:<{COL_TGL}} | "
            f"{trx['nama_properti']:<{COL_NAMA}} | "
            f"{status:<{COL_STATUS}} | "
            f"{info_review}"
)

            nomor += 1

        print("-" * 100)

        # ================= MENU =================
        print("\nOpsi:")
        print("[No] Beri Ulasan Transaksi (Ketik 1, 2, dst.)")
        print("[L]  Lihat Ulasan Saya")
        print("[0]  Kembali")

        pilihan = input(">> Pilihan Anda: ").strip()

        # ================= KELUAR =================
        if pilihan == '0':
            break

        # ================= LIHAT ULASAN =================
        if pilihan.upper() == 'L':
            print("\n=== ULASAN PEMBELIAN SAYA ===\n")

            reviews = []
            if os.path.exists(REVIEW_FILE):
                with open(REVIEW_FILE, "r", encoding="utf-8", newline="") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get("username_pembeli") == username:
                            reviews.append(row)

            if not reviews:
                print("Belum ada ulasan.")
                input("\nTekan ENTER untuk kembali...")
                continue

            for i, r in enumerate(reviews, start=1):
                print(f"[{i}]")
                print(f"🧾 ID Transaksi : {r['id_transaksi']}")
                print(f"🏠 ID Properti  : {r['id_properti']}")
                print(f"👤 Penjual      : {r['penjual']}")
                print(f"⭐ Rating       : {r['rating']} / 5")
                print(f"💬 Ulasan       : {r['review_text']}")
                print(f"🕒 Tanggal      : {r['tanggal_review']}")
                print("-" * 40)

            input("Tekan ENTER untuk kembali...")
            continue

        # ================= INPUT ULASAN =================
        if not pilihan.isdigit():
            print("\n❌ Masukkan nomor yang valid.")
            input("Tekan Enter...")
            continue

        index = int(pilihan) - 1
        if index < 0 or index >= len(my_history):
            print("\n❌ Nomor tidak ditemukan.")
            input("Tekan Enter...")
            continue

        trx_pilih = my_history[index]

        trx_valid = cari_transaksi_valid(
            username,
            trx_pilih['id_transaksi']
        )

        if not trx_valid:
            print("\n❌ Transaksi ini tidak memenuhi syarat untuk diulas.")
            input("Tekan Enter...")
            continue

        if cek_sudah_review(trx_valid['id_transaksi'], username):
            print("\n❌ Transaksi ini sudah Anda ulas.")
            input("Tekan Enter...")
            continue

        # ✅ FINAL: proses ulasan
        proses_input_ulasan(username, trx_valid)
