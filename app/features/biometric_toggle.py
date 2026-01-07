import csv
import os

FILE_BIOMETRIC = "data/biometric_toggle.csv"

def ambil_status_biometrik(username):
    if not os.path.exists(FILE_BIOMETRIC):
        return "OFF"

    with open(FILE_BIOMETRIC, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return row['toggle']

    return "OFF"

def simpan_toggle_biometrik(username, status_baru):
    data = []
    ditemukan = False

    if os.path.exists(FILE_BIOMETRIC):
        with open(FILE_BIOMETRIC, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    row['toggle'] = status_baru
                    ditemukan = True
                data.append(row)

    if not ditemukan:
        data.append({'username': username, 'toggle': status_baru})

    with open(FILE_BIOMETRIC, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'toggle'])
        writer.writeheader()
        writer.writerows(data)

def toggle_biometrik(username):
    status = ambil_status_biometrik(username)
    
    if status == "OFF":
        while True:
            konfirmasi = input("Nyalakan login biometrik? (y/n): ").lower()
            if konfirmasi == "y":
                simpan_toggle_biometrik(username, "ON")
                print("Biometrik berhasil dinyalakan!")
                break
            elif konfirmasi == "n":
                print("Biometrik tetap dimatikan.")
                break
            else:
                print("Pilihan tidak valid!\n")
                continue
            
    else:  # status == "ON"
        while True:
            konfirmasi = input("Matikan login biometrik? (y/n): ").lower()
            if konfirmasi == "y":
                simpan_toggle_biometrik(username, "OFF")
                print("Biometrik berhasil dimatikan!")
                break
            elif konfirmasi == "n":
                print("Biometrik tetap dinyalakan.")
                break
            else:
                print("Pilihan tidak valid!\n")
                continue
