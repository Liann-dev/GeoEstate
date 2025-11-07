print(f"===== BANTUAN =====\n")

while True:
    print("""Apa yang ingin kamu ketahui?

    1) GeoEstate secara umum
    2) Sistem transaksi GeoEstate
    3) Fitur yang ditawarkan GeoEstate
    4) Pihak yang terlibat dalam GeoEstate
    5) Kompatibilitas GeoEstate
    6) Keteserdiaan layanan GeoEstate
    7) Keamanan sistem GeoEstate
    """)

    P = int(input("Pilih salah satu : "))

    if P == 1:
        print(f"\nGeoEstate Project adalah sebuah aplikasi berbasis web yang berfungsi sebagai platform informasi dan komunikasi dalam jual beli real estate.")

    if P == 2:
        print(f"\nGeoEstate tidak menyediakan sistem pembayaran internal.\nSeluruh transaksi finansial dilakukan secara langsung antara penjual dan pembeli di luar sistem melalui proses legal formal yang melibatkan PPAT dan notaris.")
    
    if P == 3:
        print(f"""\n GeoEstate akan mencakup beberapa fitur utama sebagai berikut:
        
        1) Pencarian dan penyaringan properti
        2) Manajemen akun pengguna
        3) Pengelolaan data properti
        4) Notifikasi 
        5) Chat internal
        6) Layanan peta digital
        7) Wishlist dan riwayat pencarian
        8) Feedback""")

    if P == 4:
        print(f"""\nTerdapat tiga pihak yang terlibat dalam GeoEstate:
              
        1) Pembeli/Pencari Properti = Pengguna umum yang mencari informasi properti berdasarkan lokasi dan kebutuhan spesifik.
        2) Penjual/Agen Properti = Individu atau lembaga yang ingin mempromosikan properti milik mereka melalui sistem.
        3) Admin/Verifikator = Tim pengelola platform yang bertugas menjaga keaslian data, moderasi konten, dan pemeliharaan sistem.""")
    
    if P == 5:
        print(f"\nGeoEstate dapat dijalankan di browser apapun, seperti : Google Chrome, Mozilla Firefox, Apple Safari, Microsoft Edge, dll.")
    
    if P == 6:
        print(f"\nLayanan GeoEstate selalu tersedia 24/7, kecuali selama periode maintenance yang harus dijadwalkan sebelumnya dan diumumkan kepada pengguna.")
    
    if P == 7:
        print(f"""\nBerikut adalah beberapa fitur keamanan sistem GeoEstate:
              
        1) Autentikasi: Sistem GeoEstate mewajibkan pengguna untuk mengautentikasi diri mereka sendiri sebelum mengakses informasi sensitif apapun menggunakan kebijakan kata sandi yang kuat dan autentikasi multifaktor untuk keamanan tambahan.
        2) Otorisasi: Sistem GeoEstate menerapkan kontrol akses berbasis peran, memastikan bahwa pengguna hanya dapat mengakses informasi dan fungsi yang diizinkan untuk mereka gunakan.
        3) Enkripsi: Sistem GeoEstate menggunakan teknik enkripsi yang kuat untuk melindungi informasi sensitif seperti detail kartu kredit, informasi akun pengguna, dan riwayat pesanan.
        4) Jejak audit: Sistem GeoEstate menyimpan jejak audit terperinci dari semua aktivitas pengguna, termasuk login, transaksi, dan perubahan sistem, untuk memastikan akuntabilitas dan memfasilitasi investigasi jika terjadi insiden keamanan.
        5) Pemindaian kerentanan: Sistem GeoEstate menjalani pemindaian kerentanan dan uji penetrasi secara berkala untuk mengidentifikasi dan mengatasi setiap kerentanan keamanan dan memastikan perlindungan berkelanjutan.
        6) Pemulihan bencana: Sistem GeoEstate memiliki rencana pemulihan bencana yang kuat untuk memastikan bahwa data dapat dipulihkan dengan cepat dan aman jika terjadi pelanggaran keamanan atau bencana lainnya.""")
    
    while True:
        L = input(f"\nApakah ingin mengetahui sesuatu lagi (Y/N)? ")

        if L == "Y":
            print("Mengembalikan ke laman awal menu bantuan...")
            break
        
        elif L == "N":
            print("Mengeluarkan dari menu bantuan...")
            break

        else:
            print("Tolong jawab dengan Y/N saja!")
    
    if L == "N":
        break