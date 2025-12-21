import csv
import os

FEEDBACK_FILE = "data/user_feedback.csv"

def lihat_feedback():
    print("\n=== Feedback Pengguna ===")

    if not os.path.exists(FEEDBACK_FILE):
        print("Belum ada feedback yang masuk.\n")
        return

    with open(FEEDBACK_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = list(csv.DictReader(file))

        if not reader:
            print("Belum ada feedback yang masuk.\n")
            return

        print("-" * 120)
        print(
            f"{'No':<4}"
            f"{'Waktu':<20}"
            f"{'Username':<12}"
            f"{'Role':<10}"
            f"{'Feedback'}"
        )
        print("-" * 120)

        for i, row in enumerate(reader, start=1):
            print(
                f"{i:<4}"
                f"{row['timestamp']:<20}"
                f"{row['username']:<12}"
                f"{row['role']:<10}"
                f"{row['feedback']}"
            )

        print("-" * 120)
        input("Tekan ENTER untuk kembali...")