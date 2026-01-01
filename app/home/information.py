def tampilkan_info(pilihan):
    if pilihan == 1:
        print("\nGeoEstate adalah platform jual beli properti berbasis digital.")
        print("Kami memudahkan pengguna untuk mencari properti impian dengan fitur pemetaan geografis, filter lokasi, dan informasi lengkap.")
        print("GeoEstate hadir untuk menciptakan pengalaman transaksi properti yang lebih transparan, cepat, dan aman.\n")

    elif pilihan == 2:
        print("\nTransaksi finansial dilakukan langsung antara pembeli dan penjual di luar sistem GeoEstate.")

    elif pilihan == 3:
        print("\nFitur utama: pencarian properti, manajemen akun, data properti, chat internal, peta digital, wishlist, feedback.")

    elif pilihan == 4:
        print("\nTiga pihak utama: Pembeli, Penjual, dan Admin/Verifikator.")

    elif pilihan == 5:
        print("\nGeoEstate dapat dijalankan di browser seperti Chrome, Firefox, Safari, dan Edge.")

    elif pilihan == 6:
        print("\nLayanan GeoEstate tersedia 24/7 kecuali saat maintenance.")

    elif pilihan == 7:
        print("\nGeoEstate menerapkan autentikasi, enkripsi, kontrol akses, dan pemindaian keamanan rutin.")

    elif pilihan == 8:
        print("\nKontak:")
        print("+62 851-7158-0526 (Adi)")
        print("+62 895-3272-66457 (Lian)")

    else:
        print("\nPilihan tidak valid!")

def info():
    print("===== INFORMASI UMUM GEOESTATE =====\n")

    print("""Apa yang ingin kamu ketahui?

    1) Tentang GeoEstate
    2) Sistem transaksi GeoEstate
    3) Fitur yang ditawarkan GeoEstate
    4) Pihak yang terlibat
    5) Kompatibilitas GeoEstate
    6) Ketersediaan layanan
    7) Keamanan sistem GeoEstate
    8) Informasi lainnya
    0) Kembali
    """)

    # ===== FASE 1: PILIHAN AWAL (WAJIB VALID) =====
    while True:
        user_input = input("Pilih salah satu : ").strip()

        if user_input == "":
            print("Pilihan tidak boleh kosong!\n")
            continue

        if not user_input.isdigit():
            print("Input harus berupa angka!\n")
            continue

        pilihan = int(user_input)

        if pilihan == 0:
            return

        if 1 <= pilihan <= 8:
            tampilkan_info(pilihan)
            break
        else:
            print("Pilihan tidak tersedia!\n")

    # ===== FASE 2: PILIHAN LANJUTAN =====
    while True:
        user_input = input("\nIngin mengetahui sesuatu lagi? ").strip()

        if user_input == "":
            print("Pilihan tidak boleh kosong!")
            continue

        if not user_input.isdigit():
            print("Input harus berupa angka!")
            continue

        pilihan = int(user_input)

        if pilihan == 0:
            return

        if 1 <= pilihan <= 8:
            tampilkan_info(pilihan)
        else:
            print("Pilihan tidak tersedia!")
