import csv
import os

FILE_TRANSAKSI = "data/transaksi.csv"
FILE_SCHEDULE = "data/booking_schedule.csv"

def hapus_jadwal(username, id_transaksi):
    if not os.path.exists(FILE_SCHEDULE):
        return

    data_baru = []
    terhapus = False

    with open(FILE_SCHEDULE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        for row in reader:
            if (
                row['id_transaksi'] == id_transaksi
                and row.get('session') == username
            ):
                terhapus = True
                continue  # skip baris ini
            data_baru.append(row)

    if not terhapus:
        return

    with open(FILE_SCHEDULE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_baru)

def hapus_transaksi(username, id_transaksi):
    if not os.path.exists(FILE_TRANSAKSI):
        print("File transaksi tidak ditemukan.")
        return False

    semua_data = []
    target = None
    milik_user = False

    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            semua_data.append(row)

            if (
                row['id_transaksi'] == id_transaksi
                and row.get('session') == username
            ):
                target = row

                if (
                    row['transaksi'] in ('booking, beli')
                    and row['username_pembeli'] == username
                ) or (
                    row['transaksi'] in ('booking, jual')
                    and row['penjual'] == username
                ):
                    milik_user = True

    if not target:
        print("ID Transaksi tidak ditemukan di riwayat Anda.")
        return False

    if not milik_user:
        print("❌ Anda tidak berhak menghapus transaksi ini.")
        return False

    if target['status'] in ('Menunggu Konfirmasi', 'Perpanjang Waktu'):
        print("❌ Transaksi yang belum selesai tidak dapat dihapus.")
        return False

    # ================= HAPUS RIWAYAT TRANSAKSI (SESSION USER) =================
    data_baru = [
        row for row in semua_data
        if not (
            row['id_transaksi'] == id_transaksi
            and row.get('session') == username
        )
    ]

    with open(FILE_TRANSAKSI, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=semua_data[0].keys())
        writer.writeheader()
        writer.writerows(data_baru)

    hapus_jadwal(username, id_transaksi)
    
    print("✅ Riwayat transaksi berhasil dihapus.")
    return True

# ======================================================
# RIWAYAT TRANSAKSI (SESSION-BASED)
# ======================================================
def history_transaksi(username):

    print("\n" * 50)
    print("==============================================================")
    print("                   📜 RIWAYAT TRANSAKSI                       ")
    print("==============================================================")

    if not os.path.exists(FILE_TRANSAKSI):
        print("\n   [INFO] Belum ada data transaksi apapun di sistem.")
        input("Tekan ENTER untuk kembali...")
        return

    my_history = []
    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 🔥 FILTER UTAMA: SESSION
            if (row.get('session') == username
            and row.get('transaksi') in ('beli, jual, booking')
            ):
                my_history.append(row)

    if not my_history:
        print("\n   [INFO] Kamu belum pernah melakukan transaksi.")
        print("   Yuk, cari properti impianmu sekarang!")
        input("Tekan ENTER untuk kembali...")
        return

    # ================= TABEL RIWAYAT =================
    print("-" * 100)
    print(f" {'ID':<8} |{'TRANSAKSI':<10} | {'TANGGAL':<12} | {'NAMA PROPERTI':<20} | {'HARGA':<20} | {'STATUS':<15}")
    print("-" * 100)

    for trx in my_history:
        idt = trx['id_transaksi']

        # Tentukan jenis transaksi
        if trx['transaksi'] == 'beli':
            transaksi = "Beli"
        elif trx['transaksi'] == 'jual':
            transaksi = "Jual"
        elif trx['transaksi'] == 'booking' and trx['username_pembeli'] == username:
            transaksi = "Beli"
        elif trx['transaksi'] == 'booking' and trx['penjual'] == username:
            transaksi = "Jual"

        tgl_short = trx['tanggal'].split(' ')[0]

        nama_display = (
            trx['nama_properti'][:17] + '..'
            if len(trx['nama_properti']) > 17
            else trx['nama_properti']
        )


        harga_display = f"Rp {int(trx['harga']):,}"
        status_icon = {
            "Menunggu Konfirmasi": "⏳ Menunggu",
            "Perpanjang Waktu": "⏰ Diperpanjang",
            "Lunas / Selesai": "✅ Selesai",
            "Dibatalkan": "❌ Dibatalkan"
        }.get(trx['status'], trx['status'])

        print(
            f" {idt:<8} | {transaksi:<9} | {tgl_short:<12} | "
            f"{nama_display:<20} | {harga_display:<20} | {status_icon}"
        )

    print("=" * 100)
    print(f" Total Transaksi: {len(my_history)}")

    # ================= OPSI =================
    print("\n[ OPSI ]")
    print("1. 🗑️  Hapus Riwayat Transaksi")
    print("0. 🔙 Kembali")

    while True:
        pilihan = input(">> Pilih opsi: ")
        if pilihan == '1':
            id_pilih = input("Pilih ID Transaksi yang ingin dihapus (Tekan ENTER untuk kembali): ").strip()
            if not id_pilih:
                return
            hapus_transaksi(username, id_pilih)
            input("Tekan ENTER untuk kembali...")
            return

        elif pilihan == '0':
            return
        else:
            print("Pilihan tidak valid.")
