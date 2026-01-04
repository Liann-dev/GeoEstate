import csv

NOTIF_FILE = "data/notifikasi.csv"

def tampilkan_notifikasi_inbox(username):
    semua = []

    with open(NOTIF_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        semua = list(reader)

    user_notif = [n for n in semua if n["username"] == username]

    print("\n========== NOTIFIKASI INBOX ==========\n")

    if not user_notif:
        print("Tidak ada notifikasi.")
    else:
        for i, notif in enumerate(user_notif, 1):
            print(f"{i}. {notif['pesan']}")

    # ================= AUTO MARK AS READ =================
    for notif in semua:
        if notif["username"] == username and notif["status"] == "unread":
            notif["status"] = "read"

    with open(NOTIF_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "username", "role", "pesan", "status", "timestamp"]
        )
        writer.writeheader()
        writer.writerows(semua)

    print("\n[0] Kembali ke Menu Utama")
    input(">> ")