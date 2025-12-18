def collect_feedback():

    print("Silakan ketik feedback Anda di bawah ini:")
    
    # Mengambil input feedback dari pengguna
    user_feedback = input("Feedback: ")
    
    try:
        # Menyimpan feedback ke file 'user_feedback.txt'
        with open("user_feedback.txt", "a") as file:
            file.write(user_feedback + "\\n") # Menambahkan feedback dan baris baru
        print("\\nFeedback Anda berhasil disimpan. Terima kasih!")
        
    except IOError as e:
        # Menangani error jika file tidak dapat ditulis
        print(f"Terjadi kesalahan saat menulis ke file: {e}")

collect_feedback()