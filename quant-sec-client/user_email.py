import mysql.connector
from dotenv import dotenv_values
from termcolors import Bcolors
import requests
import os
import json
import crypto.crypto as crypto


config = dotenv_values(".env")

def create_and_send_email(username, serverHost):
    reciever = input("Enter the reciever username: ")
    subject = input("Enter the subject of matter: ")
    body = input("Type your message: ")

    reciever_public_key = requests.get("http://" + serverHost + "/quantserver/get-public-key/", params={
        "username": reciever
    }).json()['Public Key']

    encrypted_subject = crypto.encrypt(subject, reciever_public_key)
    encrypted_body = crypto.encrypt(body, reciever_public_key)

    requests.post(
        "http://" + serverHost + "/quantserver/post-email",
        data={
            "reciever_username": reciever,
            "sender_username": username,
            "subject": ""
        }
    )

def create_table(username):
    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database="clientdatabase"
    )

    mycursor = mydb.cursor()
    mycursor.execute(
        f"""
        CREATE TABLE {username}
        (sender_name VARCHAR(200), sender_email VARCHAR(200), subject TEXT, body TEXT, date_time_of_arrival DATETIME)
        """
    )

def show_emails(username, numberOfEmails = 5):
    # Shows the first 5 emails in the inbox
    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database="clientdatabase"
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
        print(email[1])
        print(email[4])
        print("SUBJECT: " + email[2])
        print('\n' + email[3])
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
        database="clientdatabase"
    )
    mycursor = mydb.cursor()
    
    # Get the user password
    user_password = ''
    parent_dir = os.path.expanduser("~")
    path = os.path.join(parent_dir, "quantsec/")
    with open(path + f"/{username}.json", "w") as f:
        data = json.load(f)
        user_password = data['password']

    # Import all the emails
    response = requests.get("http://" + serverHost + "/quantserver/get-inbox", params={
        "username": username,
        "password": user_password
    }).json()
    if response['Status'] == 'Negative':
        print(response['Message'])
        return
    else:
        print(response['Message'])
    
    # Put all the emails in the database
    for email in response['Emails']:
        # decrypt the contents
        email['Subject'] = crypto.decrypt(email['Subject'])
        email['Body'] = crypto.decrypt(email['Body'])
        mycursor.execute(
            f"""
            INSERT INTO {username} VALUES
            ({response['Emails']['sender']}, {response['Emails']['sender']}, {email['Subject']}, {email['Body']}, {email['datetime_of_arrival']})
            """
        )
    print("Succesfully synced all the emails")

def composeEmail(username):
    pass