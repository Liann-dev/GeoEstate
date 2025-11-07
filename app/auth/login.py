from app.auth import register

#login
def login():
    kesempatan = 3
    while kesempatan > 0:
        print("--- Login GeoEstate ---")
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")
        for user in register.users:
            if user['username'] == username and user['password'] == password:
                print("Login berhasil!\n")
                return True
        kesempatan -= 1
        print(f"Username atau Password salah. Kesempatan tersisa: {kesempatan}\n")
    print("Login gagal. Silakan coba lagi nanti.\n")
    return False