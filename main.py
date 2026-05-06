# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.

import smtplib
import datetime as dt
import socket
import pandas as pd
from pathlib import Path
from random import choice
import os

PLACEHOLDER = "[NAME]"

# --------------------------------- EMAIL DATA SETUP --------------------------------- #
# import os and use it to get the Github repository secrets
sender_email = os.environ.get("MY_EMAIL")
sender_password = os.environ.get("MY_PASSWORD")

# ------------------------------------- LOAD DATA ------------------------------------ #
base_dir = Path(__file__).resolve().parent
birthdays_file_path = base_dir / "birthdays.csv"
letter_templates = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]
df = pd.read_csv(birthdays_file_path, index_col = 0)
birthdays = list(df.itertuples(name = None))

# ---------------------------- GET ELIGIBLE DATA FOR WISHES -------------------------- #
def select_template():
    letter = choice(letter_templates)
    local_file_path = f"letter_templates/{letter}"
    letter_template_path = base_dir / local_file_path
    with open(letter_template_path, "r") as f:
        template = f.read().splitlines()
    return template

def generate_birthday_wish(name, template):
    letter = template.copy()
    letter[0] = letter[0].replace("[NAME]", name)
    subject_line = "Subject: Birthday Wish\n\n"
    birthday_wish = subject_line + "\n".join(letter)
    return birthday_wish

def send_birthday_wish(recipient, wish):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(sender_email, sender_password)
        try:
            connection.sendmail(from_addr=sender_email,
                                to_addrs=recipient,
                                msg=wish)
            return True
        except (smtplib.SMTPRecipientsRefused,
                smtplib.SMTPSenderRefused,
                smtplib.SMTPDataError,
                smtplib.SMTPConnectError,
                smtplib.SMTPServerDisconnected,
                smtplib.SMTPAuthenticationError,
                socket.error) as e:
            print(f"{type(e).__name__}: {e}")
            return False

today = dt.datetime.now()
month = today.month
day = today.day
today_birthdays = tuple(x for x in birthdays if x[3] == month and x[4] == day)

for birthday in today_birthdays:
    letter_template = select_template()
    message = generate_birthday_wish(birthday[0], letter_template)
    recipient_email = birthday[1]
    print(f"Sending Birthday Wish to {recipient_email}....")
    if send_birthday_wish(recipient_email, message):
        print(f"Birthday Wish successfully sent to {recipient_email}. ✅")
    else:
        print(f"Sending Birthday Wish to {recipient_email} failed. Please try again. ⛔")
