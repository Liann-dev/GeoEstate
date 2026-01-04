import csv
import os
from datetime import datetime

FILE_TRANSAKSI = "data/transaksi.csv"
FILE_PROPERTI = "data/properti.csv"
FILE_RIWAYAT = "data/properti_dimiliki.csv"
FILE_SCHEDULE = "data/booking_schedule.csv"


# ================= UTIL =================

def baca_data_csv():
    if not os.path.exists(FILE_TRANSAKSI):
        return []
    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        return list(csv.DictReader(file))


def simpan_perubahan_csv(data_baru):
    fieldnames = [
        'id_transaksi', 'username_pembeli', 'penjual',
        'id_properti', 'nama_properti', 'harga',
        'tanggal', 'transaksi', 'status', 'session'
    ]

    os.makedirs(os.path.dirname(FILE_TRANSAKSI), exist_ok=True)

    with open(FILE_TRANSAKSI, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_baru)


def print_separator(lebar):
    print("-" * lebar)


# ================= SCHEDULE =================

def get_schedule_by_transaksi(id_transaksi):
    if not os.path.exists(FILE_SCHEDULE):
        return "-"
    with open(FILE_SCHEDULE, mode='r', newline='') as file:
        for row in csv.DictReader(file):
            if row['id_transaksi'] == id_transaksi:
                return row['schedule']
    return "-"


def get_jadwal_lama(id_transaksi):
    if not os.path.exists(FILE_SCHEDULE):
        return None
    with open(FILE_SCHEDULE, mode='r', newline='') as file:
        for row in csv.DictReader(file):
            if row['id_transaksi'] == id_transaksi:
                return row['schedule']
    return None


def update_jadwal_booking(id_transaksi, jadwal_baru):
    data = []
    ditemukan = False

    if os.path.exists(FILE_SCHEDULE):
        with open(FILE_SCHEDULE, mode='r', newline='') as file:
            for row in csv.DictReader(file):
                if row['id_transaksi'] == id_transaksi:
                    row['schedule'] = jadwal_baru
                    ditemukan = True
                data.append(row)

    if not ditemukan:
        data.append({
            'id_transaksi': id_transaksi,
            'schedule': jadwal_baru
        })

    with open(FILE_SCHEDULE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id_transaksi', 'schedule'])
        writer.writeheader()
        writer.writerows(data)


# ================= CEK TRANSAKSI AKTIF =================

def sedang_dalam_transaksi(username, id_properti):
    if not os.path.exists(FILE_TRANSAKSI):
        return False

    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get('session') != username:
                continue

            if (
                row.get('username_pembeli') == username
                and row.get('id_properti') == id_properti
            ):
                if row.get('status') not in ("Lunas / Selesai", "Dibatalkan"):
                    return True
    return False


# ================= TAMPILKAN PESANAN =================

def tampilkan_pesanan(penjual_login):
    semua_transaksi = baca_data_csv()

    transaksi_penjual = [
        t for t in semua_transaksi
        if t['session'] == penjual_login and t['transaksi'] == 'booking'
    ]

    print(f"\n=== DAFTAR BOOKING ({penjual_login}) ===")

    if not transaksi_penjual:
        print(">> Tidak ada pesanan masuk.")
        return []

    header = (
        f"| {'ID':<10} | {'Pembeli':<15} | {'Properti':<20} | "
        f"{'Tanggal':<19} | {'Jadwal':<12} | {'Harga':<15} | {'Status':<18} |"
    )
    print_separator(len(header))
    print(header)
    print_separator(len(header))

    for t in transaksi_penjual:
        jadwal = get_schedule_by_transaksi(t['id_transaksi'])
        harga = f"Rp {int(t['harga']):,}".replace(",", ".")
        print(
            f"| {t['id_transaksi']:<10} | {t['username_pembeli']:<15} | "
            f"{t['nama_properti'][:20]:<20} | {t['tanggal']:<19} | "
            f"{jadwal:<12} | {harga:<15} | {t['status']:<18} |"
        )

    print_separator(len(header))
    return transaksi_penjual


# ================= UPDATE STATUS (FIX UTAMA) =================

def update_status_pesanan(penjual_login):
    tampilkan_pesanan(penjual_login)

    id_input = input("\nID Transaksi (ENTER untuk batal): ").strip()
    if not id_input:
        return

    semua_data = baca_data_csv()

    trx_penjual = None
    for row in semua_data:
        if (
            row['id_transaksi'] == id_input
            and row['session'] == penjual_login
        ):
            trx_penjual = row
            break

    if not trx_penjual:
        print(">> Transaksi tidak ditemukan / bukan milik Anda.")
        return

    if trx_penjual['status'] in ("Lunas / Selesai", "Dibatalkan"):
        print(">> Status final, tidak bisa diubah.")
        return

    print("\n1. Konfirmasi (Lunas/Selesai)")
    print("2. Batalkan")
    print("3. Perpanjang Waktu")
    pilihan = input("Pilihan: ")

    status_baru = trx_penjual['status']

    if pilihan == "1":
        status_baru = "Lunas / Selesai"
    elif pilihan == "2":
        status_baru = "Dibatalkan"
    elif pilihan == "3":
        while True:
            jadwal_baru = input("Jadwal baru (YYYY-MM-DD): ").strip()
            try:
                baru = datetime.strptime(jadwal_baru, "%Y-%m-%d")
                lama = get_jadwal_lama(id_input)
                if lama and baru <= datetime.strptime(lama, "%Y-%m-%d"):
                    print(">> Jadwal harus lebih maju.")
                    continue
                update_jadwal_booking(id_input, jadwal_baru)
                status_baru = "Perpanjang Waktu"
                break
            except ValueError:
                print(">> Format salah.")
    else:
        print(">> Batal.")
        return

    # ================= SYNC KE SEMUA SESSION =================
    for row in semua_data:
        if row['id_transaksi'] == id_input:
            row['status'] = status_baru
            
        if pilihan == "1":
            if row['id_transaksi'] == id_input:
                if row['session'] == row['username_pembeli']:
                    row['transaksi'] = "beli"
                if row['session'] == row['penjual']:
                    row['transaksi'] = "jual"
        if pilihan == "2":
            if row['id_transaksi'] == id_input:
                if row['session'] == row['username_pembeli']:
                    row['transaksi'] = "batal"

    simpan_perubahan_csv(semua_data)

    if status_baru == "Lunas / Selesai":
        simpan_ke_riwayat(trx_penjual)

    print(">> Status berhasil diperbarui.")


# ================= SIMPAN RIWAYAT =================

def simpan_ke_riwayat(row):
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE_PROPERTI, mode='r', newline='') as f:
        for p in csv.DictReader(f):
            if p['id'] == row['id_properti']:
                properti = p
                break
        else:
            print(">> Properti tidak ditemukan.")
            return

    data = {
        "id_transaksi": row['id_transaksi'],
        "username": row['username_pembeli'],
        "id": properti['id'],
        "nama": properti['nama'],
        "kategori": properti['kategori'],
        "lokasi": properti['lokasi'],
        "harga": properti['harga'],
        "penjual": properti['penjual'],
        "tanggal": tanggal,
        "transaksi": "beli"
    }

    file_ada = os.path.exists(FILE_RIWAYAT)

    with open(FILE_RIWAYAT, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_ada:
            writer.writeheader()
        writer.writerow(data)

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
