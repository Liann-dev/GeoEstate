import csv
import os
from app.home.profile import profile
from app.home.properties import pilih_properti
from app.home.information import info
from app.home.detail_properti import detail_properti
from app.home.seller_menu import seller_menu
from app.home.review_seller import seller_review
from app.features.chat import menu_chat
from app.features.wishlist import menu_wishlist
from app.features.feedback import collect_feedback



FILE_PROPERTI = 'data/properti.csv'

def load_properties():
    data = []
    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    return data

def home_seller(username):
    while True:
        semua_properti = load_properties()
        

        print("\n" * 50) 
        print(f" Halo, {username} 👋")
        print("========================================")
 
        print(" 🔥 REKOMENDASI UNTUKMU:")
        if not semua_properti:
            print("    (Belum ada data properti)")
        else:
            limit = 3
            count = 0
            for p in semua_properti:
                if count >= limit: break
                harga_txt = f"Rp {int(p['harga']):,}"
                print(f" +--------------------------------------+")
                print(f" | 🏠 {p['nama']:<32} |")
                print(f" | 📍 {p['lokasi']:<32} |")
                print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
                print(f" | ID: {p['id']} {' '*30}|")
                print(f" +--------------------------------------+")
                count += 1
        
        print("----------------------------------------")
        
  
        print(" [L] Lihat Semua Properti")
        print(" [P] Profil Saya")
        print(" [I] Informasi Umum")
        print(" [C] Kirim Pesan (Chat)")
        print(" [U] Ulasan Saya")
        print(" [F] Feedback")
        print(" [W] Wishlist")
        print(" [M] Menu Seller")
        print(" [K] Keluar / Logout")
        print("========================================")
        print(" KETIK: Huruf menu atau Angka ID Properti")
        
        pilihan = input(">> ").lower() 

            
        if pilihan == 'l':  # L = Lihat Semua
            pilih_properti(username)
        elif pilihan == 'p':  # P = Profil
            profile(username)
        elif pilihan == 'k':  # K = Keluar
            print("\nTerima kasih telah menggunakan GeoEstate. Sampai jumpa lagi!")
            input("Tekan ENTER untuk kembali ke halaman awal...")
            print("\n" * 25)
            return
        elif pilihan == 'i':  # I = Informasi
            info()
        elif pilihan == 'u':  # U = Ulasan
            seller_review(username)
        elif pilihan == 'c':  # C = Chat
            menu_chat(username)
        elif pilihan == 'f':  # F = Feedback
            collect_feedback(username, 'seller')
        elif pilihan == 'w':  # W = Wishlist
            menu_wishlist(username)
        elif pilihan == 'm':  # M = seller
            seller_menu(username)
            
        else:
          
            item_pilih = next((item for item in semua_properti if item['id'] == pilihan), None)
            
            if item_pilih:
              detail_properti(username,item_pilih)
            else:
                print(f"\n[!] Menu '{pilihan}' tidak dikenali atau ID Properti tidak ditemukan.")
                input("Tekan ENTER untuk coba lagi...")