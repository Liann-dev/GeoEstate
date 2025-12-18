import csv

FILE_USERS = "data/users.csv"

def verifikasi_user(username):
    users = []

    with open(FILE_USERS, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                row['user_verified'] = "True"
            users.append(row)

    with open(FILE_USERS, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

    print("Akun pengguna berhasil diverifikasi.")