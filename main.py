from app.auth.register import register
from app.auth.login import login
from app.home.home_user import home_user
from app.home.home_seller import home_seller
from app.Utils.OnboardingScreen import show_splash, show_onboarding
from app.Utils.padding import pad_center as centerpadding


def loading():
    show_splash()
    show_onboarding()

def main():
    while True:
        print("\n" * 25)
        print(centerpadding("Selamat datang di GeoEstate!"))
        print(centerpadding("1. Register"))
        print(centerpadding("2. Login"))
        print(centerpadding("3. Exit"))
        pilihan = input(centerpadding("Pilih opsi (1/2/3): "))
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
                if user['role'] == 'user':
                    input("Tekan ENTER untuk masuk...")
                    home_user(user['username'])
                elif user['role'] == 'seller':
                    input("Tekan ENTER untuk masuk...")
                    home_seller(user['username'])
                elif user['role'] == 'admin':
                    return

        # =====================
        # EXIT
        # =====================
        elif pilihan == '3':
            print("Terima kasih telah menggunakan GeoEstate!")
            break

        else:
            print("\nOpsi tidak valid, silakan coba lagi.")
            input("Tekan ENTER untuk kembali ke halaman awal...")



if __name__ == "__main__":
    loading()
    main()