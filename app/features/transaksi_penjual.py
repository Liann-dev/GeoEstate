import csv
import os
from datetime import datetime

FILE_TRANSAKSI = "data/transaksi.csv"
FILE_PROPERTI = "data/properti.csv"
FILE_RIWAYAT = "data/properti_dimiliki.csv"
FILE_SCHEDULE = "data/booking_schedule.csv"

def get_schedule_by_transaksi(id_transaksi):
    if not os.path.exists(FILE_SCHEDULE):
        return "-"

    with open(FILE_SCHEDULE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id_transaksi'] == id_transaksi:
                return row['schedule']

    return "-"

def sedang_dalam_transaksi(username, id_properti):
    if not os.path.exists(FILE_TRANSAKSI):
        return False

    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (
                row['username_pembeli'] == username
                and row['id_properti'] == id_properti
                and row['status'] not in ["Lunas / Selesai", "Dibatalkan"]
            ):
                return True

    return False

def baca_data_csv():
    transaksi_list = []
    if os.path.exists(FILE_TRANSAKSI):
        with open(FILE_TRANSAKSI, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaksi_list.append(row)
    return transaksi_list

def simpan_perubahan_csv(data_baru):
    fieldnames = ['id_transaksi', 'username_pembeli', 'penjual', 'id_properti', 'nama_properti', 'harga', 'tanggal', 'transaksi', 'status',]
    
    os.makedirs(os.path.dirname(FILE_TRANSAKSI), exist_ok=True)
    
    with open(FILE_TRANSAKSI, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_baru)

def print_separator(lebar):
    print("-" * lebar)

def get_jadwal_lama(id_transaksi):
    if not os.path.exists(FILE_SCHEDULE):
        return None

    with open(FILE_SCHEDULE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id_transaksi'] == id_transaksi:
                return row['schedule']
    return None

def update_jadwal_booking(id_transaksi, jadwal_baru):
    data = []
    ditemukan = False

    # Jika file belum ada, buat baru
    if not os.path.exists(FILE_SCHEDULE):
        with open(FILE_SCHEDULE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id_transaksi', 'schedule'])
            writer.writeheader()

    # Baca data lama
    with open(FILE_SCHEDULE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id_transaksi'] == id_transaksi:
                row['schedule'] = jadwal_baru
                ditemukan = True
            data.append(row)

    # Jika belum ada jadwal untuk transaksi ini, tambahkan
    if not ditemukan:
        data.append({
            'id_transaksi': id_transaksi,
            'schedule': jadwal_baru
        })

    # Simpan kembali
    with open(FILE_SCHEDULE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id_transaksi', 'schedule'])
        writer.writeheader()
        writer.writerows(data)

def tampilkan_pesanan(penjual_login):
  
    semua_transaksi = baca_data_csv()
    
    transaksi_milik_penjual = [t for t in semua_transaksi if t['penjual'] == penjual_login]

    print(f"\n=== DAFTAR BOOKING (Penjual: {penjual_login}) ===")
    
    if not transaksi_milik_penjual:
        print(f">> Tidak ada pesanan masuk untuk akun '{penjual_login}'.")
       
        return [] 

    header = (
    f"| {'ID Trx':<10} | {'Pembeli':<15} | {'Properti':<20} | "
    f"{'Tanggal Pesan':<19} | {'Jadwal':<12} | {'Harga':<20} | {'Status':<20} |"
    )
    lebar_tabel = len(header)

    print_separator(lebar_tabel)
    print(header)
    print_separator(lebar_tabel)

    for t in transaksi_milik_penjual:
        try:
            harga_int = int(t['harga'])
            harga_fmt = f"Rp {harga_int:,}".replace(",", ".")
            jadwal = get_schedule_by_transaksi(t['id_transaksi'])
            tanggal_pesan = t.get("tanggal", "-")
        except ValueError:
            harga_fmt = t['harga']

        print(
    f"| {t['id_transaksi']:<10} | "
    f"{t['username_pembeli']:<15} | "
    f"{t['nama_properti'][:20]:<20} | "
    f"{tanggal_pesan:<19} | "
    f"{jadwal:<12} | "
    f"{harga_fmt:<20} | "
    f"{t['status']:<20} |"
    )

    print_separator(lebar_tabel)
    
    return transaksi_milik_penjual

def update_status_pesanan(penjual_login):
    data_filtered = tampilkan_pesanan(penjual_login)
    
    if not data_filtered:
        return

    print("\n--- Update Status Booking ---")
    id_input = input("Masukkan ID Transaksi (contoh: GES-1234) (Tekan ENTER untuk kembali): ")
    
    if not id_input:
        return
    
    semua_data = baca_data_csv()
    found = False
    
    for row in semua_data:

        if row['id_transaksi'] == id_input:
            

            if row['penjual'] != penjual_login:
                print(">> ERROR: Transaksi ini bukan milik Anda! Akses ditolak.")
                return 

            found = True

            if row['status'] in ["Lunas / Selesai", "Dibatalkan"]:
                print(f"\n>> Transaksi ini sudah berstatus '{row['status']}'.")
                print(">> Status final tidak dapat diubah kembali.")
                return
        
            print(f"\nItem Ditemukan: {row['nama_properti']}")
            print(f"Pembeli       : {row['username_pembeli']}")
            print(f"Status Saat Ini: {row['status']}")
            
            print("\nPilih Status Baru:")
            if row['status'] == "Perpanjang Waktu":
                print("1. Konfirmasi (Lunas/Selesai)")
                print("2. Tolak / Batalkan")
                print("\n>> Mohon untuk segera menyelesaikan transaksi")
            else:
                print("1. Konfirmasi (Lunas/Selesai)")
                print("2. Tolak / Batalkan")
                print("3. Perpanjang Waktu")
            
            pilihan = input("Pilihan: ")
            status_baru = row['status'] 

            if row['status'] == "Perpanjang Waktu":
                if pilihan == "1":
                    status_baru = "Lunas / Selesai"
                elif pilihan == "2":
                    status_baru = "Dibatalkan"
                else:
                    print(">> Pilihan tidak valid. Batal update.")
                    return
            else:
                if pilihan == "1":
                    status_baru = "Lunas / Selesai"
                elif pilihan == "2":
                    status_baru = "Dibatalkan"
                elif pilihan == "3":
                    print("\n--- Perpanjang Waktu Booking ---")
                    while True:
                        jadwal_baru = input("Masukkan jadwal baru (YYYY-MM-DD) (ENTER untuk batal): ").strip()

                        if not jadwal_baru:
                            return

                        jadwal_lama = get_jadwal_lama(row['id_transaksi'])

                        try:
                            tanggal_baru = datetime.strptime(jadwal_baru, "%Y-%m-%d")
                        except ValueError:
                            print(">> Format tanggal tidak valid!\n")
                            continue

                        if jadwal_lama:
                            tanggal_lama = datetime.strptime(jadwal_lama, "%Y-%m-%d")
                            if tanggal_baru <= tanggal_lama:
                                print(">> Jadwal baru harus lebih maju dari jadwal sebelumnya.\n")
                                continue
                        break

                    update_jadwal_booking(row['id_transaksi'], jadwal_baru)
                    status_baru = "Perpanjang Waktu"

                else:
                    print(">> Pilihan tidak valid. Batal update.")
                    return

            row['status'] = status_baru

            if status_baru == "Lunas / Selesai":
                simpan_ke_riwayat(row)
            
            simpan_perubahan_csv(semua_data)
            if status_baru == "Lunas / Selesai":
                print(f"\n>> Berhasil! Transaksi {id_input} telah lunas.")
                break
            elif status_baru == "Dibatalkan":
                print(f"\n>> Berhasil! Transaksi {id_input} telah dibatalkan.")
                break
    
    if not found:
        print(">> ID Transaksi tidak ditemukan di database Anda.")

def simpan_ke_riwayat(row_transaksi):
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Cari data properti
    properti = None
    with open(FILE_PROPERTI, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for p in reader:
            if p['id'] == row_transaksi['id_properti']:
                properti = p
                break

    if not properti:
        print(">> ERROR: Data properti tidak ditemukan.")
        return

    data_riwayat = {
        "id_transaksi": row_transaksi['id_transaksi'],
        "username": row_transaksi['username_pembeli'],
        "id": properti['id'],
        "nama": properti['nama'],
        "kategori": properti['kategori'],
        "lokasi": properti['lokasi'],
        "harga": properti['harga'],
        "penjual": properti['penjual'],
        "doc_verified": properti['doc_verified'],
        "tanggal": tanggal,
        "transaksi" : 'Beli'
    }

    file_ada = os.path.exists(FILE_RIWAYAT)

    with open(FILE_RIWAYAT, mode='a', newline='') as file:
        fieldnames = [
            "id_transaksi", "username", "id", "nama", "kategori",
            "lokasi", "harga", "penjual", "doc_verified", "tanggal", "transaksi"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_ada:
            writer.writeheader()

        writer.writerow(data_riwayat)

def menu_kelola_pesanan(user_active):
   
    while True:
        print(f"\n=== MENU KELOLA DATA BOOKING ({user_active}) ===")
        print("1. Lihat Data Booking")
        print("2. Update Status Booking") 
        print("0. Kembali")
        
        pil = input(">> Pilih menu: ")
        
        if pil == "1":
            tampilkan_pesanan(user_active)
            input("Tekan Enter untuk lanjut...")
        elif pil == "2":
            update_status_pesanan(user_active)
            input("Tekan Enter untuk lanjut...")
        elif pil == "0":
            break
        else:
            print(">> Pilihan salah.")
