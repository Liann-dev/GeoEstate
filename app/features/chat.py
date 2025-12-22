import csv
import os
import random
from datetime import datetime

# =========================
# Path file CSV
# =========================
FILE_USERS = "data/users.csv"
FILE_CHAT = "data/chat.csv"

# =========================
# Fungsi daftar user
# =========================
def daftar_user(username):
    """Mengembalikan daftar user selain username sendiri dan admin."""
    users = []
    try:
        with open(FILE_USERS, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] != username and row['role'].lower() != 'admin':
                    users.append({'username': row['username'], 'email': row['email']})
    except FileNotFoundError:
        print(f"File {FILE_USERS} tidak ditemukan!")
    return users

# =========================
# Fungsi generate ID unik
# =========================
def generate_chat_id():
    """Menghasilkan ID unik untuk chat dengan format CHT-XXXX."""
    existing_ids = set()
    try:
        with open(FILE_CHAT, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_ids.add(row['id'])
    except FileNotFoundError:
        pass

    while True:
        rand_id = f"CHT-{random.randint(1000, 9999)}"
        if rand_id not in existing_ids:
            return rand_id

# =========================
# Fungsi simpan chat dengan session
# =========================
def simpan_chat(sender, receiver, pesan):
    """Simpan pesan chat ke FILE_CHAT dengan ID unik, timestamp, dan session per user."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_id = generate_chat_id()
    fieldnames = ['id','sender','receiver','message','timestamp','session']

    try:
        with open(FILE_CHAT, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            # Baris untuk sender
            writer.writerow({
                'id': chat_id,
                'sender': sender,
                'receiver': receiver,
                'message': pesan,
                'timestamp': timestamp,
                'session': sender
            })
            # Baris untuk receiver
            writer.writerow({
                'id': chat_id,
                'sender': sender,
                'receiver': receiver,
                'message': pesan,
                'timestamp': timestamp,
                'session': receiver
            })
    except Exception as e:
        print("Gagal menyimpan chat:", e)
        input("Tekan ENTER untuk kembali...")

# =========================
# Fungsi lihat chat dengan kontak
# =========================
def lihat_chat_user(username, kontak, width=50, msg_width=30):
    """Menampilkan chat antara username dan kontak, chat kiri/kanan sesuai pengirim, judul di tengah."""
    try:
        with open(FILE_CHAT, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            chat_list = []
            for row in reader:
                session = row.get('session', username)
                if session == username and (row['sender'] == username or row['sender'] == kontak) and (row['receiver'] == username or row['receiver'] == kontak):
                    chat_list.append(row)

            if not chat_list:
                print("Belum ada chat dengan kontak ini.")
                return []

            # Judul chat rata tengah
            judul = f"=== Chat dengan {kontak} ==="
            print(f"{judul:^{width}}")  # rata tengah
            print("="*width)

            for chat in chat_list:
                msg = chat['message']
                ts = chat['timestamp']

                # Pecah pesan menjadi beberapa baris jika terlalu panjang
                lines = [msg[i:i+msg_width] for i in range(0, len(msg), msg_width)]

                if chat['sender'] == username:
                    # Chat kita -> kanan
                    for line in lines:
                        print(f"{line:>{width}}")
                    print(f"{ts:>{width}}")
                    print("-"*width)
                else:
                    # Chat kontak -> kiri
                    for line in lines:
                        print(f"{line:<{width}}")
                    print(f"{ts:<{width}}")
                    print("-"*width)

            # Nama pengirim di kiri/kanan ujung garis chat
            print("="*width)
            left_name = kontak
            right_name = username
            space_between = width - len(left_name) - len(right_name)
            print(f"{left_name}{' '*space_between}{right_name}")

            return chat_list

    except FileNotFoundError:
        print("Belum ada chat sama sekali.")
        input("Tekan ENTER untuk kembali...")
        return []



# =========================
# Fungsi hapus chat
# =========================
def hapus_chat_by_id_user(username):
    """Hapus chat tertentu berdasarkan ID untuk session user saat ini."""
    try:
        # Ambil semua chat milik user
        chat_list = []
        with open(FILE_CHAT, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['session'] == username:
                    chat_list.append(row)

        if not chat_list:
            print("Belum ada chat yang bisa dihapus.")
            input("Tekan ENTER untuk kembali...")
            return

        # Tampilkan tabel chat
        print("\nDaftar Chat Anda:")
        print(f"{'ID Chat':<10}{'Pesan':<40}{'Tanggal':<20}")
        print("-"*70)
        for chat in chat_list:
            msg_display = (chat['message'][:37] + '...') if len(chat['message']) > 40 else chat['message']
            print(f"{chat['id']:<10}{msg_display:<40}{chat['timestamp']:<20}")
        print("-"*70)

        # Input ID Chat
        chat_id = input("Masukkan ID Chat yang ingin dihapus [ENTER untuk batal]: ").strip()
        if not chat_id:
            return

        # Validasi ID
        if chat_id not in [c['id'] for c in chat_list]:
            print("ID Chat tidak valid.")
            input("Tekan ENTER untuk kembali...")
            return

        # Hapus chat hanya untuk session = username
        rows = []
        with open(FILE_CHAT, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not (row['id'] == chat_id and row['session'] == username):
                    rows.append(row)

        with open(FILE_CHAT, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['id','sender','receiver','message','timestamp','session']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"\nChat dengan ID {chat_id} berhasil dihapus.")
        input("Tekan ENTER untuk kembali...")

    except FileNotFoundError:
        print("Belum ada chat sama sekali.")
        input("Tekan ENTER untuk kembali...")

def hapus_semua_chat_session(username, kontak):
    """Hapus semua chat antara username dan kontak untuk session user saat ini dengan konfirmasi."""
    try:
        # Konfirmasi
        while True:
            konfirmasi = input(f"Apakah Anda yakin ingin menghapus semua chat dengan {kontak}? (y/n): ").strip().lower()
            if konfirmasi == 'y':
                break
            elif konfirmasi == 'n':
                print("\nBatal menghapus semua chat.")
                input("Tekan ENTER untuk kembali...")
                return
            else:
                print("Input tidak valid. Silakan masukkan 'y' atau 'n'.\n")

        # Proses hapus chat
        rows = []
        with open(FILE_CHAT, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not (row['session'] == username and ((row['sender'] == username and row['receiver'] == kontak) or (row['sender'] == kontak and row['receiver'] == username))):
                    rows.append(row)
        with open(FILE_CHAT, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['id','sender','receiver','message','timestamp','session']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"\nSemua chat dengan {kontak} berhasil dihapus.")
        input("Tekan ENTER untuk kembali...")

    except FileNotFoundError:
        print("Belum ada chat sama sekali.")
        input("Tekan ENTER untuk kembali...")

# =========================
# Menu utama
# =========================
def menu_chat(username):
    while True:
        print("\n=== Menu Chat ===")
        print("1. Lihat Kontak")
        print("2. Kirim Pesan")
        print("3. Hapus Pesan")
        print("4. Kembali")
        pilihan = input("\nPilih opsi (1-4): ").strip()

        users = daftar_user(username)
        if not users and pilihan in ['1','2','3']:
            print("Tidak ada kontak tersedia.")
            input("Tekan ENTER untuk kembali...")
            continue

        # =========================
        # Lihat Kontak / Chat
        # =========================
        if pilihan == '1':
            # Tampilkan tabel kontak
            print("\nDaftar Kontak:")
            print(f"{'No':<4}{'Username':<15}{'Email':<30}")
            print("-"*50)
            for i, user in enumerate(users, 1):
                print(f"{i:<4}{user['username']:<15}{user['email']:<30}")
            print("-"*50)

            kontak_idx = input("Pilih nomor kontak untuk melihat chat [ENTER untuk batal]: ").strip()
            if not kontak_idx:
                continue
            if not kontak_idx.isdigit():
                print("Nomor kontak tidak valid.")
                input("Tekan ENTER untuk kembali...")
                continue
            idx = int(kontak_idx)
            if not (1 <= idx <= len(users)):
                print("Nomor kontak tidak ada.")
                input("Tekan ENTER untuk kembali...")
                continue

            kontak = users[idx-1]['username']
            chat_list = lihat_chat_user(username, kontak)
            if not chat_list:
                input("Tekan ENTER untuk kembali...")
                continue

            input("\nTekan ENTER untuk kembali...")


        # =========================
        # Kirim Pesan
        # =========================
        elif pilihan == '2':
            # Tampilkan tabel kontak
            print("\nDaftar Kontak:")
            print(f"{'No':<4}{'Username':<15}{'Email':<30}")
            print("-"*50)
            for i, user in enumerate(users, 1):
                print(f"{i:<4}{user['username']:<15}{user['email']:<30}")
            print("-"*50)

            kontak_idx = input("Pilih nomor kontak untuk mengirim pesan [ENTER untuk batal]: ").strip()
            if not kontak_idx:
                continue
            if not kontak_idx.isdigit():
                print("Nomor kontak tidak valid.")
                input("Tekan ENTER untuk kembali...")
                continue
            idx = int(kontak_idx)
            if not (1 <= idx <= len(users)):
                print("Nomor kontak tidak ada.")
                input("Tekan ENTER untuk kembali...")
                continue

            pesan = input("Masukkan pesan [ENTER untuk batal]: ").strip()
            if not pesan:
                continue

            simpan_chat(username, users[idx-1]['username'], pesan)
            print("Pesan terkirim!")
            input("Tekan ENTER untuk kembali...")

        # =========================
        # Hapus Pesan
        # =========================
        elif pilihan == '3':
            # Tampilkan tabel kontak
            print("\nDaftar Kontak:")
            print(f"{'No':<4}{'Username':<15}{'Email':<30}")
            print("-"*50)
            for i, user in enumerate(users, 1):
                print(f"{i:<4}{user['username']:<15}{user['email']:<30}")
            print("-"*50)

            kontak_idx = input("Pilih nomor kontak untuk hapus chat [ENTER untuk batal]: ").strip()
            if not kontak_idx:
                continue
            if not kontak_idx.isdigit():
                print("Nomor kontak tidak valid.")
                input("Tekan ENTER untuk kembali...")
                continue
            idx = int(kontak_idx)
            if not (1 <= idx <= len(users)):
                print("Nomor kontak tidak ada.")
                input("Tekan ENTER untuk kembali...")
                continue

            kontak = users[idx-1]['username']

            # Tampilkan chat dengan kontak
            chat_list = lihat_chat_user(username, kontak)
            if not chat_list:
                input("Tekan ENTER untuk kembali...")
                continue

            # Opsi hapus
            print("\n1. Hapus satu chat")
            print(f"2. Hapus semua chat dengan {kontak}")
            print("3. Kembali")
            opsi = input("\nPilih opsi (1-3): ").strip()

            if opsi == '1':
                hapus_chat_by_id_user(username)
            elif opsi == '2':
                hapus_semua_chat_session(username, kontak)
            elif opsi == '3':
                continue
            else:
                print("Opsi tidak valid.")

        # =========================
        # Kembali
        # =========================
        elif pilihan == '4':
            break
        else:
            print("Pilihan tidak valid.")