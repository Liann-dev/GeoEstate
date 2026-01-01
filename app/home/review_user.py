import csv
import os
from datetime import datetime

# Lokasi File
TRANSAKSI_FILE = "data/transaksi.csv"
REVIEWS_FILE = "data/reviews.csv"

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

def cek_sudah_review(transaksi_id):
    reviews = baca_csv(REVIEWS_FILE)
    sudah_ada = False
    for row in reviews:
        if row['id_transaksi'] == transaksi_id:
            sudah_ada = True
            break
    return sudah_ada

# Perbaikan: Parameter diganti jadi 'username' (string)
def proses_input_ulasan(username, transaksi):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== TULIS ULASAN ===")
    print("Properti : " + transaksi['nama_properti'])
    print("Seller   : " + transaksi['penjual'])
    print("-" * 40)

    # Validasi Rating
    rating = 0
    while True:
        input_angka = input("Beri Bintang (1-5): ")
        if input_angka.isdigit():
            angka = int(input_angka)
            if angka >= 1 and angka <= 5:
                rating = angka
                break
            else:
                print("❌ Harap masukkan angka 1 sampai 5.")
        else:
            print("❌ Input harus berupa angka.")

    komentar = input("Tulis komentar Anda: ")
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
    tulis_csv(REVIEWS_FILE, header, review_baru)
    
    print("\n✅ Ulasan berhasil disimpan!")
    input("Tekan Enter untuk kembali...")

# Perbaikan: Parameter diganti jadi 'username' (string)
def history_transaksi(username):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== [H] RIWAYAT PEMBELIAN SAYA ===")
        
        semua_transaksi = baca_csv(TRANSAKSI_FILE)
        
        # 1. Filter: Ambil transaksi milik user ini saja
        my_history = []
        for trx in semua_transaksi:
            # Perbaikan: Langsung bandingkan dengan string 'username'
            if trx['username_pembeli'] == username: 
                my_history.append(trx)

        if len(my_history) == 0:
            print("\nAnda belum memiliki riwayat pembelian properti.")
            input("\nTekan Enter untuk kembali...")
            break

        # 2. Tampilkan Tabel
        print("-" * 95)
        print(f"{'No':<3} | {'Tanggal':<11} | {'Nama Properti':<20} | {'Status':<18} | {'Keterangan'}")
        print("-" * 95)

        nomor = 1
        for trx in my_history:
            tgl_pendek = trx['tanggal'][0:10] 
            status = trx['status']
            
            info_review = ""
            
            if "Lunas" in status or "Selesai" in status:
                if cek_sudah_review(trx['id_transaksi']):
                    info_review = "✅ Sudah Diulas"
                else:
                    info_review = "⭐ BISA DIULAS"
            elif "Batal" in status or "Dibatalkan" in status:
                info_review = "-"
            else:
                info_review = "⏳ Menunggu"

            print(f"{nomor:<3} | {tgl_pendek:<11} | {trx['nama_properti']:<20} | {status:<18} | {info_review}")
            nomor = nomor + 1
        
        print("-" * 95)
        
        print("\nOpsi:")
        print("[0] Kembali ke Menu Utama")
        print("[No] Masukkan Nomor Urut (1, 2, dst) untuk memberi ulasan.")
        
        pilihan = input(">> Pilihan Anda: ")

        if pilihan == '0':
            break 
        
        if pilihan.isdigit():
            index = int(pilihan) - 1
            if index >= 0 and index < len(my_history):
                transaksi_pilih = my_history[index]
                status_trx = transaksi_pilih['status']
                
                if "Lunas" in status_trx or "Selesai" in status_trx:
                    if cek_sudah_review(transaksi_pilih['id_transaksi']):
                        print("\n❌ Transaksi ini sudah Anda ulas sebelumnya!")
                        input("Tekan Enter...")
                    else:
                        # Perbaikan: Kirim 'username' (string)
                        proses_input_ulasan(username, transaksi_pilih)
                else:
                    print("\n❌ Hanya transaksi yang LUNAS/SELESAI yang boleh diulas.")
                    input("Tekan Enter...")
            else:
                print("\n❌ Nomor tidak ditemukan dalam daftar.")
                input("Tekan Enter...")
        else:
            print("\n❌ Masukkan angka nomor urut yang benar.")
            input("Tekan Enter...")