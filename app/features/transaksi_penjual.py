import csv
import os
from datetime import datetime, timedelta
from app.features.notifikasi_helper import simpan_notifikasi
from app.features.chat import buka_chat, normalize_session
from app.features.booking_history import simpan_booking_history

FILE_TRANSAKSI = "data/transaksi.csv"
FILE_PROPERTI = "data/properti.csv"
FILE_RIWAYAT = "data/properti_dibeli.csv"
FILE_BOOKING = "data/booking.csv"


# ================= UTIL =================

def baca_data_csv():
    if not os.path.exists(FILE_TRANSAKSI):
        return []
    with open(FILE_TRANSAKSI, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def simpan_perubahan_csv(data):
    if not data:
        return
    with open(FILE_TRANSAKSI, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def update_status_properti(id_properti, status_baru):
    if not os.path.exists(FILE_PROPERTI):
        return

    with open(FILE_PROPERTI, newline="", encoding="utf-8") as f:
        data = list(csv.DictReader(f))

    for p in data:
        if p["id"] == id_properti:
            p["status"] = status_baru
            break

    with open(FILE_PROPERTI, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


# ================= BOOKING DATE =================

def get_jadwal_terakhir(id_transaksi):
    if not os.path.exists(FILE_BOOKING):
        return None

    terakhir = None
    with open(FILE_BOOKING, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["id_transaksi"] == id_transaksi:
                terakhir = r["tanggal"]
    return terakhir


def get_extend_count(id_transaksi):
    if not os.path.exists(FILE_BOOKING):
        return 0

    jadwal = set()
    with open(FILE_BOOKING, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["id_transaksi"] == id_transaksi:
                jadwal.add(r["tanggal"])
    return max(0, len(jadwal) - 1)


def simpan_booking_awal(id_transaksi, tanggal):
    tulis_header = not os.path.exists(FILE_BOOKING)
    with open(FILE_BOOKING, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id_transaksi", "tanggal"])
        if tulis_header:
            writer.writeheader()
        writer.writerow({
            "id_transaksi": id_transaksi,
            "tanggal": tanggal
        })


# ================= AUTO EXPIRED =================

def auto_expire_booking():
    semua = baca_data_csv()
    sekarang = datetime.now()
    berubah = False

    for r in semua:
        if r["status"] not in ("Menunggu Konfirmasi", "Booked"):
            continue

        tanggal_booking = datetime.strptime(r["tanggal"], "%Y-%m-%d %H:%M:%S")

        batas = 2 if r["status"] == "Menunggu Konfirmasi" else 7

        if sekarang - tanggal_booking > timedelta(days=batas):
            r["status"] = "Dibatalkan"
            update_status_properti(r["id_properti"], "available")
            berubah = True

            simpan_booking_history(
                r["id_transaksi"],
                aksi="EXPIRED",
                oleh="system",
                tanggal_lama=r["tanggal"][:10],
                tanggal_baru="-"
            )

            simpan_notifikasi(
                r["username_pembeli"],
                "user",
                f"Booking properti '{r['nama_properti']}' dibatalkan otomatis (expired)",
                redirect="transaksi_buyer"
            )

    if berubah:
        simpan_perubahan_csv(semua)


# ================= UPDATE STATUS =================

def update_status_pesanan(penjual_login):
    id_trx = input("\nMasukkan ID Transaksi: ").strip()
    semua = baca_data_csv()

    trx = next(
        (r for r in semua if r["id_transaksi"] == id_trx and r["session"] == penjual_login),
        None
    )

    if not trx:
        print("❌ Transaksi tidak ditemukan.")
        input("ENTER...")
        return

    status = trx["status"]
    pembeli = trx["username_pembeli"]
    properti = trx["nama_properti"]

    if status in ("Sold", "Lunas / Selesai", "Dibatalkan"):
        print("🔒 Status sudah final.")
        input("ENTER...")
        return

    # ===== MENUNGGU KONFIRMASI =====
    if status == "Menunggu Konfirmasi":
        print("1. ✅ Terima Booking")
        print("2. ❌ Tolak Booking")
        pilih = input(">> ")

        if pilih == "1":
            trx["status"] = "Booked"

            tanggal_awal = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            simpan_booking_awal(id_trx, tanggal_awal)

            simpan_booking_history(
                id_trx,
                aksi="SET_BOOKING",
                oleh="seller",
                tanggal_lama="-",
                tanggal_baru=tanggal_awal
            )

            update_status_properti(trx["id_properti"], "booked")

            simpan_notifikasi(
                pembeli, "user",
                f"Booking properti '{properti}' disetujui (berlaku s/d {tanggal_awal})"
            )

        elif pilih == "2":
            trx["status"] = "Dibatalkan"
            update_status_properti(trx["id_properti"], "available")

            simpan_booking_history(
                id_trx, "CANCEL", "seller",
                trx["tanggal"][:10], "-"
            )

    # ===== BOOKED =====
    elif status == "Booked":
        print("1. ❌ Batalkan Booking")
        print("2. ⏰ Perpanjang Waktu")
        pilih = input(">> ")

        if pilih == "1":
            trx["status"] = "Dibatalkan"
            update_status_properti(trx["id_properti"], "available")

            simpan_booking_history(
                id_trx, "CANCEL", "seller",
                trx["tanggal"][:10], "-"
            )

        elif pilih == "2":
            extend = get_extend_count(id_trx)
            if extend >= 3:
                print("❌ Maksimal perpanjangan 3x.")
                input("ENTER...")
                return

            tanggal_lama = get_jadwal_terakhir(id_trx)
            tanggal_baru = (
                datetime.strptime(tanggal_lama, "%Y-%m-%d") + timedelta(days=7)
            ).strftime("%Y-%m-%d")

            simpan_booking_awal(id_trx, tanggal_baru)

            simpan_booking_history(
                id_trx, "EXTEND", "seller",
                tanggal_lama, tanggal_baru
            )

            simpan_notifikasi(
                pembeli, "user",
                f"Booking properti '{properti}' diperpanjang hingga {tanggal_baru}"
            )

    simpan_perubahan_csv(semua)
    print("✅ Status berhasil diperbarui.")
    input("ENTER...")

def menu_kelola_pesanan(user_active):
    auto_expire_booking()

    while True:
        transaksi = baca_data_csv()
        data = [t for t in transaksi if t["session"] == user_active]

        print("\n" * 50)
        print("=" * 110)
        print("📦 KELOLA BOOKING SELLER")
        print("=" * 110)

        if not data:
            print("Belum ada booking.")
        else:
            print(f"{'ID':<10} {'BUYER':<12} {'PROPERTI':<20} {'TANGGAL':<14} {'STATUS'}")
            print("-" * 110)

            for t in data:
                jadwal = get_jadwal_terakhir(t["id_transaksi"]) or "-"
                extend = get_extend_count(t["id_transaksi"])
                print(
                    f"{t['id_transaksi']:<10} "
                    f"{t['username_pembeli']:<12} "
                    f"{t['nama_properti'][:18]:<20} "
                    f"{jadwal} ({extend}/3) "
                    f"{t['status']}"
                )

        print("\n[ OPSI ]")
        print("1. 🔄 Update Status Booking")
        print("2. 💬 Chat Buyer")
        print("3. 📜 Lihat Riwayat Booking")
        print("0. 🔙 Kembali")

        pilih = input(">> ").strip()

        if pilih == "1":
            update_status_pesanan(user_active)

        elif pilih == "2":
            id_trx = input("ID Transaksi: ").strip()
            for t in data:
                if t["id_transaksi"] == id_trx:
                    session = normalize_session(user_active, t["username_pembeli"])
                    buka_chat(user_active, session, t["username_pembeli"])
                    break

        elif pilih == "3":
            id_trx = input("Masukkan ID Transaksi: ").strip()
            if id_trx:
                lihat_history_booking(id_trx)

        elif pilih == "0":
            return

def sedang_dalam_transaksi(username, id_properti):
    """
    Mengecek apakah user masih memiliki transaksi aktif
    untuk properti tertentu
    """
    if not os.path.exists(FILE_TRANSAKSI):
        return False

    with open(FILE_TRANSAKSI, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (
                row["username_pembeli"] == username
                and row["id_properti"] == id_properti
                and row["status"] not in ("Dibatalkan", "Sold", "Lunas / Selesai")
            ):
                return True
    return False

def lihat_history_booking(id_transaksi):
    import csv, os
    from app.features.booking_history import FILE_HISTORY

    print("\n📜 RIWAYAT PERUBAHAN BOOKING")
    print("-" * 60)

    if not os.path.exists(FILE_HISTORY):
        print("Belum ada riwayat booking.")
        input("ENTER...")
        return

    found = False

    with open(FILE_HISTORY, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if "id_transaksi" not in reader.fieldnames:
            print("❌ Struktur file history tidak valid.")
            print("💡 Hapus data/booking_history.csv lalu ulangi.")
            input("ENTER...")
            return

        for r in reader:
            if r["id_transaksi"] == id_transaksi:
                print(
                    f"[{r['waktu']}] "
                    f"{r['aksi']} | "
                    f"{r['tanggal_lama']} → {r['tanggal_baru']} "
                    f"({r['oleh']})"
                )
                found = True

    if not found:
        print("Tidak ada riwayat untuk transaksi ini.")

    input("\nENTER...")
