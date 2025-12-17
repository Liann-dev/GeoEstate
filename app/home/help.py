def bantuan():
    print(f"===== BANTUAN GEOESTATE =====\n")

    while True:
        print("""Apa yang ingin kamu ketahui?

    1) GeoEstate secara umum
    2) Sistem transaksi GeoEstate
    3) Fitur yang ditawarkan GeoEstate
    4) Pihak yang terlibat
    5) Kompatibilitas GeoEstate
    6) Ketersediaan layanan
    7) Keamanan sistem GeoEstate
    """)

        try:
            P = int(input("Pilih salah satu : "))
        except ValueError:
            print("Masukkan angka yang valid!\n")
            continue

        if P == 1:
            print("\nGeoEstate adalah aplikasi berbasis web untuk jual beli real estate secara digital.")
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
            print("\nUntuk bantuan lainnya, silahkan hubungi nomor di bawah ini :\n+62 851-7158-0526 (Adi)\n+62 895-3272-66457 (Lian)")
        else:
            print("\nOpsi bantuan tidak ditemukan!")
            
        lanjut = input("\nIngin mengetahui sesuatu lagi? (Y/N): ").upper()
        if lanjut == "N":
            print("Kembali ke menu utama GeoEstate...\n")
            break