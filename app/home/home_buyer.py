from app.home.about import about
from app.home.profile import profile
from app.home.properties import lihat_properti
from app.home.help import bantuan

def home_buyer(username):
    while True:
        print(f"\n=== GeoEstate Home (Pembeli) ===")
        print(f"Halo, {username} 👋")
        print("1. Tentang GeoEstate")
        print("2. Profil Saya")
        print("3. Lihat Properti")
        print("4. Bantuan")
        print("5. Logout")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == '1':
            about()
        elif pilihan == '2':
            profile(username)
        elif pilihan == '3':
            lihat_properti()
        elif pilihan == '4':
            bantuan()
        elif pilihan == '5':
            print("Logout berhasil. Sampai jumpa!\n")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")