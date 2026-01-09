import time
import sys
# Import lebar juga biar sinkron ukuran loading bar-nya
from app.Utils.padding import pad_center as centerpadding, lebar 

def show_splash():
    print("\n" * 2) 

    print(centerpadding("G E O   E S T A T E"))
    print(centerpadding("Find Your Future"))
    
    print("\n") 

    print(centerpadding("Loading..."))
    

    padding_kiri = " " * int((lebar - 25) / 2) 
    total_loading = 22
    
    for i in range(total_loading + 1):
        time.sleep(0.07) 
        percent = int((i / total_loading) * 100)
        bar_isi = '█' * i
        bar_kosong = '░' * (total_loading - i)
        
        sys.stdout.write(f"\r{padding_kiri}[{bar_isi}{bar_kosong}] {percent}%")
        sys.stdout.flush()

    print("\n\n")

def show_onboarding():
  
    print("\n" * 20)
    print(centerpadding("[Page 1 of 3]"))
    print(centerpadding("========================================="))
    print(centerpadding("📍  TEMUKAN PROPERTI STRATEGIS ANDA"))
    print(centerpadding("========================================="))
    print(centerpadding("Akses properti terlengkap dengan"))
    print(centerpadding("pemetaan wilayah yang presisi."))
    print("\n" * 4)
    
   
    input(centerpadding(">> Tekan ENTER untuk lanjut..."))
    print("\n" * 20)


    print("\n" * 20)
    print(centerpadding("[Page 2 of 3]"))
    print(centerpadding("========================================="))
    print(centerpadding("🏠  INTERIOR SESUAI GAYA ANDA"))
    print(centerpadding("========================================="))
    print(centerpadding("Filter pencarian berdasarkan gaya"))
    print(centerpadding("arsitektur, luas ruangan, dan fasilitas."))
    print("\n" * 4)
    input(centerpadding(">> Tekan ENTER untuk lanjut..."))
    print("\n" * 20)

    print("\n" * 20)
    print(centerpadding("[Page 3 of 3]"))
    print(centerpadding("========================================="))
    print(centerpadding("🛡️  JUAL BELI AMAN DAN TERPERCAYA"))
    print(centerpadding("========================================="))
    print(centerpadding("Semua properti telah diverifikasi"))
    print(centerpadding("oleh tim legal GeoEstate."))
    print("\n" * 4)
    input(centerpadding(">> Tekan ENTER untuk Masuk ke Aplikasi..."))
    print("\n" * 20)

import time
import sys
import os

def loading_seller_transition():
    print("\n" * 2) 
    print(centerpadding("G E O   E S T A T E   |   B U S I N E S S"))
    print(centerpadding("Menyiapkan Portofolio Aset Anda..."))
    print("\n") 
    print(centerpadding("Membuka Dashboard Penjual..."))
    padding_kiri = " " * int((lebar - 25) / 2) 
    total_loading = 22
    
    for i in range(total_loading + 1):
        time.sleep(0.05)  
        percent = int((i / total_loading) * 100)
        bar_isi = '█' * i
        bar_kosong = '░' * (total_loading - i)
        sys.stdout.write(f"\r{padding_kiri}[{bar_isi}{bar_kosong}] {percent}%")
        sys.stdout.flush()

    print("\n\n") 
    time.sleep(0.5)

def loading_exit_seller():  
    print("\n" * 3) 
    print(centerpadding("G E O   E S T A T E   |   B U S I N E S S"))
    print(centerpadding("Menyiapkan Perubahan Data..."))
    print("\n") 
    print(centerpadding("Menutup Dasbor Penjual..."))
    padding_kiri = " " * int((lebar - 25) / 2) 
    total_loading = 22
    
    for i in range(total_loading + 1):
        time.sleep(0.03)  
        percent = int((i / total_loading) * 100)
        bar_isi = '█' * i
        bar_kosong = '░' * (total_loading - i)
        sys.stdout.write(f"\r{padding_kiri}[{bar_isi}{bar_kosong}] {percent}%")
        sys.stdout.flush()

    print("\n\n") 
    time.sleep(0.3)
    