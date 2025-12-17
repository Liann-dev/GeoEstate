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

def tambah_ke_wishlist(username, id_properti):
    data_wishlist = muat_csv()
    id_properti_str = str(id_properti)
    

    for item in data_wishlist:
        if item['username'] == username and item['id_properti'] == id_properti_str:
            print("\n[INFO] Properti ini sudah ada di Wishlist Anda!")
            return

    data_baru = {
        "username": username,
        "id_properti": id_properti_str
    }
    
    data_wishlist.append(data_baru)
    simpan_csv(data_wishlist)
    print("\n[SUKSES] Properti berhasil disimpan ke Wishlist (CSV)!")

def lihat_wishlist_gue(username):
    list_wishlist = muat_csv()

    id_milik_gue = []
    for item in list_wishlist:
        if item['username'] == username:
            id_milik_gue.append(item['id_properti']) 
    
    if not id_milik_gue:
        print("\n--- Wishlist Anda Masih Kosong ---")
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
        return

    print(f"\n=== WISHLIST {username.upper()} ===")
    ketemu = False
    
    for prop in semua_properti:
        if prop['id'] in id_milik_gue:
            nama = prop.get('nama_rumah', 'Tanpa Nama')
            harga = prop.get('harga', '0')
            lokasi = prop.get('lokasi', '-')
            
            print(f"- [ID: {prop['id']}] {nama} | Rp {harga}")
            print(f"   Lokasi: {lokasi}")
            ketemu = True
            
    if not ketemu:
        print("Data properti yang Anda simpan tidak ditemukan di database utama.")

def hapus_dari_wishlist(username, id_properti):
    data_wishlist = muat_csv()
    id_hapus_str = str(id_properti)
    
    data_baru = [
        item for item in data_wishlist 
        if not (item['username'] == username and item['id_properti'] == id_hapus_str)
    ]
    
    if len(data_baru) == len(data_wishlist):
        print("\n[Gagal] ID Properti tidak ditemukan di wishlist Anda.")
    else:
        simpan_csv(data_baru)
        print("\n[SUKSES] Properti dihapus dari Wishlist.")

def cek_status_love(username, id_properti):
    #Mengecek apakah user sudah me-love properti ini
    data_wishlist = muat_csv()
    id_str = str(id_properti)
    
    for item in data_wishlist:
        if item['username'] == username and item['id_properti'] == id_str:
            return True # Sudah di-love
    return False # Belum di-love

