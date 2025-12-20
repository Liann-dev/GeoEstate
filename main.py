from app.auth.register import register
from app.auth.login import login
from app.home.home_buyer import home_buyer
from app.home.home_seller import home_seller

from app.Utils.OnboardingScreen import show_splash, show_onboarding
from app.Utils.padding import pad_center as centerpadding

from app.features.admin_verification import admin_menu



def main():
    show_splash()
    show_onboarding()
    while True:
        print("\n" * 25)
        
        print(centerpadding("Selamat datang di GeoEstate!"))
        print(centerpadding("1. Register"))
        print(centerpadding("2. Login"))
        print(centerpadding("3. Admin Verifikasi"))
        print(centerpadding("4. Exit"))
        pilihan = input(centerpadding("Pilih opsi (1/2/3/4): "))
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
                if user['role'] == 'pembeli':
                    input("Tekan ENTER untuk masuk ke halaman pembeli...")
                    home_buyer(user['username'])
                elif user['role'] == 'penjual':
                    input("Tekan ENTER untuk masuk ke halaman penjual...")
                    home_seller(user['username'])
                break
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