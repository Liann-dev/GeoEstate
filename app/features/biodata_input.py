import csv
import os
from datetime import datetime

FILE_BIODATA = "data/biodata.csv"

FIELDS = [
    "username","provinsi","kota","nik","nama_lengkap","tempat_lahir",
    "tgl_lahir","jenis_kelamin","alamat","rt","rw","kelurahan",
    "kecamatan","agama","status_kawin","pekerjaan",
    "kewarganegaraan","masa_berlaku","tgl_ktp_dibuat"
]

def input_biodata(username):
    print("\n=== INPUT DATA KTP USER ===")
    data = {"username": username}

    for field in FIELDS[1:]:
        label = field.replace("_", " ").title()
        data[field] = input(f"{label}: ")

    if not os.path.exists(FILE_BIODATA):
        with open(FILE_BIODATA, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

    with open(FILE_BIODATA, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(data)

    print("\n✅ Biodata berhasil disimpan.")
