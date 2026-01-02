import csv
import os

# Lokasi file (Semuanya CSV)
FILE_WISHLIST = "data/wishlist.csv"
FILE_PROPERTI = "data/properti.csv" 

def to_bool_wl(val):
    return str(val).strip().lower() == "true"

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
    tersedia = str(p.get('tersedia', 'true')).strip().lower() == "true"
    status = "✅ TERSEDIA" if tersedia else "❌ TERJUAL"

    print(f" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']:<10}{status:>20} |")
    print(f" +--------------------------------------+")

def sinkron_wishlist_dengan_properti(username):
    if not os.path.exists(FILE_PROPERTI):
        return

    semua_properti = {}
    with open(FILE_PROPERTI, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for p in reader:
            semua_properti[p['id']] = p.get('tersedia', 'true').lower()

    wishlist = muat_csv()
    data_baru = [
        item for item in wishlist
        if semua_properti.get(item['id_properti'], 'false') == 'true'
    ]

    if len(data_baru) != len(wishlist):
        simpan_csv(data_baru)

def wishlist_kosong(username):
    data_wishlist = muat_csv()
    for item in data_wishlist:
        if item['username'] == username:
            return False
    return True

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
    properti_valid = []

    for p in semua_properti:
        if (
            p['doc_verified'].strip().lower() == "true"
            and p.get('tersedia', 'true').strip().lower() == "true"
        ):
            print_card_alt(p)
            properti_valid.append(p)

    if not properti_valid:
        print("Belum ada properti yang tersedia saat ini.")
        input("Tekan ENTER untuk kembali...\n")

    return properti_valid


def tambah_ke_wishlist(username, id_properti):
    id_properti_str = str(id_properti)

    # 🔎 Cek properti di properti.csv
    properti_valid = None
    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for p in reader:
                if (
                    p['id'] == id_properti_str
                    and p['doc_verified'].strip().lower() == "true"
                    and p.get('tersedia', 'true').strip().lower() == "true"
                ):
                    properti_valid = p
                    break

    # ❌ Jika properti tidak valid / terjual
    if not properti_valid:
        print("\n❌ ID Properti tidak ditemukan.")
        input("Tekan ENTER untuk kembali...\n")
        return

    # 📥 Load wishlist
    data_wishlist = muat_csv()

    # ❤️ Cek duplikasi
    for item in data_wishlist:
        if item['username'] == username and item['id_properti'] == id_properti_str:
            print("\nProperti ini sudah ada di Wishlist Anda!")
            input("Tekan ENTER untuk kembali...\n")
            return

    # ✅ Simpan ke wishlist
    data_wishlist.append({
        "username": username,
        "id_properti": id_properti_str
    })

    simpan_csv(data_wishlist)
    print("\n✅ Properti berhasil disimpan ke Wishlist!")
    input("Tekan ENTER untuk kembali...\n")

def lihat_wishlist(username):
    list_wishlist = muat_csv()

    id_milik_gue = [
        item['id_properti']
        for item in list_wishlist
        if item['username'] == username
    ]

    # 1️⃣ Wishlist benar-benar kosong
    if not id_milik_gue:
        print("\n--- Wishlist Anda Masih Kosong ---")
        return

    # Ambil properti
    with open(FILE_PROPERTI, mode='r', newline='') as f:
        semua_properti = list(csv.DictReader(f))

    print(f"\n=== WISHLIST {username.upper()} ===")

    ada_yang_tersedia = False
    id_tersedia = set()

    for prop in semua_properti:
        if prop['id'] in id_milik_gue:
            tersedia = str(prop.get('tersedia', 'true')).lower() == "true"

            if tersedia:
                print(f"- [ID: {prop['id']}] {prop['nama']} | Rp {prop['harga']}")
                print(f"  Lokasi: {prop['lokasi']}")
                ada_yang_tersedia = True
                id_tersedia.add(prop['id'])

    # 2️⃣ Semua wishlist TERJUAL → auto clean
    if not ada_yang_tersedia:
        print("Semua properti di wishlist Anda sudah terjual.")

        # 🔥 Hapus semua wishlist milik user
        data_baru = [
            item for item in list_wishlist
            if item['username'] != username
        ]
        simpan_csv(data_baru)
        return 

def hapus_dari_wishlist(username, id_properti):
    data_wishlist = muat_csv()
    id_hapus_str = str(id_properti)

    # Cek apakah ID ada di wishlist user
    ada = any(
        item['username'] == username and item['id_properti'] == id_hapus_str
        for item in data_wishlist
    )

    if not ada:
        print("\n❌ ID Properti tidak ditemukan di Wishlist Anda.")
        input("Tekan ENTER...\n")
        return

    data_baru = [
        item for item in data_wishlist
        if not (item['username'] == username and item['id_properti'] == id_hapus_str)
    ]

    simpan_csv(data_baru)
    print("\n✅ Properti berhasil dihapus dari Wishlist.")
    input("Tekan ENTER...\n")


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
2. Hapus Properti dari Wishlist
0. Kembali\n
""")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_wishlist(username)
            input("Tekan ENTER untuk kembali...\n")

        elif pilihan == "2":

            # 🚫 Wishlist masih kosong
            if wishlist_kosong(username):
                print("\n--- Wishlist Anda Masih Kosong ---")
                print("Tidak ada properti yang bisa dihapus.")
                input("Tekan ENTER untuk kembali...\n")
                continue

            lihat_wishlist(username)

            if wishlist_kosong(username):
                print("\n--- Wishlist Anda Masih Kosong ---")
                print("Tidak ada properti yang bisa dihapus.")
                input("Tekan ENTER untuk kembali...\n")
                continue

            id_properti = input("Masukkan ID Properti yang ingin dihapus dari Wishlist [ENTER untuk batal]: ").strip()
            if not id_properti:
                continue
            
            hapus_dari_wishlist(username, id_properti)

        elif pilihan == "0":
            return

        else:
            print("Pilihan tidak valid!")
