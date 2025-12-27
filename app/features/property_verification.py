import csv

FILE_PROPERTIES = "data/properti.csv"

def tampilkan_properti():
    with open(FILE_PROPERTIES, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    if not data:
        print("Belum ada data properti.\n")
        return

    print("\n=== Daftar Properti ===")
    print("-" * 100)
    print(f"{'ID':<5}{'NAMA':<20}{'KATEGORI':<15}{'LOKASI':<20}{'HARGA':<15}{'PENJUAL':<15}{'VERIFIED':<10}")
    print("-" * 100)

    for prop in data:
        status = "Ya" if prop['doc_verified'] == "True" else "Tidak"
        print(f"{prop['id']:<5}{prop['nama']:<20}{prop['kategori']:<15}{prop['lokasi']:<20}{prop['harga']:<15}{prop['penjual']:<15}{status:<10}")

    print("-" * 100)

def verifikasi_properti(id_properti):
    properti_list = []
    ditemukan = False

    with open(FILE_PROPERTIES, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == str(id_properti):
                ditemukan = True
                if row['doc_verified'] == "True":
                    print("Properti sudah terverifikasi.\n")
                    input("Tekan ENTER untuk kembali...")
                    return
                else:
                    row['doc_verified'] = "True"
            properti_list.append(row)

    if not ditemukan:
        print("Properti tidak ditemukan.\n")
        input("Tekan ENTER untuk kembali...")
        return

    with open(FILE_PROPERTIES, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=properti_list[0].keys())
        writer.writeheader()
        writer.writerows(properti_list)

    print("Properti berhasil diverifikasi.\n")
    input("Tekan ENTER untuk kembali...")

def hapus_verifikasi_properti(id_properti):
    properti_list = []
    ditemukan = False

    with open(FILE_PROPERTIES, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == str(id_properti):
                ditemukan = True
                if row['doc_verified'] == "False":
                    print("Properti memang belum diverifikasi.\n")
                    input("Tekan ENTER untuk kembali...")
                    return
                else:
                    row['doc_verified'] = "False"
            properti_list.append(row)

    if not ditemukan:
        print("Properti tidak ditemukan.\n")
        input("Tekan ENTER untuk kembali...")
        return

    with open(FILE_PROPERTIES, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=properti_list[0].keys())
        writer.writeheader()
        writer.writerows(properti_list)

    print("Verifikasi properti berhasil dihapus.\n")
    input("Tekan ENTER untuk kembali...")

def menu_verifikasi_properti():
    while True:
        print("""
=== Menu Verifikasi Properti ===
1. Apa itu verifikasi properti?
2. Verifikasi Properti
3. Hapus Verifikasi Properti
4. Kembali
""")
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            print("""
Verifikasi properti adalah proses admin untuk memastikan dokumen
atau kelengkapan suatu properti sudah valid sebelum dipublikasikan.
""")
            input("Tekan ENTER untuk kembali...")

        elif pilihan == "2":
            tampilkan_properti()
            
            id_properti = input("Masukkan ID properti yang ingin diverifikasi (ENTER untuk batal): ")

            if not id_properti:
                continue
            else:
                verifikasi_properti(id_properti)
                continue
            

        elif pilihan == "3":
            tampilkan_properti()
           
            id_properti = input("Masukkan ID properti yang ingin dihapus verifikasinya (ENTER untuk batal): ")
            if not id_properti:
                continue
            else:
                hapus_verifikasi_properti(id_properti)
                continue
            

        elif pilihan == "4":
            break

        else:
            print("Pilihan tidak valid.\n")