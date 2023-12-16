import os
from crypto.crystals.kyber import Kyber512
import json
import base64
import user_email
import requests


def help():
    with open('help.txt', 'r') as f:
        file_contents = f.read()
        print(file_contents)

def create_account(host):
    
    # Generate a CRYSTALS-kyber key pair for encryption purposes
    (public_key, private_key) = Kyber512.keygen()
    name = input("Please enter your name: ")

    # Get a unique username from the user
    while True:
        unique_username = input("Please enter an unique user_name: ")
        response = requests.get("http://" + host + "/quantserver/check-uniqueness/", params={
            "username": unique_username
        }).json()

        if response['Status'] == 'Positive':
            break
    
    # Get a password from the user
    user_password = ''
    while True:
        pswd = input("Please enter a password: ")
        cnf_pswd = input("Please confirm the password: ")
        if pswd == cnf_pswd:
            user_password = pswd
            break
        else:
            print("Passwords do not match")
    
    # Create a directory to store user data
    parent_dir = os.path.expanduser("~")
    path = os.path.join(parent_dir, "quantsec/")
    try:
        os.mkdir(path)
    except OSError:
        print("quantsec folder already exists")
    
    with open(path + f"/{unique_username}.json", "w") as f:
        user_data = {
            "Name": name,
            "UserName": unique_username,
            "Kyber Public Key": str(base64.b64encode(public_key), encoding='utf-8'),
            "Kyber Private Key": str(base64.b64encode(private_key), encoding='utf-8'),
            "Password": user_password
        }
        print(user_data)
        json_object = json.dumps(user_data, indent=4)
        f.write(json_object)

    # Create a table in database to store incomming emails
    user_email.create_table(unique_username)

    response = requests.post("http://" + host + "/quantserver/register-user", data={
        "name": name,
        "username": unique_username,
        "public_key": str(base64.b64encode(public_key), encoding='utf-8'),
        "password": user_password
    }).json()

    if response['Status'] == 'Positive':
        print("Succesfully created the account")


def handle_login(username):
    isPresent = False
    for _, _, files in os.walk("~/quantsec"):
        if username + ".json" in files:
            isPresent = True
            break
    
    return isPresent

def clearInbox(username, host):
    pass