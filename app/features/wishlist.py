import csv
import os

FILE_WISHLIST = "data/wishlist.csv"
FILE_PROPERTI = "data/properti.csv"


# =========================
# UTIL
# =========================
def muat_wishlist():
    if not os.path.exists(FILE_WISHLIST):
        return []

    with open(FILE_WISHLIST, newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))


def simpan_wishlist(data):
    with open(FILE_WISHLIST, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "id_properti"])
        writer.writeheader()
        writer.writerows(data)


def ambil_properti_by_id(id_properti):
    if not os.path.exists(FILE_PROPERTI):
        return None

    with open(FILE_PROPERTI, newline='', encoding='utf-8') as file:
        for p in csv.DictReader(file):
            if p["id"] == str(id_properti):
                return p
    return None


# =========================
# CORE
# =========================
def tambah_ke_wishlist(username, id_properti):
    wishlist = muat_wishlist()
    id_str = str(id_properti)

    for item in wishlist:
        if item["username"] == username and item["id_properti"] == id_str:
            print("\n❤️  Properti ini sudah ada di wishlist.")
            input("Tekan ENTER...")
            return

    p = ambil_properti_by_id(id_str)
    if not p or p.get("tersedia", "true").lower() != "true":
        print("\n❌ Properti tidak tersedia.")
        input("Tekan ENTER...")
        return

    wishlist.append({
        "username": username,
        "id_properti": id_str
    })

    simpan_wishlist(wishlist)
    print("\n✅ Properti berhasil ditambahkan ke wishlist.")
    input("Tekan ENTER...")


def hapus_dari_wishlist(username, id_properti):
    wishlist = muat_wishlist()
    id_str = str(id_properti)

    if not any(
        i for i in wishlist
        if i["username"] == username and i["id_properti"] == id_str
    ):
        print("\n❌ ID properti tidak ada di wishlist.")
        input("Tekan ENTER...")
        return

    wishlist = [
        i for i in wishlist
        if not (i["username"] == username and i["id_properti"] == id_str)
    ]

    simpan_wishlist(wishlist)
    print("\n🗑️ Properti berhasil dihapus dari wishlist.")
    input("Tekan ENTER...")


# =========================
# MENU [W]
# =========================
def menu_wishlist(username):
    from app.home.detail_properti import detail_properti  # ✅ lazy import

    while True:
        wishlist = muat_wishlist()
        id_list = [
            i["id_properti"]
            for i in wishlist
            if i["username"] == username
        ]

        print("\n=========== WISHLIST KAMU ===========")

        properti_list = []
        for pid in id_list:
            p = ambil_properti_by_id(pid)
            if p and p.get("tersedia", "true").lower() == "true":
                properti_list.append(p)
                print(f"- ID {p['id']} | {p['nama']} | Rp {p['harga']} | {p['lokasi']}")

        if not properti_list:
            print("📭 Wishlist kamu masih kosong.")
            input("Tekan ENTER...")
            return

        print("\n[Masukkan ID] Lihat Detail Properti")
        print("[H] Hapus Properti dari Wishlist")
        print("[0] Kembali")

        pilih = input(">> ").strip()

        # 🔙 Kembali
        if pilih == "0":
            return

        # 🗑️ Hapus
        if pilih.lower() == "h":
            idp = input("Masukkan ID properti yang ingin dihapus: ").strip()
            if idp:
                hapus_dari_wishlist(username, idp)
            continue

        # 🔢 Detail Properti
        if pilih.isdigit():
            prop = next((p for p in properti_list if p["id"] == pilih), None)
            if not prop:
                print("❌ ID properti tidak ditemukan.")
                input("Tekan ENTER...")
                continue

            detail_properti(username, prop)
            continue

        print("❌ Input tidak valid.")
