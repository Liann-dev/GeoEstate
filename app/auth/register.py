users = []

def register():
    print("--- Register GeoEstate ---")
    username = input("Masukkan Username: ")

    # Cek apakah username sudah ada
    for user in users:
        if user['username'] == username:
            print("Username sudah dipakai, silakan coba lagi.")
            return False

    password = input("Masukkan Password: ")

    # Pilih peran (Penjual / Pembeli)
    print("Pilih peran Anda:")
    print("1. Pembeli")
    print("2. Penjual")
    role_choice = input("Masukkan pilihan (1/2): ")

    if role_choice == '1':
        role = "pembeli"
    elif role_choice == '2':
        role = "penjual"
    else:
        print("Pilihan tidak valid, registrasi dibatalkan.")
        return False

    users.append({
        'username': username,
        'password': password,
        'role': role
    })

    print(f"Register berhasil sebagai {role}!\n")
    return users