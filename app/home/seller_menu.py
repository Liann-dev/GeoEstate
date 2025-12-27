import csv
import os


from app.features.transaksi_penjual import menu_kelola_pesanan
from app.home.review_seller import seller_review
from app.features.seller_withdraw import seller_withdraw_menu

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
    
    # Generate ID
    new_id = 1
    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='r', newline='') as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                new_id = len(reader)

    data_baru = {
        "id": str(new_id),
        "nama": nama,
        "kategori": kategori,
        "lokasi": lokasi,
        "harga": harga,
        "penjual": username,
        "doc_verified": "False"
    }

    with open(FILE_PROPERTI, mode='a', newline='') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "nama", "kategori", "lokasi", "harga", "penjual", "doc_verified"]
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

                if p['doc_verified'] == "True":
                    status_text = "✅ Terverifikasi"
                else:
                    status_text = "❌ Belum Terverifikasi"

                if p['tersedia'] == "True":
                    ketersediaan = "✅ Tersedia"
                else:
                    ketersediaan = "❌ Terjual"
                print(f"ID: {p['id']}")
                print(f"Nama: {p['nama']} ({p['kategori']})")
                print(f"Lokasi: {p['lokasi']}")
                print(f"Harga: Rp {p['harga']}")
                print(f"Status: {status_text}")
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
                if p['tersedia'].strip().lower() != 'true':
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
    print(f"\nHalo {username}, selamat datang di GeoEstate Merchant!")

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='w', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["id", "nama", "kategori", "lokasi", "harga", "penjual", "doc_verified"]
            )
            writer.writeheader()

    while True:
        print("\n===== GeoEstate Menu Merchant =====")
        print("1. Tambah Properti Baru")
        print("2. Lihat Properti Saya")
        print("3. Hapus Properti Saya")
        print("4. Kelola Pesanan Masuk")  
        print("5. Lihat Ulasan Properti Saya")
        print("6. Ajukan Pengunduran Diri Sebagai Merchant")
        print("7. Kembali")
        print("==================================")

        pilihan = input("Pilih menu (1-6): ")

        # =========================
        # OPSI 1: TAMBAH PROPERTI
        # =========================
        if pilihan == "1":
            tambah_properti(username)

        # =========================
        # OPSI 2: LIHAT PROPERTI SAYA
        # =========================
        elif pilihan == "2":
            lihat_properti_saya(username)
            input("\nTekan ENTER untuk kembali...")

        # =========================
        # OPSI 3: HAPUS PROPERTI SAYA
        # =========================
        elif pilihan == "3":
            lihat_properti_saya(username)
            hapus_properti_saya(username)

        # =========================
        # OPSI 4: KELOLA PESANAN 
        # =========================
        elif pilihan == "4":
            menu_kelola_pesanan(username) 
        
        # =========================
        # OPSI 5: LIHAT ULASAN
        # =========================
        elif pilihan == "5":
            seller_review(username)

        # =========================
        # OPSI 6: UNDUR DIRI MERCHANT
        # =========================
        elif pilihan == "6":
            seller_withdraw_menu(username)

        # =========================
        # OPSI 7: KEMBALI
        # =========================
        elif pilihan == "7":
            print("Kembali ke menu utama...\n")
            break

        else:
            print("\nPilihan tidak valid, silakan coba lagi!")