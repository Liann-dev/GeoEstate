import csv
import os

FILE_TRANSAKSI = "data/transaksi.csv"

def history_transaksi(username):

    print("\n" * 50)
    print("==============================================================")
    print("                   📜 RIWAYAT PEMBELIAN                       ")
    print("==============================================================")

    if not os.path.exists(FILE_TRANSAKSI):
        print("\n   [INFO] Belum ada data transaksi apapun di sistem.")
        print("\n==============================================================")
        input("Tekan ENTER untuk kembali...")
        return

    my_history = []
    with open(FILE_TRANSAKSI, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
           
            if row['username_pembeli'] == username:
                my_history.append(row)


    if not my_history:
        print("\n   [INFO] Kamu belum pernah melakukan transaksi.")
        print("   Yuk, cari properti impianmu sekarang!")
        print("\n==============================================================")
    else:
      
        print(f" {'Penjual':<12} | {'TANGGAL':<12} | {'NAMA PROPERTI':<20} | {'HARGA':<13} | {'STATUS'}" )
        print(" " + "-" * 60)

        for trx in my_history:
            penjual = trx['penjual']
            tgl_short = trx['tanggal'].split(' ')[0]

            nama_display = (trx['nama_properti'][:17] + '..') if len(trx['nama_properti']) > 17 else trx['nama_properti']
            
            harga_display = f"Rp {int(trx['harga']):,}"

            raw_status = trx['status']
            if raw_status == 'Berhasil':
                status_icon = "✅ Berhasil"
            elif raw_status == 'Menunggu Konfirmasi':
                status_icon = "⏳ Menunggu"
            elif raw_status == 'Ditolak':
                status_icon = "❌ Ditolak"
            else:
                status_icon = raw_status

            print(f" {penjual:<12} | {tgl_short:<12} | {nama_display:<20} | {harga_display:<13} | {status_icon}")

        print("\n==============================================================")
        print(f" Total Transaksi: {len(my_history)}")


    print("\n[ OPSI ]")
    print("0. 🔙 Kembali")
    
    while True:
        pilihan = input(">> Pilih opsi: ")
        if pilihan == '0':
            return
        else:
            print("Pilihan tidak valid.")