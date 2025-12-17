from app.auth.register import register
from app.auth.login import login
from app.home.home_buyer import home_buyer
from app.home.home_seller import home_seller
from app.features.admin_verification import admin_menu


def main():
    while True:
        print("\n=== GeoEstate ===")
        print("1. Register")
        print("2. Login")
        print("3. Admin Verifikasi")
        print("4. Exit")

        pilihan = input("Pilih opsi (1-4): ")

        # =====================
        # REGISTER
        # =====================
        if pilihan == '1':
            register()

        # =====================
        # LOGIN USER
        # =====================
        elif pilihan == '2':
            user = login()
            if user:
                input("Tekan ENTER untuk masuk ke halaman utama...")

                if user['role'] == 'pembeli':
                    home_buyer(user['username'])

                elif user['role'] == 'penjual':
                    home_seller(user['username'])

        # =====================
        # ADMIN VERIFIKASI
        # =====================
        elif pilihan == '3':
            print("\n=== MODE ADMIN ===")
            print("Simulasi admin/verifikator GeoEstate\n")
            admin_menu()

        # =====================
        # EXIT
        # =====================
        elif pilihan == '4':
            print("Terima kasih telah menggunakan GeoEstate!")
            break

        else:
            print("Opsi tidak valid, silakan coba lagi.\n")


if __name__ == "__main__":
    main()