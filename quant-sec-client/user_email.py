import mysql.connector
from dotenv import dotenv_values
from termcolors import Bcolors
import requests
import os
import json
import crypto.crypto as crypto
from datetime import datetime

config = dotenv_values(".env")


def create_and_send_email(username, serverHost):
    if username == None:
        print("You need to login first")
        return
    if serverHost == None:
        print("You need to connect to a server first")
        return

    reciever = ""
    while True:
        reciever = input("Enter the reciever username: ")
        response = requests.get(
            "http://" + serverHost + "/quantserver/check-uniqueness/",
            params={"username": reciever},
        ).json()
        if response["Status"] == "Positive":
            print(Bcolors.ERROR + "The reciever doesn't exist" + Bcolors.ENDC)
        else:
            break

    subject = input("Enter the subject of matter: ")
    body = input("Type your message: ")

    reciever_public_key = requests.get(
        "http://" + serverHost + "/quantserver/get-public-key/",
        params={"username": reciever},
    ).json()["Public Key"]

    encrypted_subject = crypto.encrypt(subject, reciever_public_key)
    encrypted_body = crypto.encrypt(body, reciever_public_key)

    # Get the user password
    user_password = ""
    parent_dir = os.path.expanduser("~")
    file_path = os.path.join(parent_dir, "quantsec/")
    with open(file_path + f"/{username}.json", "r") as f:
        data = json.load(f)
        user_password = data["Password"]

    response = requests.post(
        "http://" + serverHost + "/quantserver/post-email",
        data={
            "reciever_username": reciever,
            "sender_username": username,
            "subject": json.dumps(encrypted_subject),
            "body": json.dumps(encrypted_body),
            "password": user_password,
        },
    ).json()
    if response["Status"] == "Positive":
        print(f"Succesfully sent the email to {reciever} from {username}")
    else:
        print(Bcolors.ERROR + response["Message"] + Bcolors.ERROR)


def create_table(username):
    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database=config["DATABASE"],
    )

    mycursor = mydb.cursor()
    mycursor.execute(
        f"""
        CREATE TABLE {username}
        (sender_username VARCHAR(200), subject TEXT, body TEXT, date_time_of_arrival DATETIME)
        """
    )


def show_emails(username, numberOfEmails=5):
    if username == None:
        print("You need to login first")
        return

    # Shows the first 5 emails in the inbox
    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database=config["DATABASE"],
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        f"""
        SELECT * FROM {username}
        ORDER BY date_time_of_arrival DESC
        LIMIT {numberOfEmails}
        """
    )
    for email in mycursor:
        print(Bcolors.BOLD + email[0] + Bcolors.ENDC)
        print(email[3])
        print("SUBJECT: " + email[1])
        print("\n" + email[2])
        print("--------------------------------\n\n")


def sync_emails(username, serverHost):
    if username == None:
        print("You need to login first")
        return
    if serverHost == None:
        print("You need to connect to a server first")
        return

    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database=config["DATABASE"],
    )
    mycursor = mydb.cursor()

    # Get the user password
    user_password = ""
    parent_dir = os.path.expanduser("~")
    path = os.path.join(parent_dir, "quantsec/")
    with open(path + f"/{username}.json", "r") as f:
        data = json.load(f)
        user_password = data["Password"]

    # Import all the emails
    response = requests.get(
        "http://" + serverHost + "/quantserver/get-inbox",
        params={"username": username, "password": user_password},
    ).json()

    if response["Status"] == "Negative":
        print(response["Message"])
        return
    else:
        print("Succesfully downloaded all the emails")

    print("Decrypting downloaded emails")
    # Put all the emails in the database
    for email in response["Emails"]:
        # decrypt the contents
        email["encrypted_subject"] = json.loads(email["encrypted_subject"])
        email["encrypted_body"] = json.loads(email["encrypted_body"])

        decrypted_subject = crypto.decrypt(
            email["encrypted_subject"]["tag"],
            email["encrypted_subject"]["concatenated_string"],
            username,
        )
        decrypted_body = crypto.decrypt(
            email["encrypted_body"]["tag"],
            email["encrypted_body"]["concatenated_string"],
            username,
        )
        datetime_of_arrival = datetime.strptime(
            email["datetime_of_arrival"], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%Y-%m-%d %H:%M:%S")

        mycursor.execute(
            f"""
            INSERT INTO {username} VALUES
            ('{email['sender']}', '{decrypted_subject}', '{decrypted_body}', '{datetime_of_arrival}');
            """
        )
    mydb.commit()
    print("Succesfully synced all the emails")


def clearInbox(username, serverHost):
    if username == None:
        print("You need to login first")
        return
    if serverHost == None:
        print("You need to connect to a server first")
        return

    user_password = ""
    parent_dir = os.path.expanduser("~")
    path = os.path.join(parent_dir, "quantsec/")
    with open(path + f"/{username}.json", "r") as f:
        data = json.load(f)
        user_password = data["Password"]

    response = requests.post(
        "http://" + serverHost + "/quantserver/clear-inbox",
        data={"username": username, "password": user_password},
    ).json()

    if response["Status"] == "Negative":
        print(response["Message"])

    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database=config["DATABASE"],
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        f"""
        TRUNCATE TABLE {username};
        """
    )
    mydb.commit()

    print("Succesfully cleared the inbox")
