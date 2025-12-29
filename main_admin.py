from app.auth.login import login
from app.home.admin_menu import admin_menu

from app.Utils.padding import pad_center as centerpadding


def main_admin():
    while True:
        print("\n" * 25)
        print(centerpadding("=== GeoEstate ADMIN PANEL ==="))
        print(centerpadding("1. Login Admin"))
        print(centerpadding("2. Exit"))

        pilihan = input(centerpadding("Pilih opsi (1/2): "))

        if pilihan == "1":
            user = login()
            if not user:
                continue

            if user["role"] != "admin":
                print("❌ Akses ditolak. Ini khusus ADMIN.")
                input("Tekan ENTER...")
                continue

            input("Tekan ENTER untuk masuk Admin Panel...")
            admin_menu(user["username"])

        elif pilihan == "2":
            print("Keluar dari Admin Panel.")
            break

        else:
            print("Pilihan tidak valid.")
            input("Tekan ENTER...")


if __name__ == "__main__":
    main_admin()
