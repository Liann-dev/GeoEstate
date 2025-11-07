users = []

def register():
    print("--- Register GeoEstate ---")
    username = input("Masukkan Username: ")

    for user in users:
        if user['username'] == username:
            print("Username sudah dipakai, silakan coba lagi.")
            return False

    password = input("Masukkan Password: ")

    users.append({'username': username, 'password': password})
    print("Register berhasil!\n")
    return users