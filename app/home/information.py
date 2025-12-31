def info():
    print("===== INFORMASI UMUM GEOESTATE =====\n")

    while True:
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

        try:
            P = int(input("Pilih salah satu : "))
        except ValueError:
            print("\nKarakter tidak valid! Silahkan masukkan angka saja.")
            input("Tekan ENTER untuk coba lagi...")
            continue

        if P == 1:
            print("GeoEstate adalah platform jual beli properti berbasis digital.")
            print("Kami memudahkan pengguna untuk mencari properti impian dengan fitur pemetaan geografis, filter lokasi, dan informasi lengkap.")
            print("GeoEstate hadir untuk menciptakan pengalaman transaksi properti yang lebih transparan, cepat, dan aman.\n")
        elif P == 2:
            print("\nTransaksi finansial dilakukan langsung antara pembeli dan penjual di luar sistem GeoEstate.")
        elif P == 3:
            print("\nFitur utama: pencarian properti, manajemen akun, data properti, chat internal, peta digital, wishlist, feedback.")
        elif P == 4:
            print("\nTiga pihak utama: Pembeli, Penjual, dan Admin/Verifikator.")
        elif P == 5:
            print("\nGeoEstate dapat dijalankan di browser seperti Chrome, Firefox, Safari, dan Edge.")
        elif P == 6:
            print("\nLayanan GeoEstate tersedia 24/7 kecuali saat maintenance.")
        elif P == 7:
            print("\nGeoEstate menerapkan autentikasi, enkripsi, kontrol akses, dan pemindaian keamanan rutin.")
        elif P == 8:
            print("\nUntuk informasi lainnya, silahkan hubungi nomor di bawah ini :"
                  "\n+62 851-7158-0526 (Adi)"
                  "\n+62 895-3272-66457 (Lian)")
        elif P == 0:
            print("Kembali ke menu utama...\n")
            break
        else:
            print("\nOpsi bantuan tidak ditemukan!")
            input("Tekan ENTER untuk coba lagi...")
            continue   

        while True:
            lanjut = input("\nIngin mengetahui sesuatu lagi? (Y/N): ").strip().upper()

            if lanjut == "Y":
                break  
            elif lanjut == "N":
                print("Kembali ke menu utama...\n")
                return  
            else:
                print("Input tidak valid! Silakan pilih Y atau N saja.")