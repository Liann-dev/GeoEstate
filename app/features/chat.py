import csv
import os
from datetime import datetime

FILE_CHAT = "data/chat.csv"

WIDTH = 60
MSG_WIDTH = 40


# =========================
# UTIL
# =========================
def normalize_session(user1, user2):
    u1, u2 = sorted([user1.lower(), user2.lower()])
    return f"CHAT-{u1}-{u2}"


def init_chat_file():
    if not os.path.exists(FILE_CHAT):
        with open(FILE_CHAT, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "sender", "receiver", "message", "timestamp", "session"
            ])


def wrap_text(text, width):
    return [text[i:i + width] for i in range(0, len(text), width)]


# =========================
# LOAD CHAT USER
# =========================
def load_user_chats(username):
    chats = {}
    init_chat_file()

    with open(FILE_CHAT, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["sender"] != username and row["receiver"] != username:
                continue

            lawan = row["receiver"] if row["sender"] == username else row["sender"]
            session_id = normalize_session(username, lawan)

            if session_id not in chats:
                chats[session_id] = {
                    "with": lawan,
                    "messages": []
                }

            chats[session_id]["messages"].append(row)

    return chats


# =========================
# MENU CHAT
# =========================
def menu_chat(username):
    chats = load_user_chats(username)

    if not chats:
        print("\n📭 Kamu belum memiliki chat apapun.")
        input("Tekan ENTER untuk kembali...")
        return

    sessions = list(chats.keys())

    while True:
        print("\n" * 50)
        print("=========== CHAT SAYA ===========")

        for i, s in enumerate(sessions, start=1):
            print(f"{i}. Chat dengan {chats[s]['with']}")

        print("0. Kembali")
        pilihan = input(">> Pilih chat: ").strip()

        if pilihan == "0":
            return

        if not pilihan.isdigit() or not (1 <= int(pilihan) <= len(sessions)):
            print("❌ Pilihan tidak valid.")
            input("Tekan ENTER...")
            continue

        session_id = sessions[int(pilihan) - 1]
        buka_chat(username, session_id, chats[session_id]["with"])


# =========================
# BUKA CHAT (STYLE LAMA)
# =========================
def buka_chat(username, session_id, lawan):
    init_chat_file()

    print("\n" * 50)
    judul = f"=== Chat dengan {lawan} ==="
    print(f"{judul:^{WIDTH}}")
    print("=" * WIDTH)

    messages = []

    with open(FILE_CHAT, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["session"] == session_id:
                messages.append(row)

    messages.sort(key=lambda x: x["timestamp"])

    if not messages:
        print("Belum ada pesan.")
        print("=" * WIDTH)
    else:
        for m in messages:
            lines = wrap_text(m["message"], MSG_WIDTH)
            ts = m["timestamp"]

            if m["sender"] == username:
                # pesan kita (kanan)
                for line in lines:
                    print(f"{line:>{WIDTH}}")
                print(f"{ts:>{WIDTH}}")
            else:
                # pesan lawan (kiri)
                for line in lines:
                    print(f"{line:<{WIDTH}}")
                print(f"{ts:<{WIDTH}}")

            print("-" * WIDTH)

        print("=" * WIDTH)
        space = WIDTH - len(lawan) - len(username)
        print(f"{lawan}{' ' * space}{username}")

    print("\n[Ketik pesan lalu ENTER]")
    print("[ENTER kosong untuk kembali]\n")

    msg = input(">> ").strip()
    if not msg:
        return

    kirim_pesan(username, lawan, msg)


# =========================
# KIRIM PESAN
# =========================
def kirim_pesan(sender, receiver, message):
    init_chat_file()

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_id = normalize_session(sender, receiver)
    chat_id = f"{session_id}-{int(datetime.now().timestamp())}"

    with open(FILE_CHAT, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            chat_id,
            sender,
            receiver,
            message,
            waktu,
            session_id
        ])
