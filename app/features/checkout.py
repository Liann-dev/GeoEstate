import csv
import os
import datetime
import random

FILE_TRANSAKSI = "data/transaksi.csv"

def simpan_transaksi(username, properti):
    file_exists = os.path.exists(FILE_TRANSAKSI)
    
    with open(FILE_TRANSAKSI, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['id_transaksi', 'username_pembeli', 'penjual', 'id_properti', 'nama_properti', 'harga', 'tanggal', 'transaksi', 'status'])
        

        trc_id = f"GES-{random.randint(1000, 9999)}"
        tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        

        writer.writerow([
            trc_id, 
            username, 
            properti['penjual'],
            properti['id'], 
            properti['nama'], 
            properti['harga'], 
            tanggal,
            "Beli",
            "Menunggu Konfirmasi"
        ])
        return trc_id

def checkout(user_active, properti):
    
    harga_fmt = f"Rp {int(properti['harga']):,}"
    print("\n" * 50)
    print("\n========================================")
    print("           HALAMAN CHECKOUT             ")
    print("========================================")
    print("Rincian Pesanan:")
    print(f"Rumah     : {properti['nama']}")
    print(f"Lokasi    : {properti['lokasi']}")
    print(f"Penjual   : {properti['penjual']}")
    print(f"Harga     : {harga_fmt}")
    print("----------------------------------------")
    print("Biaya Admin : Rp 5,000")
    print(f"Total       : Rp {int(properti['harga']) + 5000:,}")
    print("========================================")
    
    while True:
        confirm = input("Konfirmasi pembelian? (y/n): ").lower()
        
        if confirm == 'y':
            trc_id = simpan_transaksi(user_active, properti)
            
            print("\n[BERHASIL] Pesanan telah dibuat!")
            print(f"ID Transaksi: {trc_id}")
            print("Status saat ini: MENUNGGU KONFIRMASI PENJUAL.")
            print("Silakan cek menu 'Profil Saya' untuk memantau status.")
            input("\nTekan ENTER untuk kembali...")
            break
        if not confirm:
            print("\nPembelian dibatalkan.")
            input("Tekan ENTER untuk kembali...")
            break
        else:
            print("\nPilihan tidak valid!.")
            input("Tekan ENTER untuk coba lagi...\n")
            