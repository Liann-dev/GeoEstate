import csv
import os
from datetime import datetime, timedelta
from app.features.notifikasi_helper import simpan_notifikasi
from app.features.chat import buka_chat, normalize_session


FILE_TRANSAKSI = "data/transaksi.csv"
FILE_PROPERTI = "data/properti.csv"
FILE_RIWAYAT = "data/properti_dibeli.csv"
FILE_SCHEDULE = "data/booking_schedule.csv"


# ================= UTIL =================

def baca_data_csv():
    if not os.path.exists(FILE_TRANSAKSI):
        return []
    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        return list(csv.DictReader(file))


def simpan_perubahan_csv(data_baru):
    fieldnames = [
        'id_transaksi', 'username_pembeli', 'penjual',
        'id_properti', 'nama_properti', 'harga',
        'tanggal', 'transaksi', 'status', 'session'
    ]

    os.makedirs(os.path.dirname(FILE_TRANSAKSI), exist_ok=True)

    with open(FILE_TRANSAKSI, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_baru)


def print_separator(lebar):
    print("-" * lebar)

# ================= SCHEDULE =================
def get_base_date(id_transaksi):
    """
    Jika belum ada jadwal → pakai hari ini
    Jika sudah → pakai jadwal terakhir
    """
    terakhir = get_jadwal_terakhir(id_transaksi)

    if not terakhir:
        return datetime.now().date()

    return datetime.strptime(terakhir, "%Y-%m-%d").date()

def get_jadwal_terakhir(id_transaksi):
    if not os.path.exists(FILE_SCHEDULE):
        return None

    terakhir = None

    with open(FILE_SCHEDULE, mode='r', newline='') as file:
        for row in csv.DictReader(file):
            if row['id_transaksi'] == id_transaksi:
                terakhir = row['schedule']

    return terakhir

def tambah_jadwal_booking(id_transaksi, jadwal_baru, penjual, pembeli):
    with open(FILE_SCHEDULE, mode='a', newline='') as file:
        writer = csv.writer(file)

        # session pembeli
        writer.writerow([id_transaksi, jadwal_baru, pembeli])

        # session penjual
        writer.writerow([id_transaksi, jadwal_baru, penjual])

def get_extend_count(id_transaksi):
    if not os.path.exists(FILE_SCHEDULE):
        return 0

    jadwal_set = set()

    with open(FILE_SCHEDULE, mode='r', newline='') as file:
        for row in csv.DictReader(file):
            if row['id_transaksi'] == id_transaksi:
                jadwal_set.add(row['schedule'])

    # ✅ jadwal pertama langsung dihitung sebagai extend ke-1
    return len(jadwal_set)

def bisa_extend(id_transaksi, max_extend=3):
    return get_extend_count(id_transaksi) < max_extend

def input_tanggal_valid(jadwal_lama=None):
    while True:
        tanggal_input = input(">> Masukkan Tanggal (0 untuk kembali): ").strip()

        if tanggal_input == '0':
            return None

        parts = tanggal_input.split('-')
        if len(parts) != 3:
            print("❌ Format salah! Gunakan YYYY-MM-DD.")
            continue

        y, m, d = parts
        if not (y.isdigit() and m.isdigit() and d.isdigit()):
            print("❌ Tanggal harus berupa angka.")
            continue

        try:
            tanggal = datetime(int(y), int(m), int(d)).date()
        except ValueError:
            print("❌ Tanggal tidak valid.")
            continue

        hari_ini = datetime.now().date()
        if tanggal < hari_ini:
            print("❌ Tidak boleh di masa lalu.")
            continue

        if jadwal_lama:
            lama = datetime.strptime(jadwal_lama, "%Y-%m-%d").date()

            if tanggal <= lama:
                print("❌ Harus lebih maju dari jadwal sebelumnya.")
                continue

            batas_maks = lama + timedelta(days=7)
            if tanggal > batas_maks:
                print("❌ Perpanjangan maksimal 7 hari dari jadwal sebelumnya.")
                print(f"   📅 Batas akhir: {batas_maks}")
                continue

        return tanggal.strftime("%Y-%m-%d")

def input_tanggal_extend(id_transaksi):
    base_date = get_base_date(id_transaksi)
    max_date = base_date + timedelta(days=7)

    while True:
        tanggal_input = input(
            f">> Masukkan tanggal ({base_date} s/d {max_date}) (0 untuk batal): "
        ).strip()

        if tanggal_input == "0":
            return None

        try:
            tanggal = datetime.strptime(tanggal_input, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Format salah! Gunakan YYYY-MM-DD.")
            continue

        if tanggal < base_date:
            print("❌ Tanggal tidak boleh sebelum jadwal acuan.")
            continue

        if tanggal > max_date:
            print("❌ Extend maksimal hanya 7 hari dari jadwal sebelumnya.")
            continue

        return tanggal_input

# ================= CEK TRANSAKSI AKTIF =================

def sedang_dalam_transaksi(username, id_properti):
    if not os.path.exists(FILE_TRANSAKSI):
        return False

    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get('session') != username:
                continue

            if (
                row.get('username_pembeli') == username
                and row.get('id_properti') == id_properti
            ):
                if row.get('status') not in ("Lunas / Selesai", "Dibatalkan"):
                    return True
    return False


# ================= TAMPILKAN PESANAN =================

def tampilkan_pesanan(penjual_login):
    semua_transaksi = baca_data_csv()

    transaksi_penjual = [
        t for t in semua_transaksi
        if t['session'] == penjual_login
    ]

    print("\n" * 50)
    print("=" * 110)
    print("                                        📦 KELOLA BOOKING SELLER")
    print("=" * 110)

    if not transaksi_penjual:
        print("📭 Belum ada booking masuk.")
        print("=" * 110)
        return []

    print(
        f" {'ID':<10} | {'BUYER':<12} | {'PROPERTI':<20} | "
        f"{'TANGGAL':<18} | {'HARGA':<18} | STATUS"
    )
    print("=" * 110)

    for t in transaksi_penjual:
        # ✅ ambil jadwal terbaru (extend terakhir)
        jadwal_terakhir = get_jadwal_terakhir(t['id_transaksi'])
        tanggal_tampil = jadwal_terakhir if jadwal_terakhir else t['tanggal'][:10]

        extend = get_extend_count(t['id_transaksi'])
        tanggal_text = f"{tanggal_tampil} ({extend}/3)"

        harga = f"Rp {int(t['harga']):,}".replace(",", ".")
        status_icon = {
            "Menunggu Konfirmasi": "⏳ Menunggu",
            "Perpanjang Waktu": "⏰ Diperpanjang",
            "Lunas / Selesai": "✅ Selesai",
            "Dibatalkan": "❌ Dibatalkan"
        }.get(t['status'], t['status'])

        print(
            f" {t['id_transaksi']:<10} | {t['username_pembeli']:<12} | "
            f"{t['nama_properti'][:18]:<20} | {tanggal_text:<18} | "
            f"{harga:<18} | {status_icon}"
        )

    print("=" * 110)
    print(f" Total Booking: {len(transaksi_penjual)}")

    return transaksi_penjual

# ================= UPDATE STATUS  =================

def update_status_pesanan(penjual_login):

    id_input = input("\nID Transaksi (ENTER untuk batal): ").strip()
    if not id_input:
        return

    semua_data = baca_data_csv()

    # 🔎 Cari transaksi milik seller
    trx_penjual = None
    for row in semua_data:
        if row['id_transaksi'] == id_input and row['session'] == penjual_login:
            trx_penjual = row
            break

    if not trx_penjual:
        print("❌ Transaksi tidak ditemukan / bukan milik Anda.")
        input("ENTER...")
        return

    # 🔒 Status final tidak bisa diubah
    if trx_penjual['status'] in ("Lunas / Selesai", "Dibatalkan"):
        print("⚠️ Status sudah final, tidak bisa diubah.")
        input("ENTER...")
        return

    # ================= MENU =================
    print("\n[ UPDATE STATUS ]")
    print("1. Konfirmasi (Lunas / Selesai)")
    print("2. Batalkan")
    print("3. Perpanjang Waktu")

    pilihan = input(">> Pilihan: ").strip()
    status_baru = trx_penjual['status']

    # ================= OPSI 1 =================
    if pilihan == "1":
        status_baru = "Lunas / Selesai"

    # ================= OPSI 2 =================
    elif pilihan == "2":
        status_baru = "Dibatalkan"

    # ================= OPSI 3 =================
    elif pilihan == "3":

        extend_count = get_extend_count(id_input)
        if extend_count >= 3:
            print("❌ Perpanjangan sudah maksimal (3x).")
            input("ENTER...")
            return

        jadwal_lama = get_jadwal_terakhir(id_input)
        base_date = (
            datetime.strptime(jadwal_lama, "%Y-%m-%d").date()
            if jadwal_lama else datetime.now().date()
        )

        print("\n📅 PERPANJANG WAKTU")
        print(f"• Tanggal acuan : {base_date}")
        print("• Maksimal      : +7 hari")
        print("• Format        : YYYY-MM-DD")

        while True:
            tanggal_input = input(">> Tanggal baru (ENTER batal): ").strip()
            if not tanggal_input:
                return

            # Validasi format
            try:
                tanggal_baru = datetime.strptime(
                    tanggal_input, "%Y-%m-%d"
                ).date()
            except ValueError:
                print("❌ Format tanggal salah.")
                continue

            # Validasi range
            if tanggal_baru <= base_date:
                print("❌ Tanggal harus setelah jadwal sebelumnya.")
                continue

            if tanggal_baru > base_date + timedelta(days=7):
                print("❌ Maksimal perpanjangan hanya 7 hari.")
                continue

            # Simpan jadwal
            tambah_jadwal_booking(
                id_transaksi=id_input,
                jadwal_baru=tanggal_baru.strftime("%Y-%m-%d"),
                penjual=penjual_login,
                pembeli=trx_penjual['username_pembeli']
            )

            status_baru = "Perpanjang Waktu"
            break

    else:
        print("❌ Pilihan tidak valid.")
        input("ENTER...")
        return

    # ================= SYNC STATUS =================
    for row in semua_data:
        if row['id_transaksi'] == id_input:
            row['status'] = status_baru

            if status_baru == "Lunas / Selesai":
                row['transaksi'] = (
                    "beli" if row['session'] == row['username_pembeli'] else "jual"
                )

            elif status_baru == "Dibatalkan":
                if row['session'] == row['username_pembeli']:
                    row['transaksi'] = "batal"

    # ================= TRIGGER NOTIFIKASI =================
    pembeli = trx_penjual["username_pembeli"]
    properti = trx_penjual["nama_properti"]

    if status_baru == "Lunas / Selesai":
        simpan_notifikasi(
            username=pembeli,
            role="user",
            pesan=f"Properti '{properti}' berhasil dibeli"
        )
        simpan_notifikasi(
        username=penjual_login,
        role="seller",
        pesan=f"💰 Properti '{properti}' berhasil terjual"
    )
        simpan_ke_riwayat(trx_penjual)

    elif status_baru == "Dibatalkan":
        simpan_notifikasi(
            username=pembeli,
            role="user",
            pesan=f"Booking properti '{properti}' dibatalkan oleh seller"
        )

    elif status_baru == "Perpanjang Waktu":
        simpan_notifikasi(
            username=pembeli,
            role="user",
            pesan=f"Booking properti '{properti}' diperpanjang oleh seller"
        )


    # ================= SYNC KE SEMUA SESSION =================
    for row in semua_data:
        if row['id_transaksi'] == id_input:
            row['status'] = status_baru
            
        if pilihan == "1":
            if row['id_transaksi'] == id_input:
                if row['session'] == row['username_pembeli']:
                    row['transaksi'] = "beli"
                if row['session'] == row['penjual']:
                    row['transaksi'] = "jual"
        if pilihan == "2":
            if row['id_transaksi'] == id_input:
                if row['session'] == row['username_pembeli']:
                    row['transaksi'] = "batal"

    simpan_perubahan_csv(semua_data)

    # ================= SIMPAN RIWAYAT =================
    if status_baru == "Lunas / Selesai":
        simpan_ke_riwayat(trx_penjual)
    
    print(">> Status berhasil diperbarui.")
    input("Tekan ENTER untuk lanjut...")


# ================= SIMPAN RIWAYAT =================

def simpan_ke_riwayat(row):
    # Cegah duplikasi berdasarkan id_transaksi
    if os.path.exists(FILE_RIWAYAT):
        with open(FILE_RIWAYAT, mode='r', newline='') as f:
            for r in csv.DictReader(f):
                if r['id_transaksi'] == row['id_transaksi']:
                    return  # sudah tersimpan, hentikan

    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE_PROPERTI, mode='r', newline='') as f:
        for p in csv.DictReader(f):
            if p['id'] == row['id_properti']:
                properti = p
                break
        else:
            print(">> Properti tidak ditemukan.")
            return

    data = {
        "id_transaksi": row['id_transaksi'],
        "username": row['username_pembeli'],
        "id": properti['id'],
        "nama": properti['nama'],
        "kategori": properti['kategori'],
        "lokasi": properti['lokasi'],
        "harga": properti['harga'],
        "penjual": properti['penjual'],
        "tanggal": tanggal,
        "transaksi": "beli"
    }

    file_ada = os.path.exists(FILE_RIWAYAT)

    with open(FILE_RIWAYAT, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_ada:
            writer.writeheader()
        writer.writerow(data)

def menu_kelola_pesanan(user_active):

    while True:
        transaksi = tampilkan_pesanan(user_active)

        print("\n[ OPSI ]")
        print("1. 🔄 Update Status Booking")
        print("2. 💬 Chat dengan Buyer")
        print("0. 🔙 Kembali")

        pil = input(">> Pilih menu: ").strip()

        if pil == "1":
            update_status_pesanan(user_active)
            
        elif pil == "2":
            if not transaksi:
                input("Belum ada booking. ENTER...")
                continue

            id_trx = input("Masukkan ID Transaksi (ENTER batal): ").strip()
            if not id_trx:
                continue

            for t in transaksi:
                if t['id_transaksi'] == id_trx:
                    session_id = normalize_session(user_active, t['username_pembeli'])
                    buka_chat(user_active, session_id, t['username_pembeli'])
                    break
            else:
                print("❌ ID Transaksi tidak ditemukan.")
                input("ENTER...")

        elif pil == "0":
            return

        else:
            print("❌ Pilihan tidak valid.")
