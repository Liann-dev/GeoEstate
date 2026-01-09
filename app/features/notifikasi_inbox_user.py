import csv
import os

from app.home.profile import profile
from app.features.chat import menu_chat
from app.features.jadwal_survey import lihat_jadwal_survey
from app.home.riwayat_transaksi_terpadu import riwayat_transaksi_terpadu
from app.features.transaksi_penjual import menu_kelola_pesanan
from app.Utils.animation import loading_seller_transition
from app.features.kelola_survey import menu_kelola_survei

NOTIF_FILE = "data/notifikasi.csv"

FIELDNAMES = [
    "id",
    "username",
    "role",
    "pesan",
    "status",
    "timestamp",
    "redirect"
]


# =========================
# UTIL CSV
# =========================
def load_notifikasi():
    if not os.path.exists(NOTIF_FILE):
        return []
    with open(NOTIF_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_notifikasi(data):
    with open(NOTIF_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)


# =========================
# HAPUS NOTIFIKASI
# =========================
def menu_hapus_notifikasi(username, semua, user_notif):
    print("\n=== HAPUS NOTIFIKASI ===")
    print("1. Hapus Notifikasi Tertentu")
    print("2. Hapus Semua Notifikasi")
    print("0. Batal")

    pilih = input("Pilih: ").strip()

    # BATAL
    if pilih == "0":
        return semua

    # ===== HAPUS SATU =====
    if pilih == "1":
        nomor = input("Nomor notifikasi: ").strip()

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
        konfirmasi = input("Yakin hapus semua notifikasi? (y/n): ").lower()
        if konfirmasi != "y":
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
        semua = load_notifikasi()
        user_notif = [n for n in semua if n["username"] == username]

        print("\n========== NOTIFIKASI INBOX ==========\n")

        if not user_notif:
            print("Tidak ada notifikasi.")
            input("ENTER untuk kembali...")
            return

        for i, n in enumerate(user_notif, 1):
            icon = "🔔" if n["status"] == "unread" else "✓"
            print(f"{i}. {icon} {n['pesan']}")

        print("\nPilih nomor notifikasi")
        print("[H] Hapus Notifikasi")
        print("[0] Kembali")

        pilih = input(">> ").strip().lower()

        # ===== KEMBALI =====
        if pilih == "0":
            return

        # ===== HAPUS =====
        if pilih == "h":
            semua = menu_hapus_notifikasi(username, semua, user_notif)
            save_notifikasi(semua)
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

        # ===== MARK AS READ =====
        for n in semua:
            if n["id"] == notif["id"]:
                n["status"] = "read"

        save_notifikasi(semua)

        # ===== REDIRECT =====
        if target == "profile":
            profile(username)

        elif target == "chat":
            menu_chat(username)

        elif target == "transaksi_seller":
            loading_seller_transition()
            menu_kelola_pesanan(username)

        elif target == "transaksi_buyer":
            riwayat_transaksi_terpadu(username)

        elif target == "survey_buyer":
            lihat_jadwal_survey(username)

        elif target == "survey_seller":
            loading_seller_transition()
            menu_kelola_survei(username)

        else:
            print("\nℹ️  Notifikasi ini tidak memiliki halaman tujuan.")
            input("ENTER...")
