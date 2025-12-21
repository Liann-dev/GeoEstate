import csv
import os

# Lokasi file (Semuanya CSV)
FILE_WISHLIST = "data/wishlist.csv"
FILE_PROPERTI = "data/properti.csv" 

def muat_csv():
    if os.path.exists(FILE_WISHLIST):
        data = []
        with open(FILE_WISHLIST, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    else:
        return []

def simpan_csv(data):
    fieldnames = ['username', 'id_properti'] 
    
    with open(FILE_WISHLIST, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def print_card_alt(p):
    harga_txt = f"Rp {int(p['harga']):,}" 
    print(f" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']} {' '*30}|")
    print(f" +--------------------------------------+")

def lihat_properti_alt(username):
    if not os.path.exists(FILE_PROPERTI):
        print("Belum ada data properti.")
        return []

    semua_properti = []
    with open(FILE_PROPERTI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for p in reader:
            semua_properti.append(p)

    print("\n=== Properti Tersedia ===")
    properti_terverifikasi = []

    for p in semua_properti:
        if p['doc_verified'].strip().lower() == "true":
            print_card_alt(p)
            properti_terverifikasi.append(p)

    if not properti_terverifikasi:
        print("Belum ada properti yang terverifikasi saat ini.")
        input("Tekan ENTER untuk kembali...\n")

    return properti_terverifikasi

def tambah_ke_wishlist(username, id_properti):
    data_wishlist = muat_csv()
    id_properti_str = str(id_properti)

    for item in data_wishlist:
        if item['username'] == username and item['id_properti'] == id_properti_str:
            print("\nProperti ini sudah ada di Wishlist Anda!")
            input("Tekan ENTER untuk kembali...\n")
            return

    data_baru = {
        "username": username,
        "id_properti": id_properti_str
    }
    
    data_wishlist.append(data_baru)
    simpan_csv(data_wishlist)
    print("\nProperti berhasil disimpan ke Wishlist!")
    input("Tekan ENTER untuk kembali...\n")

def lihat_wishlist_gue(username):
    list_wishlist = muat_csv()

    id_milik_gue = []
    for item in list_wishlist:
        if item['username'] == username:
            id_milik_gue.append(item['id_properti']) 
    
    if not id_milik_gue:
        print("\n--- Wishlist Anda Masih Kosong ---")
        input("Tekan ENTER untuk kembali...\n")
        return

    semua_properti = []
    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                semua_properti.append(row)
    else:
        print(f"\n[ERROR] File database properti tidak ditemukan di: {FILE_PROPERTI}")
        print("Pastikan Anda sudah membuat file 'data/properti.csv'!")
        input("Tekan ENTER untuk kembali...\n")
        return

    print(f"\n=== WISHLIST {username.upper()} ===")
    ketemu = False
    
    for prop in semua_properti:
        if prop['id'] in id_milik_gue:
            nama = prop.get('nama', 'Tanpa Nama')
            harga = prop.get('harga', '0')
            lokasi = prop.get('lokasi', '-')
            
            print(f"- [ID: {prop['id']}] {nama} | Rp {harga}")
            print(f"   Lokasi: {lokasi}")
            ketemu = True
            
    if not ketemu:
        print("Data properti yang Anda simpan tidak ditemukan di database utama.")
        input("Tekan ENTER untuk kembali...\n")

def hapus_dari_wishlist(username, id_properti):
    data_wishlist = muat_csv()
    id_hapus_str = str(id_properti)
    
    data_baru = [
        item for item in data_wishlist 
        if not (item['username'] == username and item['id_properti'] == id_hapus_str)
    ]
    
    if len(data_baru) == len(data_wishlist):
        print("\nID Properti tidak ditemukan di wishlist Anda.")
        input("Tekan ENTER untuk kembali...\n")
        
    else:
        simpan_csv(data_baru)
        print("\nProperti dihapus dari Wishlist.")
        input("Tekan ENTER untuk kembali...\n")

def cek_status_love(username, id_properti):
    #Mengecek apakah user sudah me-love properti ini
    data_wishlist = muat_csv()
    id_str = str(id_properti)
    
    for item in data_wishlist:
        if item['username'] == username and item['id_properti'] == id_str:
            return True # Sudah di-love
    return False # Belum di-love

def menu_wishlist(username):
    while True:
        print(f"""
=== MENU WISHLIST ({username}) ===
1. Lihat Wishlist
2. Tambah Properti ke Wishlist
3. Hapus Properti dari Wishlist
4. Kembali
""")
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            lihat_wishlist_gue(username)
            input("\nTekan ENTER untuk kembali...\n")

        elif pilihan == "2":
            lihat_properti_alt(username)
            while True:
                id_properti = input("Masukkan ID Properti yang ingin ditambahkan ke Wishlist: ")
                if not id_properti:
                    print("ID Properti tidak boleh kosong!\n")
                else:
                    break
            if cek_status_love(username, id_properti):
                print("\nProperti ini sudah ada di Wishlist Anda!")
                input("Tekan ENTER untuk kembali...\n")
            else:
                tambah_ke_wishlist(username, id_properti)

        elif pilihan == "3":
            lihat_wishlist_gue(username)
            while True:
                id_properti = input("Masukkan ID Properti yang ingin dihapus dari Wishlist: ")
                if not id_properti:
                    print("ID Properti tidak boleh kosong!\n")
                else:
                    break
            hapus_dari_wishlist(username, id_properti)

        elif pilihan == "4":
            break

        else:
            print("[ERROR] Pilihan tidak valid, silakan pilih antara 1-4.")
