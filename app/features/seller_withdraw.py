import csv
import os
import random

WITHDRAW_FILE = "data/selldraw.csv"
USERS_FILE = "data/users.csv"

def get_user_by_username(username):
    with open(USERS_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user["username"] == username:
                return user
    return None

def init_withdraw_file():
    if not os.path.exists(WITHDRAW_FILE):
        with open(WITHDRAW_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["wd_id", "username", "email", "reason", "status"])

def generate_wd_id(existing_ids):
    while True:
        wd_id = f"WD-{random.randint(1000, 9999)}"
        if wd_id not in existing_ids:
            return wd_id