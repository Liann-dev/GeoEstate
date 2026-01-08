import os
import csv
from datetime import datetime

FILE_USERS = "data/users.csv"
FILE_FEEDBACK = "data/user_feedback.csv"

def collect_feedback(username):
    print()
    user_data = None

    if os.path.exists(FILE_USERS):
        with open(FILE_USERS, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user["username"] == username:
                    user_data = user

    while True:
        user_feedback = input("Silakan ketik feedback Anda (Tekan ENTER untuk membatalkan): ")
        if not user_feedback:
            return   
        else:
            break

    with open(FILE_FEEDBACK, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_data['username'],
            user_data['role'],
            user_feedback
        ])

    print("\nFeedback Anda berhasil disimpan. Terima kasih!")
    input("Tekan ENTER untuk kembali...")