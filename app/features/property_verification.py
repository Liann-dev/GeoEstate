import csv

FILE_PROPERTI = "data/properti.csv"

def verifikasi_dokumen_properti(id_properti):
    data = []

    with open(FILE_PROPERTI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == str(id_properti):
                row['doc_verified'] = "True"
            data.append(row)

    with open(FILE_PROPERTI, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print("Dokumen properti berhasil diverifikasi.")