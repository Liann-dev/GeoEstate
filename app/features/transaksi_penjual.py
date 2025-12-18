import csv
import os

FILE_TRANSAKSI = "data/transaksi.csv"

def baca_data_csv():
    transaksi_list = []
    if os.path.exists(FILE_TRANSAKSI):
        with open(FILE_TRANSAKSI, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaksi_list.append(row)
    return transaksi_list

def simpan_perubahan_csv(data_baru):
    fieldnames = ['id_transaksi', 'username_pembeli', 'penjual', 'id_properti', 'nama_properti', 'harga', 'tanggal', 'status']
    
    os.makedirs(os.path.dirname(FILE_TRANSAKSI), exist_ok=True)
    
    with open(FILE_TRANSAKSI, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_baru)

def print_separator(lebar):
    print("-" * lebar)

def tampilkan_pesanan(penjual_login):
  
    semua_transaksi = baca_data_csv()
    
    transaksi_milik_penjual = [t for t in semua_transaksi if t['penjual'] == penjual_login]

    print(f"\n=== DAFTAR PESANAN MASUK (Penjual: {penjual_login}) ===")
    
    if not transaksi_milik_penjual:
        print(f">> Tidak ada pesanan masuk untuk akun '{penjual_login}'.")
       
        return [] 

    header = f"| {'ID Trx':<10} | {'Pembeli':<15} | {'Properti':<20} | {'Harga':<15} | {'Status':<20} |"
    lebar_tabel = len(header)

    print_separator(lebar_tabel)
    print(header)
    print_separator(lebar_tabel)

    for t in transaksi_milik_penjual:
        try:
            harga_int = int(t['harga'])
            harga_fmt = f"Rp {harga_int:,}".replace(",", ".")
        except ValueError:
            harga_fmt = t['harga']

        print(f"| {t['id_transaksi']:<10} | {t['username_pembeli']:<15} | {t['nama_properti'][:20]:<20} | {harga_fmt:<15} | {t['status']:<20} |")
    
    print_separator(lebar_tabel)
    
    return transaksi_milik_penjual

def update_status_pesanan(penjual_login):
    data_filtered = tampilkan_pesanan(penjual_login)
    
    if not data_filtered:
        return

    print("\n--- Update Status Pesanan ---")
    id_input = input("Masukkan ID Transaksi (contoh: GES-1234): ")
    
    semua_data = baca_data_csv()
    found = False
    
    for row in semua_data:

        if row['id_transaksi'] == id_input:
            

            if row['penjual'] != penjual_login:
                print(">> ERROR: Transaksi ini bukan milik Anda! Akses ditolak.")
                return 

            found = True
            print(f"\nItem Ditemukan: {row['nama_properti']}")
            print(f"Pembeli       : {row['username_pembeli']}")
            print(f"Status Saat Ini: {row['status']}")
            
            print("\nPilih Status Baru:")
            print("1. Konfirmasi (Lunas/Selesai)")
            print("2. Tolak / Batalkan")
            print("3. Pending / Menunggu")
            
            pilihan = input("Pilihan (1-3): ")
            status_baru = row['status'] 

            if pilihan == "1":
                status_baru = "Lunas / Selesai"
            elif pilihan == "2":
                status_baru = "Dibatalkan"
            elif pilihan == "3":
                status_baru = "Menunggu Konfirmasi"
            else:
                print(">> Pilihan tidak valid. Batal update.")
                return

            row['status'] = status_baru
            
            simpan_perubahan_csv(semua_data)
            print(f">> Berhasil! Status transaksi {id_input} diubah menjadi '{status_baru}'.")
            break
    
    if not found:
        print(">> ID Transaksi tidak ditemukan di database Anda.")

def menu_kelola_pesanan(user_active):
   
    while True:
        print(f"\n=== MENU KELOLA PESANAN ({user_active}) ===")
        print("1. Lihat Pesanan Saya")
        print("2. Update Status Pesanan")
        print("0. Kembali")
        
        pil = input(">> Pilih menu: ")
        
        if pil == "1":
            tampilkan_pesanan(user_active)
            input("\nTekan Enter untuk lanjut...")
        elif pil == "2":
            update_status_pesanan(user_active)
            input("\nTekan Enter untuk lanjut...")
        elif pil == "0":
            break
        else:
            print(">> Pilihan salah.")
