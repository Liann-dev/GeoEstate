import csv
from datetime import datetime
import os

def collect_feedback(username, role):
    """
    Mengumpulkan feedback dan menyimpannya ke CSV
    berdasarkan username dan role pengguna.
    """
    print("\nSilakan ketik feedback Anda di bawah ini:")
    user_feedback = input("Feedback: ")

    file_name = "data/user_feedback.csv"
    file_exists = os.path.isfile(file_name)

    try:
        with open(file_name, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Header hanya ditulis sekali
            if not file_exists:
                writer.writerow(["timestamp", "username", "role", "feedback"])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                username,
                role,
                user_feedback
            ])

        print("\nFeedback Anda berhasil disimpan. Terima kasih!")
        input("Tekan ENTER untuk kembali...")

    except IOError as e:
        print(f"Terjadi kesalahan saat menulis ke file: {e}")
        input("Tekan ENTER untuk coba lagi...")