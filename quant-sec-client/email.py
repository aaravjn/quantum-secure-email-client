import mysql.connector
from dotenv import dotenv_values
from termcolors import Bcolors

config = dotenv_values(".env")

def create_and_send_email(reciever):
    pass

def create_database():
    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database="clientdatabase"
    )

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        CREATE TABLE user_emails
        (sender_name VARCHAR(200), sender_email VARCHAR(200), subject TEXT, body TEXT, date_time_of_arrival DATETIME)
        """
    )

def show_emails(pageNumber = 1):
    # Shows the first 5 emails in the inbox
    
    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database="clientdatabase"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT * FROM user_emails
        ORDER BY date_time_of_arrival DESC
        LIMIT 5
        """
    )
    for email in mycursor:
        print(Bcolors.BOLD + email[0] + Bcolors.ENDC)
        print(email[1])
        print(email[4])
        print("SUBJECT: " + email[2])
        print('\n' + email[3])
        print("--------------------------------\n\n")

def sync_emails():
    # test function

    mydb = mysql.connector.connect(
        host=config["HOST"],
        user=config["USER"],
        password=config["PASSWORD"],
        database="clientdatabase"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")