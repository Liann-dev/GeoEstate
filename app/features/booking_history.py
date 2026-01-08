import csv
import os
from datetime import datetime

FILE_HISTORY = "data/booking_history.csv"

FIELDNAMES = [
    "id_transaksi",
    "aksi",
    "oleh",
    "tanggal_lama",
    "tanggal_baru",
    "waktu"
]


def simpan_booking_history(
    id_transaksi,
    aksi,
    oleh,
    tanggal_lama,
    tanggal_baru
):
    os.makedirs("data", exist_ok=True)

    data = {
        "id_transaksi": id_transaksi,
        "aksi": aksi,
        "oleh": oleh,
        "tanggal_lama": tanggal_lama,
        "tanggal_baru": tanggal_baru,
        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tulis_header = not os.path.exists(FILE_HISTORY)

    with open(FILE_HISTORY, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if tulis_header:
            writer.writeheader()
        writer.writerow(data)
