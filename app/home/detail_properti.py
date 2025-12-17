import os
import time

def detail_properti(p):
  
    os.system('cls' if os.name == 'nt' else 'clear')

    harga_txt = f"Rp {int(p['harga']):,}" 
    print("\n" * 2)
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
        print("\n--- CHECKOUT ---")
        print(f"Item  : {p['nama']}")
        print(f"Harga : {harga_txt}")
        konfirm = input("Ketik 'BELI' untuk konfirmasi: ")
        
        if konfirm == "BELI":
            print("\n✅ Pembayaran Berhasil! Aset sedang diproses.")
        else:
            print("\nTransaksi dibatalkan.")
        input("Tekan ENTER untuk kembali...")
    
    elif pilihan == '0':
        return 