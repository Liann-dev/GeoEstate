import csv
import os
import time
import random
from datetime import datetime
from app.features.notifikasi_service import tambah_notifikasi

FILE_JADWAL = 'data/jadwal_survey.csv'

def init_csv():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists(FILE_JADWAL):
        with open(FILE_JADWAL, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(['id', 'id_properti', 'nama_properti', 'lokasi', 'tanggal', 'waktu', 'pembeli', 'penjual', 'status'])

def simpan_jadwal_csv(data_jadwal):
    init_csv()
    
    with open(FILE_JADWAL, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            data_jadwal['id'],
            data_jadwal['id_properti'],
            data_jadwal['nama_properti'],
            data_jadwal['lokasi'],
            data_jadwal['tanggal'],
            data_jadwal['waktu'],
            data_jadwal['pembeli'],
            data_jadwal['penjual'],
            data_jadwal['status']
        ])

def ui_sukses_request(id_survei):

    print("\n" * 50)
    print("========================================")
    print("          PERMINTAAN TERKIRIM           ")
    print("========================================")
    print("          (  ⏳  )                      ") 
    print("                                        ")
    print(" Permintaan Jadwal Survei Berhasil!     ")
    print(" Sedang menunggu konfirmasi penjual...  ")
    print("----------------------------------------")
    print(f" ID Survei: #{id_survei}               ")
    print(f" Status:    🟨 Pending Review           ")
    print("========================================")
    input("[ Tekan ENTER untuk kembali ke Home ]")

def survey(username, properti):
    print("\n" * 50)
    print("========================================")
    print("         JADWALKAN SURVEI              ")
    print("========================================")
    print(f" 🏠 {properti['nama']}")
    print(f" 📍 {properti['lokasi']}")
    print("----------------------------------------")
    
    print("\n[ Pilih Tanggal ]")
    print("Format: YYYY-MM-DD (Contoh: 2025-12-20)")
    
    tanggal_input = ""
    while True:
        tanggal_input = input(">> Masukkan Tanggal (0 untuk kembali): ")
        
        if tanggal_input == '0':
            return

        parts = tanggal_input.split('-')
        if len(parts) != 3:
            print("❌ Format salah! Gunakan Tahun-Bulan-Tanggal (YYYY-MM-DD).")
            continue
        
        tahun_str, bulan_str, hari_str = parts

        if not (tahun_str.isdigit() and bulan_str.isdigit() and hari_str.isdigit()):
            print("❌ Input harus berupa angka dengan pemisah strip (-).")
            continue

        tahun = int(tahun_str)
        bulan = int(bulan_str)
        hari = int(hari_str)

        if bulan < 1 or bulan > 12:
            print("❌ Bulan tidak valid (Harus 1-12).")
            continue

        hari_per_bulan = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if bulan == 2:
            if (tahun % 4 == 0 and tahun % 100 != 0) or (tahun % 400 == 0):
                hari_per_bulan[2] = 29
        
        if hari < 1 or hari > hari_per_bulan[bulan]:
            print(f"❌ Tanggal tidak valid! Bulan {bulan} hanya memiliki {hari_per_bulan[bulan]} hari.")
            continue

        tanggal_obj = datetime(tahun, bulan, hari).date()
        tanggal_sekarang = datetime.now().date()

        if tanggal_obj < tanggal_sekarang:
            print("❌ Tanggal tidak boleh di masa lalu!")
            continue

        break

    print("\n[ Pilih Waktu ]")
    print("Waktu yang tersedia agent:")
    print("1. 🕘 09:00")
    print("2. 🕐 13:00")
    print("3. 🕓 16:00")
    
    waktu_pilih = ""
    while True:
        opsi_waktu = input(">> Pilih waktu (1/2/3) (0 untuk kembali): ")
        if opsi_waktu == '1':
            waktu_pilih = "09:00"
            break
        elif opsi_waktu == '2':
            waktu_pilih = "13:00"
            break
        elif opsi_waktu == '3':
            waktu_pilih = "16:00"
            break
        elif opsi_waktu == '0':
            return
        else:
            print("❌ Pilihan tidak valid.")
            input("Tekan ENTER untuk coba lagi...")
 
    print("----------------------------------------")
    konfirmasi = input("Konfirmasi Jadwal? (y/n): ").lower()
    
    if konfirmasi == 'y':
       
        srv_id = f"SRV-{random.randint(1000, 9999)}"
        
        data_baru = {
            'id': srv_id,
            'id_properti': properti['id'],
            'nama_properti': properti['nama'],
            'lokasi': properti['lokasi'],
            'tanggal': tanggal_input,
            'waktu': waktu_pilih,
            'pembeli': username,
            'penjual': properti['penjual'],
            'status': 'Pending',
            'extend_count': 0
        }
        
        simpan_jadwal_csv(data_baru)
        tambah_notifikasi(
            properti["penjual"],
            f"📅 Permintaan survei baru untuk properti '{properti['nama']}' dari buyer {username}",
            role="seller",
            redirect="survey_seller"
        )
        ui_sukses_request(srv_id)

    else:
        print("Pembuatan jadwal dibatalkan.")
        time.sleep(1)

STATUS_PRIORITY = {
    "berlangsung": 2,
    "pending": 1
}

def lihat_jadwal_survey(username):
    init_csv()

    print("\n" * 50)
    print("========================================")
    print("          JADWAL SURVEI ANDA           ")
    print("========================================")

    surveys = {}

    with open(FILE_JADWAL, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['pembeli'] != username:
                continue

            sid = row['id']
            status = row['status'].lower()

            if status not in STATUS_PRIORITY:
                continue  # abaikan status selesai / ditolak dll

            if sid not in surveys:
                surveys[sid] = row
            else:
                old_status = surveys[sid]['status'].lower()
                if STATUS_PRIORITY[status] > STATUS_PRIORITY.get(old_status, 0):
                    surveys[sid] = row

    if not surveys:
        print(" (Belum ada jadwal survei aktif) ")
        input("[ Tekan ENTER untuk kembali ]")
        return

    for row in surveys.values():
        print(f" ID Survei   : {row['id']}")
        print(f" Properti    : {row['nama_properti']}")
        print(f" Lokasi      : {row['lokasi']}")
        print(f" Tanggal     : {row['tanggal']}")
        print(f" Waktu       : {row['waktu']}")
        print(f" Penjual     : {row['penjual']}")
        print(f" Status      : {row['status']}")
        print("----------------------------------------")

    input("[ Tekan ENTER untuk kembali ]")
