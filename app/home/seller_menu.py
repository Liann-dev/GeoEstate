import csv
import os


from app.Utils.animation import loading_exit_seller
from app.features.transaksi_penjual import menu_kelola_pesanan
from app.features.kelola_survey import menu_kelola_survei
from app.home.review_seller import seller_review

FILE_PROPERTI = "data/properti.csv"

def tambah_properti(username):
    print("\n--- Tambah Properti Baru ---")
    
    print("Pilih kategori properti:")
    print("1. Rumah")
    print("2. Villa")
    print("3. Resort")
    kategori_pilihan = input("Masukkan pilihan (1/2/3) [ENTER untuk batal]: ").strip()
    if not kategori_pilihan:
        return

    if kategori_pilihan == "1":
        kategori = "Rumah"
    elif kategori_pilihan == "2":
        kategori = "Villa"
    elif kategori_pilihan == "3":
        kategori = "Resort"
    else:
        print("Pilihan tidak valid.")
        input("Tekan ENTER untuk kembali...")
        return

    nama = input("Nama Properti [ENTER untuk batal]: ").strip()
    if not nama:
        return
    
    while True:
        lokasi = input("Lokasi [ENTER untuk batal]: ").strip()
        if not lokasi:
            return

        if not any(char.isalpha() for char in lokasi):
            print("Lokasi tidak valid!\n")
            continue

        break

    while True:
        harga = input("Harga (Rp) [ENTER untuk batal]: ").strip()
        if not harga:
            return

        if not harga.isdigit():
            print("Harga tidak valid!\n")
            continue

        break
    
    # Generate ID (ambil ID terbesar + 1)
    new_id = 1

    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            ids = []

            for row in reader:
                if row.get("id") and row["id"].isdigit():
                    ids.append(int(row["id"]))

            if ids:
                new_id = max(ids) + 1

    data_baru = {
        "id": str(new_id),
        "nama": nama,
        "kategori": kategori,
        "lokasi": lokasi,
        "harga": harga,
        "penjual": username,
        "status": "available"
    }

    with open(FILE_PROPERTI, mode='a', newline='') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "nama", "kategori", "lokasi", "harga", "penjual", "status"]
        )
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data_baru)

    print("\n[SUKSES] Properti berhasil ditambahkan!")
    input("Tekan ENTER untuk kembali...")

def lihat_properti_saya(username):
    print(f"\n--- Daftar Properti Milik {username} ---")

    with open(FILE_PROPERTI, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        found = False

        for p in reader:
            if p['penjual'].strip().lower() == username.strip().lower():

                if p['status'] == "available" or p['status'] == "pending":
                    ketersediaan = "✅ Tersedia"
                elif p['status'] == "booked":
                    ketersediaan = "⌛ Properti Telah Di-Booking"
                else:
                    ketersediaan = "❌ Terjual"
                print(f"ID: {p['id']}")
                print(f"Nama: {p['nama']} ({p['kategori']})")
                print(f"Lokasi: {p['lokasi']}")
                print(f"Harga: Rp {p['harga']}")
                print(f"Ketersediaan : {ketersediaan}")
                print("-" * 30)

                found = True

        if not found:
            print("Anda belum memiliki properti yang terdaftar.")


def hapus_properti_saya(username):
    if not os.path.exists(FILE_PROPERTI):
        print("❌ Data properti tidak ditemukan.")
        return

    id_input = input("Masukkan ID Properti yang ingin dihapus (Tekan ENTER untuk kembali): ").strip()

    if not id_input:
        return

    if not id_input.isdigit():
        print("❌ ID harus berupa angka!")
        input("Tekan ENTER untuk kembali...")
        return

    id_input = id_input.strip()

    properti_list = []
    properti_dihapus = False

    with open(FILE_PROPERTI, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        for p in reader:
            # jika ID cocok
            if p['id'] == id_input:
                # cek pemilik
                if p['penjual'].strip().lower() != username.strip().lower():
                    print("❌ Anda tidak berhak menghapus properti ini!")
                    input("Tekan ENTER untuk kembali...")
                    return

                # cek status tersedia
                if p['tersedia'] != 'available':
                    print("❌ Properti sudah tidak tersedia / terjual!")
                    input("Tekan ENTER untuk kembali...")
                    return

                properti_dihapus = True
                continue  # ⬅️ skip baris ini (hapus)

            properti_list.append(p)

    if not properti_dihapus:
        print("❌ Properti tidak ditemukan.")
        input("Tekan ENTER untuk kembali...")
        return

    # tulis ulang file
    with open(FILE_PROPERTI, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(properti_list)

    print("✅ Properti berhasil dihapus.")
    input("Tekan ENTER untuk kembali...")

def seller_menu(username):
    print(f"\nHalo {username}, selamat datang di GeoEstate Seller!")

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='w', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["id", "nama", "kategori", "lokasi", "harga", "penjual"]
            )
            writer.writeheader()

    while True:
        print("\n===== GeoEstate Menu Seller =====")
        print("[T] Tambah Properti Baru")
        print("[L] Lihat Properti Saya")
        print("[H] Hapus Properti Saya")
        print("[B] Kelola Data Booking")  
        print("[S] Kelola Data Survei")
        print("[U] Lihat Ulasan Saya")
        print("[K] Kembali")
        print("==================================")

        pilihan = input("Pilih menu: ").lower()

        # =========================
        # OPSI T: TAMBAH PROPERTI
        # =========================
        if pilihan == "t":
            tambah_properti(username)

        # =========================
        # OPSI L: LIHAT PROPERTI SAYA
        # =========================
        elif pilihan == "l":
            lihat_properti_saya(username)
            input("\nTekan ENTER untuk kembali...")

        # =========================
        # OPSI H: HAPUS PROPERTI SAYA
        # =========================
        elif pilihan == "h":
            lihat_properti_saya(username)
            hapus_properti_saya(username)

        # =========================
        # OPSI B: KELOLA BOOKING 
        # =========================
        elif pilihan == "b":
            menu_kelola_pesanan(username) 
        
        # =========================
        # OPSI S: KELOLA SURVEI
        # =========================
        elif pilihan == "s":
            menu_kelola_survei(username)

        # =========================
        # OPSI U: LIHAT ULASAN
        # =========================
        elif pilihan == "u":
            seller_review(username)

        # =========================
        # OPSI K: KEMBALI
        # =========================
        elif pilihan == "k":
            print("\n" * 25)
            loading_exit_seller()
            print("\n" * 25)
            break

        else:
            print("\nPilihan tidak valid, silakan coba lagi!")