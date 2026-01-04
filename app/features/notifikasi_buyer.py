import csv

CHAT_FILE = "data/chat.csv"
SURVEY_FILE = "data/jadwalsurvey.csv"
TRANSAKSI_FILE = "data/transaksi.csv"

def notifikasi_buyer(username):
    notifikasi = []

    # ================= CHAT DIBALAS SELLER =================
    with open(CHAT_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["receiver"] == username:
                notifikasi.append(
                    f"Pesan baru dari seller {row['sender']}"
                )

    # ================= TRANSAKSI / BOOKING =================
    with open(TRANSAKSI_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username_pembeli"] == username:

                if row["status"] in [
                    "Menunggu Konfirmasi",
                    "Perpanjang Waktu",
                    "Dibatalkan"
                ]:
                    notifikasi.append(
                        f"Status booking '{row['nama_properti']}' : {row['status']}"
                    )

                if row["status"] == "Lunas / Selesai":
                    notifikasi.append(
                        f"Properti '{row['nama_properti']}' berhasil dibeli"
                    )

    # ================= JADWAL SURVEY =================
    with open(SURVEY_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["pembeli"] == username and row["status"] == "Approve":
                notifikasi.append(
                    f"Jadwal survei '{row['nama_properti']}' disetujui seller"
                )

    return notifikasi