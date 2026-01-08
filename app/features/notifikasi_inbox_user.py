import csv

from app.home.profile import profile
from app.features.chat import menu_chat
from app.features.jadwal_survey import lihat_jadwal_survey

NOTIF_FILE = "data/notifikasi.csv"

FIELDNAMES = ["id", "username", "role", "pesan", "status", "timestamp", "redirect"]


# =========================
# HAPUS NOTIFIKASI
# =========================
def menu_hapus_notifikasi(username, semua, user_notif):
    print("\n=== HAPUS NOTIFIKASI ===")
    print("1. Hapus Notifikasi Tertentu")
    print("2. Hapus Semua Notifikasi")
    print("0. Batal")

    pilih = input("Pilih opsi: ").strip()

    if pilih == "0":
        return semua

    # ===== HAPUS SATU =====
    if pilih == "1":
        nomor = input("Masukkan nomor notifikasi: ").strip()
        if not nomor.isdigit():
            print("❌ Input tidak valid.")
            input("ENTER...")
            return semua

        idx = int(nomor) - 1
        if idx < 0 or idx >= len(user_notif):
            print("❌ Nomor tidak ditemukan.")
            input("ENTER...")
            return semua

        notif_id = user_notif[idx]["id"]
        semua = [n for n in semua if n["id"] != notif_id]

        print("🗑️  Notifikasi dihapus.")
        input("ENTER...")
        return semua

    # ===== HAPUS SEMUA =====
    if pilih == "2":
        if input("Yakin hapus semua? (y/n): ").lower() != "y":
            print("❎ Dibatalkan.")
            input("ENTER...")
            return semua

        semua = [n for n in semua if n["username"] != username]
        print("🗑️ Semua notifikasi dihapus.")
        input("ENTER...")
        return semua

    print("❌ Pilihan tidak valid.")
    input("ENTER...")
    return semua


# =========================
# INBOX NOTIFIKASI
# =========================
def tampilkan_notifikasi_inbox(username):
    while True:
        with open(NOTIF_FILE, newline="", encoding="utf-8") as f:
            semua = list(csv.DictReader(f))

        user_notif = [n for n in semua if n["username"] == username]

        print("\n========== NOTIFIKASI INBOX ==========\n")

        if not user_notif:
            print("Tidak ada notifikasi.")
            input("ENTER untuk kembali...")
            return

        for i, n in enumerate(user_notif, 1):
            status = "🔔" if n["status"] == "unread" else "✓"
            print(f"{i}. {status} {n['pesan']}")

        print("\nPilih nomor notifikasi")
        print("[H] Hapus Notifikasi")
        print("[0] Kembali")

        pilih = input(">> ").strip().lower()

        # ===== KEMBALI =====
        if pilih == "0":
            return

        # ===== MENU HAPUS =====
        if pilih == "h":
            semua = menu_hapus_notifikasi(username, semua, user_notif)

            with open(NOTIF_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()
                writer.writerows(semua)
            continue

        # ===== PILIH NOTIF =====
        if not pilih.isdigit():
            print("❌ Input tidak valid.")
            input("ENTER...")
            continue

        idx = int(pilih) - 1
        if idx < 0 or idx >= len(user_notif):
            print("❌ Nomor tidak ditemukan.")
            input("ENTER...")
            continue

        notif = user_notif[idx]
        target = notif.get("redirect", "-")

        # ===== REDIRECT =====
        if target == "profile":
            profile(username)

        elif target == "jadwal_survey":
            lihat_jadwal_survey(username)

        elif target == "chat":
            menu_chat(username)

        elif target == "transaksi_seller":
            from app.features.transaksi_penjual import menu_kelola_pesanan
            menu_kelola_pesanan(username)

        elif target == "transaksi_buyer":
            print("\nℹ️  Halaman transaksi buyer belum tersedia.")
            input("ENTER...")
            continue

        else:
            print("ℹ️  Notifikasi ini belum memiliki halaman tujuan.")
            input("ENTER...")
            continue

        # ===== MARK AS READ =====
        for n in semua:
            if n["id"] == notif["id"]:
                n["status"] = "read"

        with open(NOTIF_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(semua)

        return
