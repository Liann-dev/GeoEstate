import csv
import os
from app.home.about import about
from app.home.profile import profile
from app.home.properties import lihat_properti
from app.home.information import info
from app.home.detail_properti import detail_properti
from app.home.review_buyer import buyer_review
from app.features.feedback import collect_feedback
from app.features.merchant_register import merchant_registration_menu


FILE_PROPERTI = 'data/properti.csv'

def load_properties():
    data = []
    if os.path.exists(FILE_PROPERTI):
        with open(FILE_PROPERTI, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    return data

def home_user(username):
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
                print(f" | ID: {p['id']} {' '*26}|")
                print(f" +--------------------------------------+")
                count += 1
        
        print("----------------------------------------")
        
  
        print(" [L] Lihat Semua Properti")
        print(" [P] Profil Saya")
        print(" [T] Tentang GeoEstate")
        print(" [I] Informasi Umum")
        print(" [C] Cari Properti")
        print(" [U] Ulasan Properti (Review)")
        print(" [F] Feedback")
        print(" [M] Daftarkan Sebagai Merchant")
        print(" [K] Keluar / Logout")
        print("========================================")
        print(" KETIK: Huruf menu atau Angka ID Properti")
        
        pilihan = input(">> ").lower() 

            
        if pilihan == 'l':  # L = Lihat Semua
            lihat_properti(username)
        elif pilihan == 'p':  # P = Profil
            profile(username)
        elif pilihan == 't':  # T = Tentang
            about()
        elif pilihan == 'k':  # K = Keluar
            print("\nTerima kasih telah menggunakan GeoEstate. Sampai jumpa lagi!")
            input("Tekan ENTER untuk kembali ke halaman awal...")
            print("\n" * 25)
            return
        elif pilihan == 'i':  # I = Informasi
            info()
        elif pilihan == 'u':  # U = Ulasan
            buyer_review(username)
        elif pilihan == 'f':  # F = Feedback
            collect_feedback(username, 'user')
        elif pilihan == 'm':  # M = Merchant
            merchant_registration_menu(username)
        elif pilihan  == 'c':
            cari = input("Masukkan kata kunci lokasi atau nama properti: ").lower()
            
            hasil_cari = [item for item in semua_properti if cari in item['nama'].lower() or cari in item['lokasi'].lower()]
            
            print("\n=== Hasil Pencarian ===")
            if not hasil_cari:
                print("Tidak ada properti yang sesuai dengan pencarian Anda.")
            else:
                for p in hasil_cari:
                    harga_txt = f"Rp {int(p['harga']):,}"
                    print(f" +--------------------------------------+")
                    print(f" | 🏠 {p['nama']:<32} |")
                    print(f" | 📍 {p['lokasi']:<32} |")
                    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
                    print(f" | ID: {p['id']} {' '*26}|")
                    print(f" +--------------------------------------+")
            input("Tekan ENTER untuk kembali...")
            

        else:
          
            item_pilih = next((item for item in semua_properti if item['id'] == pilihan), None)
            
            if item_pilih:
              detail_properti(username,item_pilih)
            else:
                print(f"\n[!] Menu '{pilihan}' tidak dikenali atau ID Properti tidak ditemukan.")
                input("Tekan ENTER untuk coba lagi...")