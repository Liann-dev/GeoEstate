import csv

def lihat_properti():
    print("\n=== Properti Tersedia ===")

    with open("data/properti.csv", mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for p in reader:
            if p['doc_verified'] == "True":
                print(f"{p['nama']} ({p['kategori']})")
                print(f"Lokasi: {p['lokasi']}")
                print(f"Harga : Rp {p['harga']}\n")