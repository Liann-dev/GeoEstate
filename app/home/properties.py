def lihat_properti():
    properti = [
        {"nama": "Villa Bandung", "lokasi": "Lembang", "harga": 950000000},
        {"nama": "Rumah Modern", "lokasi": "Dago", "harga": 1250000000},
        {"nama": "Apartemen SkyView", "lokasi": "Cihampelas", "harga": 850000000},
    ]

    print("\n=== Daftar Properti GeoEstate ===")
    for p in properti:
        print(f"{p['nama']} - {p['lokasi']} - Rp {p['harga']}")
    print()
