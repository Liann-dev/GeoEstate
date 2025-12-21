import csv

FILE_USERS = "data/users.csv"

def tampilkan_user():
    with open(FILE_USERS, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    if not data:
        print("Belum ada data user.\n")
        return

    print("\n=== Daftar User ===")
    print("-" * 85)
    print(f"{'USERNAME':<15}{'EMAIL':<30}{'ROLE':<15}{'VERIFIED':<10}")
    print("-" * 85)

    for user in data:
        status = "Ya" if user['user_verified'] == "True" else "Tidak"
        print(f"{user['username']:<15}{user['email']:<30}{user['role']:<15}{status:<10}")

    print("-" * 85)

def verifikasi_user(cari):
    users = []
    ditemukan = False

    with open(FILE_USERS, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == cari:
                ditemukan = True
                if row['user_verified'] == "True":
                    print("User sudah terverifikasi.\n")
                    input("Tekan ENTER untuk kembali...")
                    return
                else:
                    row['user_verified'] = "True"
            users.append(row)

    if not ditemukan:
        print("User tidak ditemukan.\n")
        input("Tekan ENTER untuk kembali...")
        return

    with open(FILE_USERS, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

    print("User berhasil diverifikasi.\n")
    input("Tekan ENTER untuk kembali...")

def hapus_verifikasi_user(cari):
    users = []
    ditemukan = False

    with open(FILE_USERS, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == cari:
                ditemukan = True
                if row['user_verified'] == "False":
                    print("User memang belum terverifikasi.\n")
                    input("Tekan ENTER untuk kembali...")
                    return
                else:
                    row['user_verified'] = "False"
            users.append(row)

    if not ditemukan:
        print("User tidak ditemukan.\n")
        input("Tekan ENTER untuk kembali...")
        return

    with open(FILE_USERS, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

    print("Verifikasi user berhasil dihapus.\n")
    input("Tekan ENTER untuk kembali...")

def menu_verifikasi_user():
    while True:
        print("""
=== Menu Verifikasi User ===
1. Apa itu verifikasi user?
2. Verifikasi User
3. Hapus Verifikasi User
4. Kembali
""")
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            print("""
Verifikasi user adalah proses validasi akun oleh admin
yang bertujuan untuk memberikan validasi bahwa user 
dapat dipercaya dalam proses jual/beli. User yang sudah
diverifikasi biasanya memiliki tanda unik di halaman
profilnya.
""")
            input("Tekan ENTER untuk kembali...")

        elif pilihan == "2":
            tampilkan_user()
            while True:
                cari = input("Masukkan username: ")
                if not cari:
                    print("Kolom ini tidak boleh kosong!\n")
                else:
                    break
            verifikasi_user(cari)

        elif pilihan == "3":
            tampilkan_user()
            while True:
                cari = input("Masukkan username: ")
                if not cari:
                    print("Kolom ini tidak boleh kosong!\n")
                else:
                    break
            hapus_verifikasi_user(cari)

        elif pilihan == "4":
            break

        else:
            print("Pilihan tidak valid.\n")