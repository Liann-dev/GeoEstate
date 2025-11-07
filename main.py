from app.auth.register import register
from app.auth.login import login


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
            if login():
                print("Selamat datang di GeoEstate!")
                break
        elif pilihan == '3':
            print("Terima kasih telah menggunakan GeoEstate!")
            break
        else:
            print("Opsi tidak valid, silakan coba lagi.\n")

if __name__ == "__main__":
    main()