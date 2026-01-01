import csv
import os
from app.features.seller_management import menu_kelola_seller
from app.features.admin_feedback import lihat_feedback
from app.features.user_verification import menu_verifikasi_user

# FILE_USERS = "data/users.csv"
# FILE_PROPERTI = "data/properti.csv"


# def verifikasi_user():
#     if not os.path.exists(FILE_USERS):
#         print("File users.csv tidak ditemukan.")
#         return

#     users = []

#     with open(FILE_USERS, mode='r', newline='') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             users.append(row)

#     print("\n=== DAFTAR USER ===")
#     for i, u in enumerate(users, start=1):
#         status = "Terverifikasi" if u['user_verified'] == "True" else "Belum"
#         print(f"{i}. {u['username']} | {u['role']} | {status}")

#     username = input("\nMasukkan username yang ingin diverifikasi: ")

#     ditemukan = False
#     for u in users:
#         if u['username'] == username:
#             u['user_verified'] = "True"
#             ditemukan = True
#             break

#     if not ditemukan:
#         print("User tidak ditemukan.")
#         return

#     with open(FILE_USERS, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=users[0].keys())
#         writer.writeheader()
#         writer.writerows(users)

#     print("✅ User berhasil diverifikasi.\n")


# def verifikasi_properti():
#     if not os.path.exists(FILE_PROPERTI):
#         print("File properti.csv tidak ditemukan.")
#         return

#     properti = []

#     with open(FILE_PROPERTI, mode='r', newline='') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             properti.append(row)

#     print("\n=== DAFTAR PROPERTI ===")
#     for p in properti:
#         status = "Terverifikasi" if p['doc_verified'] == "True" else "Belum"
#         print(f"ID {p['id']} | {p['nama']} | {status}")

#     id_properti = input("\nMasukkan ID properti yang ingin diverifikasi: ")

#     ditemukan = False
#     for p in properti:
#         if p['id'] == id_properti:
#             p['doc_verified'] = "True"
#             ditemukan = True
#             break

#     if not ditemukan:
#         print("Properti tidak ditemukan.")
#         return

#     with open(FILE_PROPERTI, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=properti[0].keys())
#         writer.writeheader()
#         writer.writerows(properti)

#     print("✅ Dokumen properti berhasil diverifikasi.\n")


def admin_menu(username):
    while True:
        print("\n" * 50) 
        print("===== MENU ADMIN =====")
        print("1. Verifikasi Data User")
        print("2. Kelola Data Seller")
        print("3. Lihat Feedback")
        print("4. Keluar / Logout")
        pilihan = input(f"\nPilih menu (1-4): ")

        if pilihan == "1":
            menu_verifikasi_user()
        elif pilihan == "2":
            menu_kelola_seller()
        elif pilihan == "3":
            lihat_feedback()
        elif pilihan == "4":
            print("\nLogout berhasil!")
            input("Tekan ENTER untuk kembali ke halaman awal...")
            print("\n" * 25)
            return
        else:
            print("Pilihan tidak valid.\n")