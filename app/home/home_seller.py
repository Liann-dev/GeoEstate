import csv
import os

FILE_PROPERTI = "data/properti.csv"

def home_seller(username):
    print(f"\nHalo {username}, selamat datang di GeoEstate Seller!")

    # Pastikan file CSV ada
    if not os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='w', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["id", "nama", "kategori", "lokasi", "harga", "penjual", "doc_verified"]
            )
            writer.writeheader()

    while True:
        print("\n===== GeoEstate Menu Penjual =====")
        print("1. Tambah Properti Baru")
        print("2. Lihat Properti Saya")
        print("3. Logout")
        print("=================================")

        pilihan = input("Pilih menu (1-3): ")

        # =========================
        # 1. TAMBAH PROPERTI
        # =========================
        if pilihan == "1":
            print("\n--- Tambah Properti Baru ---")

            print("Pilih kategori properti:")
            print("1. Rumah")
            print("2. Villa")
            print("3. Resort")
            kategori_pilihan = input("Masukkan pilihan (1/2/3): ")

            if kategori_pilihan == "1":
                kategori = "Rumah"
            elif kategori_pilihan == "2":
                kategori = "Villa"
            elif kategori_pilihan == "3":
                kategori = "Resort"
            else:
                print("Kategori tidak valid.")
                continue

            nama = input("Nama Properti : ")
            lokasi = input("Lokasi        : ")
            harga = input("Harga         : ")

            # Ambil ID terakhir
            with open(FILE_PROPERTI, mode='r', newline='') as file:
                reader = list(csv.DictReader(file))
                new_id = len(reader) + 1

            data_baru = {
                "id": str(new_id),
                "nama": nama,
                "kategori": kategori,
                "lokasi": lokasi,
                "harga": harga,
                "penjual": username,
                "doc_verified": "False"   # <- BELUM TERVERIFIKASI
            }

            with open(FILE_PROPERTI, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data_baru.keys())
                writer.writerow(data_baru)

            print("\nProperti berhasil ditambahkan!")
            print("Status dokumen: BELUM TERVERIFIKASI")
            print("Menunggu verifikasi sebelum dapat ditampilkan ke pembeli.\n")

        # =========================
        # 2. LIHAT PROPERTI SAYA
        # =========================
        elif pilihan == "2":
            print("\n--- Daftar Properti Saya ---")

            with open(FILE_PROPERTI, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                ada = False

                for p in reader:
                    if p['penjual'] == username:
                        status = "Terverifikasi" if p['doc_verified'] == "True" else "Belum Terverifikasi"
                        print(f"- ID {p['id']} | {p['nama']} ({p['kategori']})")
                        print(f"  Lokasi : {p['lokasi']}")
                        print(f"  Harga  : Rp {p['harga']}")
                        print(f"  Status : {status}\n")
                        ada = True

                if not ada:
                    print("Anda belum memiliki properti.\n")

        # =========================
        # 3. LOGOUT
        # =========================
        elif pilihan == "3":
            print(f"\nLogout berhasil. Sampai jumpa, {username}!\n")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.\n")