from app.auth.register import register
from app.auth.login import login
from app.home.home_buyer import home_buyer
from app.home.home_seller import home_seller

def main():
    while True:
        print("=== GeoEstate ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        pilihan = input("Pilih opsi (1/2/3): ")

        if pilihan == '1':
            register()
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
        elif pilihan == '3':
            print("Terima kasih telah menggunakan GeoEstate!")
            break
        else:
            print("Opsi tidak valid, silakan coba lagi.\n")

if __name__ == "__main__":
    main()