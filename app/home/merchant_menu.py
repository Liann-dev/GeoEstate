import csv
import os


from app.features.transaksi_penjual import menu_kelola_pesanan
from app.home.profile import profile
from app.home.review_seller import seller_review
from app.features.merchant_withdraw import merchant_withdraw_menu

FILE_PROPERTI = "data/properti.csv"

def merchant_menu(username):
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
        print("3. Kelola Pesanan Masuk")  
        print("4. Lihat Ulasan Properti Saya")
        print("5. Ajukan Pengunduran Diri Sebagai Merchant")
        print("6. Kembali")
        print("==================================")

        pilihan = input("Pilih menu (1-6): ")

        # =========================
        # OPSI 1: TAMBAH PROPERTI
        # =========================
        if pilihan == "1":
            print("\n--- Tambah Properti Baru ---")
            
            print("Pilih kategori properti:")
            print("1. Rumah")
            print("2. Villa")
            print("3. Resort")
            kategori_pilihan = input("Masukkan pilihan (1/2/3): ")

            if kategori_pilihan == "1": kategori = "Rumah"
            elif kategori_pilihan == "2": kategori = "Villa"
            elif kategori_pilihan == "3": kategori = "Resort"
            else: kategori = "Lainnya"

            nama = input("Nama Properti : ")
            lokasi = input("Lokasi        : ")
            harga = input("Harga (Rp)    : ")

            new_id = 1
            if os.path.exists(FILE_PROPERTI):
                with open(FILE_PROPERTI, mode='r') as file:
                    reader = list(csv.reader(file))
                    if len(reader) > 0:
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
                writer = csv.DictWriter(file, fieldnames=["id", "nama", "kategori", "lokasi", "harga", "penjual", "doc_verified"])
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data_baru)

            print("\n[SUKSES] Properti berhasil ditambahkan!")
            input("Tekan ENTER untuk kembali...")

        # =========================
        # OPSI 2: LIHAT PROPERTI SAYA
        # =========================
        elif pilihan == "2":
         
            print(f"\n--- Daftar Properti Milik {username} ---")

            with open(FILE_PROPERTI, mode='r') as file:
                reader = csv.DictReader(file)
                found = False

                for p in reader:
                    if p['penjual'] == username:
                        if p['doc_verified'] == "True":
                            status_text = "✅ Terverifikasi"
                        else:
                            status_text = "⏳ Menunggu Verifikasi"
                        
                        print(f"ID: {p['id']}")
                        print(f"Nama: {p['nama']} ({p['kategori']})")
                        print(f"Lokasi: {p['lokasi']}")
                        print(f"Harga: Rp {p['harga']}")
                        print(f"Status: {status_text}")
                        print("-" * 30)
                        found = True

                if not found:
                    print("Anda belum memiliki properti yang terdaftar.")
            
            input("\nTekan ENTER untuk kembali...")

        # =========================
        # OPSI 3: KELOLA PESANAN 
        # =========================
        elif pilihan == "3":
            
            menu_kelola_pesanan(username) 
        
        # =========================
        # OPSI 4: LIHAT ULASAN
        # =========================
        elif pilihan == "4":
            seller_review(username)

        # =========================
        # OPSI 5: UNDUR DIRI MERCHANT
        # =========================
        elif pilihan == "5":
            merchant_withdraw_menu(username)

        # =========================
        # OPSI 6: KEMBALI
        # =========================
        elif pilihan == "6":
            print("Kembali ke menu utama...\n")
            break

        else:
            print("\nPilihan tidak valid, silakan coba lagi!")