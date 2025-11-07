print("Welcome to GeoEstate Seller")

def home_seller(username):  # <=== Tambahkan parameter username
    properti = []

    print(f"\nHalo {username}, selamat datang di GeoEstate Seller!")

    while True:
        print("\n===== GeoEstate Menu Utama (Penjual) =====")
        print("1. Tambah Properti Baru")
        print("2. Lihat Daftar Properti")
        print("3. Keluar / Logout")
        print("=========================================")

        pilihan = input("Pilih menu (1-3): ")

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
                kategori = "Lainnya"

            nama = input("\nNama Properti: ")
            lokasi = input("Lokasi: ")
            harga = int(input("Harga: "))

            properti.append({
                "nama": nama,
                "lokasi": lokasi,
                "harga": harga,
                "kategori": kategori
            })

            print(f"\nProperti '{nama}' ({kategori}) berhasil ditambahkan!\n")

        elif pilihan == "2":
            print("\n--- Daftar Properti ---")
            if len(properti) == 0:
                print("Belum ada properti, silakan tambahkan dulu melalui menu 1.\n")
            else:
                for i, p in enumerate(properti, start=1):
                    print(f"{i}. {p['nama']} ({p['kategori']}) - {p['lokasi']} - Rp {p['harga']}")
                print()

        elif pilihan == "3":
            print(f"\nTerima kasih, {username}. Sampai jumpa!\n")
            break

        else:
            print("\nPilihan tidak valid, silakan coba lagi!\n")