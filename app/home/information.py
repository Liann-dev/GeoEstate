def tampilkan_info(pilihan):
    if pilihan == 1:
        print("Tentang GeoEstate:")
        print("GeoEstate adalah platform jual beli properti berbasis digital.")
        print("Kami memudahkan pengguna untuk mencari properti impian dengan fitur pemetaan geografis, filter lokasi, dan informasi lengkap.")
        print("GeoEstate hadir untuk menciptakan pengalaman transaksi properti yang lebih transparan, cepat, dan aman.")

    elif pilihan == 2:
        print("Sistem transaksi GeoEstate:")
        print("Transaksi finansial dilakukan langsung antara pembeli dan penjual di luar sistem GeoEstate.")
        
    elif pilihan == 3:
        print("Fitur yang ditawarkan GeoEstate:")
        print("Fitur utama: pencarian properti, manajemen akun, data properti, chat internal, peta digital, wishlist, feedback.")

    elif pilihan == 4:
        print("Pihak yang terlibat:")
        print("Tiga pihak utama: Pembeli, Penjual, dan Admin/Verifikator.")

    elif pilihan == 5:
        print("Kompatibilitas GeoEstate:")
        print("GeoEstate dapat dijalankan di browser seperti Chrome, Firefox, Safari, dan Edge.")

    elif pilihan == 6:
        print("Ketersediaan layanan:")
        print("Layanan GeoEstate tersedia 24/7 kecuali saat maintenance.")

    elif pilihan == 7:
        print("Keamanan sistem GeoEstate:")
        print("GeoEstate menerapkan autentikasi, enkripsi, kontrol akses, dan pemindaian keamanan rutin.")

    elif pilihan == 8:
        print("Untuk Informasi lainnya silakan hubungi kontak di bawah ini:")
        print("+62 851-7158-0526 (Adi)")
        print("+62 895-3272-66457 (Lian)")

    else:
        print("\nPilihan tidak valid!")

def info():
    while True:
        print("\n===== INFORMASI UMUM GEOESTATE =====\n")
        print("""Apa yang ingin kamu ketahui?
        1) Tentang GeoEstate
        2) Sistem transaksi GeoEstate
        3) Fitur yang ditawarkan GeoEstate
        4) Pihak yang terlibat
        5) Kompatibilitas GeoEstate
        6) Ketersediaan layanan
        7) Keamanan sistem GeoEstate
        8) Informasi lainnya
        0) Kembali""")

        user_input = input("\nPilih salah satu : ").strip()

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
            print("-"*25)
            tampilkan_info(pilihan)
            print("-"*25,"\n")
        else:
            print("Pilihan tidak tersedia!")
