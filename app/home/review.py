import pandas as pd
import os

FILE_NAME = "reviews.csv"

# Load Data
def load_data():
    if not os.path.exists(FILE_NAME):
        return pd.DataFrame(columns=["user_id", "property_id", "rating", "review_text"])
    return pd.read_csv(FILE_NAME)

# Simpan Data
def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# Tambah Review
def add_review(user_id, property_id, rating, review_text):
    df = load_data()

    new_review = {
        "user_id": user_id,
        "property_id": property_id,
        "rating": rating,
        "review_text": review_text
    }

    df = pd.concat([df, pd.DataFrame([new_review])], ignore_index=True)
    save_data(df)

    print("Review berhasil ditambahkan!")

# Tampilkan Review Properti
def show_reviews(property_id):
    df = load_data()
    reviews = df[df["property_id"] == property_id]

    if reviews.empty:
        print("Belum ada review untuk properti ini.")
        return

    for _, row in reviews.iterrows():
        print(f"- Rating: {row['rating']}/5")
        print(f"  Ulasan: {row['review_text']}")
        print()

# Hitung Rating Rata-rata
def average_rating(property_id):
    df = load_data()
    reviews = df[df["property_id"] == property_id]

    if reviews.empty:
        return 0

    return round(reviews["rating"].mean(), 2)

# Program
while True:
    print("=== Menu Review Properti ===")
    print("1. Tambah Review")
    print("2. Lihat Review Properti")
    print("3. Lihat Rating Rata-rata")
    print("4. Keluar")

    pilihan = input("Pilih menu (1-4): ")

    if pilihan == "1":
        user_id = int(input("Masukkan User ID: "))
        property_id = int(input("Masukkan Property ID: "))
        rating = int(input("Masukkan Rating (1-5): "))
        review_text = input("Masukkan Ulasan: ")

        add_review(user_id, property_id, rating, review_text)

    elif pilihan == "2":
        property_id = int(input("Masukkan Property ID: "))
        show_reviews(property_id)

    elif pilihan == "3":
        property_id = int(input("Masukkan Property ID: "))
        avg = average_rating(property_id)
        print(f"Rating rata-rata properti {property_id}: {avg}\n")

    elif pilihan == "4":
        print("Terima kasih telah menggunakan aplikasi.")
        break

    else:
        print("Pilihan tidak valid.\n")