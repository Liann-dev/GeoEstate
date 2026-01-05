import csv
import os
from datetime import datetime, timedelta
from app.features.chat import buka_chat, normalize_session

FILE_JADWAL = 'data/jadwal_survey.csv'
MAX_EXTEND = 3
WAKTU_OPSI = ["09:00", "13:00", "16:00"]

# =====================================================
# UTIL DASAR
# =====================================================
def muat_semua_survei():
    if not os.path.exists(FILE_JADWAL):
        return []

    with open(FILE_JADWAL, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def append_survei(row):
    file_ada = os.path.exists(FILE_JADWAL)

    with open(FILE_JADWAL, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_ada:
            writer.writeheader()
        writer.writerow(row)


# =====================================================
# HISTORI & FILTER
# =====================================================
def ambil_survei_terbaru(data):
    PRIORITAS = {
        'Pending': 0,
        'Ditolak': 1,
        'Berlangsung': 2,
        'Selesai': 3
    }

    hasil = {}

    for s in data:
        id_s = s['id']
        dt = datetime.strptime(
            f"{s['tanggal']} {s['waktu']}",
            "%Y-%m-%d %H:%M"
        )

        if id_s not in hasil:
            hasil[id_s] = s | {'_dt': dt}
            continue

        lama = hasil[id_s]

        # 1️⃣ datetime lebih baru → menang
        if dt > lama['_dt']:
            hasil[id_s] = s | {'_dt': dt}
            continue

        # 2️⃣ datetime sama → bandingkan STATUS
        if dt == lama['_dt']:
            if PRIORITAS[s['status']] > PRIORITAS[lama['status']]:
                hasil[id_s] = s | {'_dt': dt}

    # buang helper
    for v in hasil.values():
        del v['_dt']

    return list(hasil.values())

def get_extend_count_survei(id_survei):
    if not os.path.exists(FILE_JADWAL):
        return 0

    histori = []
    with open(FILE_JADWAL, newline='', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if row['id'] == id_survei:
                histori.append(row)

    if len(histori) <= 1:
        return 0

    # hitung perubahan tanggal+waktu unik
    jadwal_unik = []
    for h in histori:
        key = (h['tanggal'], h['waktu'])
        if key not in jadwal_unik:
            jadwal_unik.append(key)

    # base jadwal tidak dihitung
    return max(0, len(jadwal_unik) - 1)

def get_jadwal_terakhir(id_survei, data):
    terakhir = None
    dt_terakhir = None

    for s in data:
        if s['id'] != id_survei:
            continue
        dt = datetime.strptime(
            f"{s['tanggal']} {s['waktu']}",
            "%Y-%m-%d %H:%M"
        )
        if not dt_terakhir or dt > dt_terakhir:
            terakhir = s
            dt_terakhir = dt

    return terakhir


# =====================================================
# INPUT
# =====================================================
def input_tanggal_valid(tanggal_lama):
    base = datetime.strptime(tanggal_lama, "%Y-%m-%d").date()
    batas = base + timedelta(days=7)

    while True:
        t = input(f">> Masukkan tanggal ({base} s/d {batas}) (0 batal): ").strip()
        if t == '0':
            return None
        try:
            d = datetime.strptime(t, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Format salah.")
            continue

        if not (base <= d <= batas):
            print("❌ Di luar batas 7 hari.")
            continue

        return t


def pilih_waktu(tanggal_baru, jadwal_lama):
    dt_lama = datetime.strptime(
        f"{jadwal_lama['tanggal']} {jadwal_lama['waktu']}",
        "%Y-%m-%d %H:%M"
    )
    batas = dt_lama + timedelta(days=7)

    while True:
        print("\n[ Pilih Waktu ]")
        for i, w in enumerate(WAKTU_OPSI, 1):
            print(f"{i}. 🕘 {w}")

        p = input(">> Pilih (1/2/3, 0 batal): ").strip()
        if p == '0':
            return None
        if p not in ('1', '2', '3'):
            continue

        w = WAKTU_OPSI[int(p)-1]
        dt_baru = datetime.strptime(
            f"{tanggal_baru} {w}",
            "%Y-%m-%d %H:%M"
        )

        if dt_baru <= dt_lama:
            print("❌ Harus lebih maju.")
            continue
        if dt_baru > batas:
            print("❌ Melebihi 7 hari.")
            continue

        return w


# =====================================================
# TAMPILAN
# =====================================================
def tampilkan_tabel_survei(survei_seller):
    print("\n" * 50)
    print("=" * 90)
    print("                          📋 KELOLA SURVEI SELLER")
    print("=" * 90)
    print(f" {'ID':<10} | {'PROPERTI':<20} | {'TANGGAL':<16} | {'JAM':<6} | {'BUYER':<10} | STATUS")
    print("-" *90)

    for s in survei_seller:
        status_icon = {
            'Pending': '⏳ Pending',
            'Berlangsung': '🔄 Berlangsung',
            'Selesai': '✅ Selesai',
            'Ditolak': '❌ Ditolak'
        }.get(s['status'], s['status'])

        extend = get_extend_count_survei(s['id'])
        tanggal = f"{s['tanggal']} ({extend}/3)"

        print(
            f" {s['id']:<10} | "
            f"{s['nama_properti'][:18]:<20} | "
            f"{tanggal:<16} | "
            f"{s['waktu']:<6} | "
            f"{s['pembeli']:<10} | "
            f"{status_icon}"
        )

    print("=" * 90)
    print(f" Total Survei: {len(survei_seller)}")

# =====================================================
# UPDATE STATUS SURVEI
# =====================================================
def update_status_survei(username):
    semua = muat_semua_survei()
    survei_terbaru = ambil_survei_terbaru(semua)

    survei_seller = [
        s for s in survei_terbaru
        if s['penjual'] == username
    ]

    if not survei_seller:
        print("Belum ada survei.")
        input("ENTER...")
        return

    tampilkan_tabel_survei(survei_seller)

    id_pilih = input("\nMasukkan ID Survei (ENTER batal): ").strip()
    if not id_pilih:
        return

    survei = next((s for s in survei_seller if s['id'] == id_pilih), None)
    if not survei:
        print("❌ ID survei tidak ditemukan.")
        input("ENTER...")
        return

    status = survei['status']

    # ===============================
    # STATUS PENDING
    # ===============================
    if status == 'Pending':
        print("\n[ Update Status ]")
        print("1. Terima")
        print("2. Tolak")
        print("3. Ganti Jadwal")

        opsi = input(">> Pilih: ").strip()

        # ===== TERIMA =====
        if opsi == '1':
            baru = survei.copy()
            baru['status'] = 'Berlangsung'
            append_survei(baru)

        # ===== TOLAK =====
        elif opsi == '2':
            baru = survei.copy()
            baru['status'] = 'Ditolak'
            append_survei(baru)

        # ===== GANTI JADWAL =====
        elif opsi == '3':
            extend = get_extend_count_survei(id_pilih)
            if extend >= MAX_EXTEND:
                print("❌ Ganti jadwal sudah maksimal (3x).")
                input("ENTER...")
                return

            print("\n📅 GANTI JADWAL SURVEI")
            print(f"• Jadwal Lama : {survei['tanggal']} {survei['waktu']}")
            print("• Maksimal    : +7 hari")
            print("• Format      : YYYY-MM-DD")

            tanggal_baru = input_tanggal_valid(survei['tanggal'])
            if not tanggal_baru:
                return

            waktu_baru = pilih_waktu(tanggal_baru, survei)
            if not waktu_baru:
                return

            baru = survei.copy()
            baru['tanggal'] = tanggal_baru
            baru['waktu'] = waktu_baru

            append_survei(baru)

        else:
            print("❌ Pilihan tidak valid.")
            input("ENTER...")
            return

    # ===============================
    # STATUS BERLANGSUNG
    # ===============================
    elif status == 'Berlangsung':
        print("\n1. Tandai Sebagai Selesai")
        if input(">> Pilih: ").strip() != '1':
            return

        baru = survei.copy()
        baru['status'] = 'Selesai'
        append_survei(baru)

    else:
        print("❌ Status sudah final.")
        input("ENTER...")
        return

    print("✅ Perubahan berhasil disimpan.")
    input("ENTER...")

# =====================================================
# MENU UTAMA
# =====================================================
def menu_kelola_survei(username):
    while True:
        semua = muat_semua_survei()
        survei = [
            s for s in ambil_survei_terbaru(semua)
            if s['penjual'] == username
        ]

        if not survei:
            print("Belum ada survei.")
            input("ENTER...")
            return

        tampilkan_tabel_survei(survei)

        print("\n[ OPSI ]")
        print("1. 🔄 Update Status Survei")
        print("2. 💬 Chat dengan Buyer")
        print("0. 🔙 Kembali")

        p = input(">> ").strip()

        if p == '1':
            update_status_survei(username)
        elif p == '2':
            id_s = input("ID Survei: ")
            for s in survei:
                if s['id'] == id_s:
                    buka_chat(username,
                              normalize_session(username, s['pembeli']),
                              s['pembeli'])
                    break
        elif p == '0':
            return
