import csv
import os
from datetime import datetime, timedelta

from app.features.notifikasi_helper import simpan_notifikasi
from app.features.chat import buka_chat, normalize_session
from app.features.booking_history import simpan_booking_history

FILE_TRANSAKSI = "data/transaksi.csv"
FILE_PROPERTI = "data/properti.csv"
FILE_BOOKING = "data/booking.csv"

# =====================================================
# UTIL CSV
# =====================================================

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


# =====================================================
# 🔥 FIX UTAMA: SYNC STATUS BUYER & SELLER
# =====================================================

def update_status_transaksi_semua(semua, id_transaksi, status_baru):
    for r in semua:
        if r["id_transaksi"] == id_transaksi:
            r["status"] = status_baru


# =====================================================
# BOOKING DATE & EXTEND
# =====================================================

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


def validasi_tanggal_perpanjang(tanggal_lama, tanggal_input):
    try:
        lama = datetime.strptime(tanggal_lama, "%Y-%m-%d")
        baru = datetime.strptime(tanggal_input, "%Y-%m-%d")
    except ValueError:
        return False, "❌ Format tanggal harus YYYY-MM-DD"

    if baru <= lama:
        return False, "❌ Tanggal harus setelah sebelumnya"

    if (baru - lama).days > 7:
        return False, "❌ Maksimal perpanjangan 7 hari"

    return True, ""


# =====================================================
# AUTO EXPIRE
# =====================================================

def auto_expire_booking():
    semua = baca_data_csv()
    sekarang = datetime.now()
    berubah = False

    for r in semua:
        if r["status"] not in ("Menunggu Konfirmasi", "Booked"):
            continue

        tgl = datetime.strptime(r["tanggal"], "%Y-%m-%d %H:%M:%S")
        batas = 2 if r["status"] == "Menunggu Konfirmasi" else 7

        if sekarang - tgl > timedelta(days=batas):
            update_status_transaksi_semua(semua, r["id_transaksi"], "Dibatalkan")
            update_status_properti(r["id_properti"], "available")
            berubah = True

            simpan_booking_history(
                r["id_transaksi"],
                "EXPIRED",
                "system",
                r["tanggal"][:10],
                "-"
            )

            simpan_notifikasi(
                r["username_pembeli"],
                "user",
                f"Booking properti '{r['nama_properti']}' dibatalkan otomatis (expired)",
                redirect="transaksi_buyer"
            )

    if berubah:
        simpan_perubahan_csv(semua)


# =====================================================
# UPDATE STATUS PESANAN (SELLER ONLY)
# =====================================================

def update_status_pesanan(penjual_login):
    id_trx = input("\nMasukkan ID Transaksi: ").strip()
    semua = baca_data_csv()

    trx = next(
        (
            r for r in semua
            if r["id_transaksi"] == id_trx
            and r["session"] == penjual_login
            and r["penjual"].strip().lower() == penjual_login.strip().lower()
        ),
        None
    )

    if not trx:
        print("❌ Transaksi tidak ditemukan atau bukan milik Anda.")
        input("ENTER...")
        return

    status = trx["status"]
    pembeli = trx["username_pembeli"]
    properti = trx["nama_properti"]

    if status in ("Sold", "Dibatalkan", "Lunas / Selesai"):
        print("🔒 Status sudah final.")
        input("ENTER...")
        return

    if status == "Menunggu Konfirmasi":
        print("1. ✅ Terima Booking")
        print("2. ❌ Tolak Booking")
        pilih = input(">> ")

        if pilih == "1":
            update_status_transaksi_semua(semua, id_trx, "Booked")
            tanggal_awal = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            simpan_booking_awal(id_trx, tanggal_awal)
            simpan_booking_history(id_trx, "SET_BOOKING", "seller", "-", tanggal_awal)
            update_status_properti(trx["id_properti"], "booked")
            simpan_notifikasi(pembeli, "user", f"Booking '{properti}' disetujui", redirect="transaksi_buyer")

        elif pilih == "2":
            update_status_transaksi_semua(semua, id_trx, "Dibatalkan")
            update_status_properti(trx["id_properti"], "available")

    elif status == "Menunggu Pembayaran":
        print("1. ✅ Konfirmasi Pembelian")
        print("2. ❌ Tolak Pembelian")
        pilih = input(">> ")

        if pilih == "1":
            update_status_transaksi_semua(semua, id_trx, "Sold")
            update_status_properti(trx["id_properti"], "sold")

        elif pilih == "2":
            update_status_transaksi_semua(semua, id_trx, "Dibatalkan")
            update_status_properti(trx["id_properti"], "available")

    elif status == "Booked":
        print("1. ❌ Batalkan Booking")
        print("2. ⏰ Perpanjang Booking")
        pilih = input(">> ")

        if pilih == "1":
            update_status_transaksi_semua(semua, id_trx, "Dibatalkan")
            update_status_properti(trx["id_properti"], "available")

        elif pilih == "2":
            extend = get_extend_count(id_trx)
            if extend >= 3:
                print("❌ Maksimal perpanjangan 3x.")
                input("ENTER...")
                return

            lama = get_jadwal_terakhir(id_trx)
            tanggal_baru = input("Tanggal baru (YYYY-MM-DD): ").strip()
            valid, msg = validasi_tanggal_perpanjang(lama, tanggal_baru)
            if not valid:
                print(msg)
                input("ENTER...")
                return

            simpan_booking_awal(id_trx, tanggal_baru)
            simpan_booking_history(id_trx, "EXTEND", "seller", lama, tanggal_baru)

    simpan_perubahan_csv(semua)
    print("✅ Status berhasil diperbarui.")
    input("ENTER...")


# =====================================================
# MENU SELLER
# =====================================================

def menu_kelola_pesanan(user_active):
    auto_expire_booking()

    while True:
        semua = baca_data_csv()
        data = [
            t for t in semua
            if t["session"] == user_active
            and t["penjual"].strip().lower() == user_active.strip().lower()
        ]

        print("\n" * 50)
        print("📦 KELOLA BOOKING SELLER")
        print("-" * 100)

        if not data:
            print("Belum ada booking.")
        else:
            print(f"{'ID':<12} {'BUYER':<17} {'PROPERTI':<35} {'STATUS'}")
            print("-" * 100)
            for t in data:
                print(f"{t['id_transaksi']:<12} {t['username_pembeli']:<17} {t['nama_properti'][:30]:<35} {t['status']}")

        print("\n1. 🔄 Update Status")
        print("2. 💬 Chat Buyer")
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
        elif pilih == "0":
            return


# =====================================================
# DIPAKAI BUYER
# =====================================================

def sedang_dalam_transaksi(username, id_properti):
    if not os.path.exists(FILE_TRANSAKSI):
        return False

    with open(FILE_TRANSAKSI, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (
                r["username_pembeli"] == username
                and r["id_properti"] == id_properti
                and r["status"] not in ("Dibatalkan", "Sold", "Lunas / Selesai")
            ):
                return True
    return False
