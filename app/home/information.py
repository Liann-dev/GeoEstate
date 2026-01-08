from app.features.feedback import collect_feedback

def tampilkan_info(pilihan, username):
    if pilihan == 1:
        print("Tentang GeoEstate:")
        print("GeoEstate adalah platform jual beli properti berbasis digital.")

    elif pilihan == 2:
        print("Sistem transaksi GeoEstate:")
        print("Transaksi dilakukan langsung antara pembeli dan penjual.")

    elif pilihan == 3:
        print("Fitur yang ditawarkan GeoEstate:")
        print("Pencarian properti, chat, peta, wishlist, feedback.")

    elif pilihan == 4:
        print("Pihak yang terlibat:")
        print("Pembeli, Penjual, dan Admin.")

    elif pilihan == 5:
        print("Kompatibilitas GeoEstate:")
        print("Chrome, Firefox, Safari, Edge.")

    elif pilihan == 6:
        print("Ketersediaan layanan:")
        print("24/7 kecuali maintenance.")

    elif pilihan == 7:
        print("Keamanan sistem GeoEstate:")
        print("Autentikasi, enkripsi, kontrol akses.")

    elif pilihan == 8:
        collect_feedback(username)

    elif pilihan == 9:
        print("Informasi lainnya:")
        print("Silakan hubungi kami di geoestate@gmail.com")

    else:
        print("\nPilihan tidak valid!")


def info(username):
    while True:
        print("\n===== PUSAT BANTUAN - INFORMASI UMUM GEOESTATE =====\n")
        print("""Apa yang ingin kamu ketahui?
        1) Tentang GeoEstate
        2) Sistem transaksi GeoEstate
        3) Fitur yang ditawarkan GeoEstate
        4) Pihak yang terlibat
        5) Kompatibilitas GeoEstate
        6) Ketersediaan layanan
        7) Keamanan sistem GeoEstate
        8) Kirim Feedback untuk GeoEstate
        9) Informasi lainnya
        0) Kembali""")

        pilihan = input("\nPilih salah satu : ").strip()

        if not pilihan.isdigit():
            print("Input harus berupa angka!")
            continue

        pilihan = int(pilihan)

        if pilihan == 0:
            return

        if 1 <= pilihan <= 9:
            print("-" * 25)
            tampilkan_info(pilihan, username)
            print("-" * 25)
