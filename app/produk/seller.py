print("Welcome to GeoEstate Seller")

def halaman_utama():
    properti = []

    while True:
        print("\n===== GeoEstate Menu Utama =====")
        print("1. Tambah Properti Baru")
        print("2. Lihat Daftar Properti")
        print("3. Keluar / Logout")
        print("===============================")

        pilihan = input("Pilih menu (1-3): ")

        if pilihan == "1":
            print("\n--- Tambah Properti Baru ---")
            nama = input("Nama Properti: ")
            lokasi = input("Lokasi: ")
            harga = int(input("Harga: "))

            properti.append({"nama": nama, "lokasi": lokasi, "harga": harga})
            print(f"Properti '{nama}' berhasil ditambahkan!\n")

        elif pilihan == "2":
            print("\n--- Daftar Properti ---")
            if len(properti) == 0:
                print("Belum ada properti, silakan tambahkan dulu melalui menu 1.\n")
            else:
                for p in properti:
                    print(f"{p['nama']} - {p['lokasi']} - Rp {p['harga']}")
                print()

        elif pilihan == "3":
            print("\nTerima kasih, sampai jumpa!\n")
            break

        else:
            print("\nPilihan tidak valid, silakan coba lagi!\n")

halaman_utama()
