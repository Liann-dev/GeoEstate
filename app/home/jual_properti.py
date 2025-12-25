import csv
import os
import datetime
import random

FILE_RIWAYAT = "data/properti_dimiliki.csv"
FILE_TRANSAKSI = "data/transaksi.csv"

def simpan_transaksi_jual(username_penjual, riwayat):
    file_exists = os.path.exists(FILE_TRANSAKSI)

    with open(FILE_TRANSAKSI, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                'id_transaksi', 'username_pembeli', 'penjual',
                'id_properti', 'nama_properti', 'harga',
                'tanggal', 'transaksi', 'status'
            ])

        trc_id = f"GES-{random.randint(1000, 9999)}"
        tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow([
            trc_id,
            riwayat['penjual'],   # PEMBELI BARU (pemilik setelah jual)
            username_penjual,     # PENJUAL (pemilik sebelum jual)
            riwayat['id'],
            riwayat['nama'],
            riwayat['harga'],
            tanggal,
            "Jual",
            "Lunas / Selesai"
        ])

    return trc_id

def jual_kembali_properti(username):
    if not os.path.exists(FILE_RIWAYAT):
        print("\nBelum ada riwayat transaksi.")
        input("Tekan ENTER untuk kembali...")
        return

    semua_data = []
    with open(FILE_RIWAYAT, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            semua_data.append(row)

    milik_user = [row for row in semua_data if row['username'] == username]

    if not milik_user:
        print("\nAnda tidak memiliki properti untuk dijual kembali.")
        input("Tekan ENTER untuk kembali...")
        return

    print("\n=== PROPERTI YANG BISA DIJUAL KEMBALI ===")
    for row in milik_user:
        print("-" * 50)
        print(f"ID Transaksi : {row['id_transaksi']}")
        print(f"Nama         : {row['nama']}")
        print(f"Lokasi       : {row['lokasi']}")
        print(f"Harga        : Rp {int(row['harga']):,}")
        print(f"Tanggal Beli : {row['tanggal']}")
        print(f"Pemilik Lama : {row['penjual']}")

    print("-" * 50)
    id_input = input("Masukkan ID Transaksi (ENTER untuk batal): ").strip()
    if not id_input:
        return

    riwayat = next(
        (row for row in milik_user if row['id_transaksi'] == id_input),
        None
    )

    if not riwayat:
        print("\n❌ ID Transaksi tidak valid atau bukan milik Anda.")
        input("Tekan ENTER untuk kembali...")
        return

    # 🔥 Hapus dari kepemilikan sekarang
    riwayat_baru = [row for row in semua_data if row['id_transaksi'] != id_input]

    with open(FILE_RIWAYAT, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=semua_data[0].keys())
        writer.writeheader()
        writer.writerows(riwayat_baru)

    # 🔥 Catat transaksi jual ke pemilik lama
    trc_id = simpan_transaksi_jual(username, riwayat)

    print("\n✅ Properti berhasil dijual kembali ke pemilik sebelumnya.")
    print(f"ID Transaksi Jual: {trc_id}")
    input("Tekan ENTER untuk kembali...")