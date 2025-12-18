import os
import time
from app.features.checkout import checkout


def detail_properti(username,p):
  

    harga_txt = f"Rp {int(p['harga']):,}" 
    print("\n" * 50)
    print("========================================")
    print("           DETAIL PROPERTI             ")
    print("========================================")
    print(f" +--------------------------------------+")
    print(f" | 🏠 {p['nama']:<32} |")
    print(f" | 📍 {p['lokasi']:<32} |")
    print(f" | 💰 {harga_txt:<20} {p['kategori']:>11} |")
    print(f" | ID: {p['id']} {' '*26}|")
    print(f" +--------------------------------------+")
    print(" | Status: ✅ Terverifikasi             |")
    print(f" | Penjual: {p['penjual']:<27} |")
    print(f" +--------------------------------------+")
    

    print("\n[ OPSI ]")
    print("1. 📅 Jadwalkan Survei")
    print("2. 🛒 Beli Sekarang (Checkout)")
    print("0. 🔙 Kembali")
    print("----------------------------------------")
    
    pilihan = input(">> Pilih opsi: ")
    
    if pilihan == '1':
       print("COMING SOON: Fitur Jadwalkan Survei Properti!")
       time.sleep(2)
       input("Tekan ENTER untuk kembali...")
       return

        
    elif pilihan == '2':
        checkout(username,p)
    elif pilihan == '0':
        return 