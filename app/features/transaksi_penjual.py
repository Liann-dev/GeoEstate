import csv
import os
from datetime import datetime, timedelta
from app.features.notifikasi_helper import simpan_notifikasi
from app.features.chat import buka_chat, normalize_session

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


def sedang_dalam_transaksi(username, id_properti):
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


# ================= BOOKING DATE =================

def get_jadwal_terakhir(id_transaksi):
    if not os.path.exists(FILE_BOOKING):
        return None

    terakhir = None
    with open(FILE_BOOKING, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["id_transaksi"] == id_transaksi:
                terakhir = row["schedule"]
    return terakhir


def tambah_jadwal_booking(id_transaksi, tanggal, pembeli, penjual):
    with open(FILE_BOOKING, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([id_transaksi, tanggal, pembeli])
        writer.writerow([id_transaksi, tanggal, penjual])


def get_extend_count(id_transaksi):
    if not os.path.exists(FILE_BOOKING):
        return 0

    jadwal = set()
    with open(FILE_BOOKING, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["id_transaksi"] == id_transaksi:
                jadwal.add(row["schedule"])
    return len(jadwal)


# ================= TAMPILKAN PESANAN =================

def tampilkan_pesanan(penjual):
    semua = baca_data_csv()
    data = [t for t in semua if t["session"] == penjual]

    print("\n" * 50)
    print("=" * 110)
    print("📦 KELOLA BOOKING SELLER")
    print("=" * 110)

    if not data:
        print("Belum ada booking.")
        return []

    print(f"{'ID':<10} {'BUYER':<12} {'PROPERTI':<20} {'TANGGAL':<14} {'STATUS'}")
    print("-" * 110)

    for t in data:
        jadwal = get_jadwal_terakhir(t["id_transaksi"]) or t["tanggal"][:10]
        extend = get_extend_count(t["id_transaksi"])
        print(
            f"{t['id_transaksi']:<10} {t['username_pembeli']:<12} "
            f"{t['nama_properti'][:18]:<20} {jadwal} ({extend}/3) {t['status']}"
        )

    return data


# ================= UPDATE STATUS =================

def update_status_pesanan(penjual_login):
    id_trx = input("\nMasukkan ID Transaksi (ENTER batal): ").strip()
    if not id_trx:
        return

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

    # 🔒 STATUS FINAL
    if status in ("Sold", "Lunas / Selesai", "Dibatalkan"):
        print("🔒 Status transaksi sudah final dan tidak dapat diubah.")
        input("ENTER...")
        return

    pembeli = trx["username_pembeli"]
    properti = trx["nama_properti"]
    id_properti = trx["id_properti"]

    print("\n[ UPDATE STATUS ]")

    # ================= MENUNYA DIKUNCI SESUAI STATUS =================
    if status == "Menunggu Konfirmasi":
        print("1. ✅ Terima Booking")
        print("2. ❌ Tolak Booking")
        pilih = input(">> ").strip()

        if pilih == "1":
            for r in semua:
                if r["id_transaksi"] == id_trx:
                    r["status"] = "Booked"

            update_status_properti(id_properti, "booked")
            batalkan_booking_lain(id_properti, id_trx)

            simpan_notifikasi(
                pembeli, "user",
                f"Booking properti '{properti}' disetujui seller"
            )

        elif pilih == "2":
            for r in semua:
                if r["id_transaksi"] == id_trx:
                    r["status"] = "Dibatalkan"
                    if r["session"] == pembeli:
                        r["transaksi"] = "batal"

            update_status_properti(id_properti, "available")

            simpan_notifikasi(
                pembeli, "user",
                f"Booking properti '{properti}' ditolak seller"
            )
        else:
            print("❌ Pilihan tidak valid.")
            input("ENTER...")
            return

    elif status == "Booked":
        print("Buyer belum mengajukan pembelian.")
        print("1. ❌ Batalkan Booking")
        print("2. ⏰ Perpanjang Waktu")
        pilih = input(">> ").strip()

        if pilih == "1":
            for r in semua:
                if r["id_transaksi"] == id_trx:
                    r["status"] = "Dibatalkan"
                    if r["session"] == pembeli:
                        r["transaksi"] = "batal"

            update_status_properti(id_properti, "available")

            simpan_notifikasi(
                pembeli, "user",
                f"Booking properti '{properti}' dibatalkan seller"
            )

        elif pilih == "2":
            if get_extend_count(id_trx) >= 3:
                print("❌ Maksimal perpanjangan 3x.")
                input("ENTER...")
                return

            tanggal = input("Tanggal baru (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(tanggal, "%Y-%m-%d")
            except ValueError:
                print("❌ Format salah.")
                input("ENTER...")
                return

            tambah_jadwal_booking(id_trx, tanggal, pembeli, penjual_login)

            for r in semua:
                if r["id_transaksi"] == id_trx:
                    r["status"] = "Perpanjang Waktu"

            simpan_notifikasi(
                pembeli, "user",
                f"Booking properti '{properti}' diperpanjang hingga {tanggal}"
            )
        else:
            print("❌ Pilihan tidak valid.")
            input("ENTER...")
            return

    elif status == "Menunggu Pembayaran":
        print("1. 💰 Konfirmasi Pembelian")
        print("2. ❌ Batalkan Booking")
        print("3. ⏰ Perpanjang Waktu")
        pilih = input(">> ").strip()

        if pilih == "1":
            for r in semua:
                if r["id_transaksi"] == id_trx:
                    r["status"] = "Sold"
                    r["transaksi"] = (
                        "beli" if r["session"] == pembeli else "jual"
                    )
            update_status_properti(id_properti, "sold")
            simpan_notifikasi(
                pembeli, "user",
                f"Properti '{properti}' berhasil dibeli 🎉"
            )
            simpan_notifikasi(
                penjual_login, "seller",
                f"Properti '{properti}' berhasil terjual 💰"
            )
            simpan_ke_riwayat(trx)

        elif pilih == "2":
            for r in semua:
                if r["id_transaksi"] == id_trx:
                    r["status"] = "Dibatalkan"
                    if r["session"] == pembeli:
                        r["transaksi"] = "batal"

            update_status_properti(id_properti, "available")

            simpan_notifikasi(
                pembeli, "user",
                f"Booking properti '{properti}' dibatalkan seller"
            )

        elif pilih == "3":
            if get_extend_count(id_trx) >= 3:
                print("❌ Maksimal perpanjangan 3x.")
                input("ENTER...")
                return

            tanggal = input("Tanggal baru (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(tanggal, "%Y-%m-%d")
            except ValueError:
                print("❌ Format salah.")
                input("ENTER...")
                return

            tambah_jadwal_booking(id_trx, tanggal, pembeli, penjual_login)

            for r in semua:
                if r["id_transaksi"] == id_trx:
                    r["status"] = "Perpanjang Waktu"

            simpan_notifikasi(
                pembeli, "user",
                f"Booking properti '{properti}' diperpanjang hingga {tanggal}"
            )
        else:
            print("❌ Pilihan tidak valid.")
            input("ENTER...")
            return

    simpan_perubahan_csv(semua)
    print("✅ Status berhasil diperbarui.")
    input("ENTER...")


# ================= RIWAYAT =================

def simpan_ke_riwayat(row):
    if os.path.exists(FILE_RIWAYAT):
        with open(FILE_RIWAYAT, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["id_transaksi"] == row["id_transaksi"]:
                    return

    with open(FILE_PROPERTI, newline="", encoding="utf-8") as f:
        properti = next(p for p in csv.DictReader(f) if p["id"] == row["id_properti"])

    data = {
        "id_transaksi": row["id_transaksi"],
        "username": row["username_pembeli"],
        "id": properti["id"],
        "nama": properti["nama"],
        "kategori": properti["kategori"],
        "lokasi": properti["lokasi"],
        "harga": properti["harga"],
        "penjual": properti["penjual"],
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transaksi": "beli"
    }

    with open(FILE_RIWAYAT, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(data)


# ================= MENU =================

def menu_kelola_pesanan(user_active):
    auto_expire_booking()
    while True:
        transaksi = tampilkan_pesanan(user_active)

        print("\n[ OPSI ]")
        print("1. 🔄 Update Status Booking")
        print("2. 💬 Chat Buyer")
        print("0. 🔙 Kembali")

        pilih = input(">> ").strip()

        if pilih == "1":
            update_status_pesanan(user_active)

        elif pilih == "2":
            id_trx = input("ID Transaksi: ").strip()
            for t in transaksi:
                if t["id_transaksi"] == id_trx:
                    session = normalize_session(user_active, t["username_pembeli"])
                    buka_chat(user_active, session, t["username_pembeli"])
                    break

        elif pilih == "0":
            return


# ========== MEMBATALKAN BOOKING LAIN ==========
def batalkan_booking_lain(id_properti, id_transaksi_aktif):
    semua = baca_data_csv()
    berubah = False

    for r in semua:
        if (
            r["id_properti"] == id_properti
            and r["id_transaksi"] != id_transaksi_aktif
            and r["status"] == "Menunggu Konfirmasi"
        ):
            r["status"] = "Dibatalkan"
            berubah = True

            simpan_notifikasi(
                r["username_pembeli"], "user",
                f"Booking properti '{r['nama_properti']}' dibatalkan karena sudah dibooking buyer lain",
                redirect="transaksi_buyer"
            )

    if berubah:
        simpan_perubahan_csv(semua)


# ========= AUTO EXPIRED KALAU UDAH LEWAT DEADLINE =========
def auto_expire_booking():
    if not os.path.exists(FILE_TRANSAKSI):
        return

    semua = baca_data_csv()
    sekarang = datetime.now()
    berubah = False

    for r in semua:
        tanggal = datetime.strptime(r["tanggal"], "%Y-%m-%d %H:%M:%S")

        if r["status"] == "Menunggu Konfirmasi":
            if sekarang - tanggal > timedelta(days=2):
                r["status"] = "Dibatalkan"
                update_status_properti(r["id_properti"], "available")
                berubah = True

                simpan_notifikasi(
                    r["username_pembeli"], "user",
                    f"Booking properti '{r['nama_properti']}' otomatis dibatalkan (expired)",
                    redirect="transaksi_buyer"
                )

        elif r["status"] == "Booked":
            if sekarang - tanggal > timedelta(days=7):
                r["status"] = "Dibatalkan"
                update_status_properti(r["id_properti"], "available")
                berubah = True

                simpan_notifikasi(
                    r["username_pembeli"], "user",
                    f"Booking properti '{r['nama_properti']}' dibatalkan karena melewati batas waktu",
                    redirect="transaksi_buyer"
                )

    if berubah:
        simpan_perubahan_csv(semua)