# Quantum Secure Email Client

### Overview
The problem with currently popular encryption algorithms is that their security relies on three hard mathematical problems which can be easily solved by a sufficiently powerful quantum computer running Shor's algorithm.<br>

This repository contains a prototype of a Quantum secure email client which uses a modified version of the TLS algorithm to send peer-to-peer encrypted emails.<br>

### Flow Chart of the encryption algorithm
![encryption](https://github.com/aaravjn/quantum-secure-email-client/assets/73699304/5b88d2ef-de78-4fdd-a14e-8363ab02c722)
The above chart contains the encryption workflow when a Sender tries to send a message to a receiver. A mutually secret key is common among both parties which remains the same throughout a session and is shared using an asymmetric quantum secure algorithm, <strong>*Crystal-Kyber*</strong>. A message is sent to the receiver which may involve a server in between encrypted using a symmetric algorithm called <strong>*AES-256*</strong>. AES-256 is used because of its efficiency in encrypting extensive data. The encrypted message and the encrypted secret key are sent to the receiver along with a tag obtained from applying the MAC algorithm on the concatenation of both to verify whether the data was not tampered with.


### Flow Chat of the decryption algorithm.
![decryption](https://github.com/aaravjn/quantum-secure-email-client/assets/73699304/536bc67b-ae10-44cd-a897-d3bf85317d0b) <br>
The receiver takes the received encrypted message and the encrypted key to verify it against the tag to check whether they still match. If yes, the receiver decrypts the secret key using its private key by applying Crystal-Kyber. After obtaining the secret key, it decrypts the message by applying AES-256 to obtain the original message.

### Application Workflow
![workflow](https://github.com/aaravjn/quantum-secure-email-client/assets/73699304/bd474c11-f5b2-48f2-bbdf-732d9efe279d) <br>
The application workflow goes as follows. The User will fetch the public key of the receiver from the hosted database and send the encrypted data containing the encrypted message, encrypted secret key and a tag. The receiver will then use the email client to fetch the encrypted data from the database and decrypt the message.


### Project setup Guide
You need to have the following packages in your system.
```
MySql
Python == 3.7
Docker
```

* `cd` into the project folder and run `pip install -r requirements.txt`

* The `.env` file in `quant-sec-client` needs to be populated with:
  - `HOST`: Your Mysql host, eg:- localhost.
  - `USER`: Your Mysql username.
  - `PASSWORD`: Your Mysql password.
  - `DATABASE`: Your database name for the quantsec application.

* To use a prebuild server image, use this command `docker pull aaravjn/quantserver`

### Usage guide
The possible commands are the following:
```
~ create-account   : Creates a new user account. Generates a new CRYSTALS-Kyber key pair and registeres it in the global database.
~ connect   : Connect to a email server by entering its Host domain.
~ login   : Use an account existing on device.
~ sync    : Retrives new emails from the inbox of the user stored in the server. The emails are always encrypted in the server.
~ list-emails   : Lists recent emails from the inbox. :: -c [Number of emails to be shown. Default value = 5]
~ compose   : Create and send a new email to a particular sender.
~ clear-inbox   : Delete all the emails in your inbox
~ exit  : Exit out of the application.
```

### Steps to send an email

1. Connect to a Host server
```
> connect
Please enter the host server domain: 0.0.0.0:8000
```

2. Create an account
```
> create-account
Please enter your name: Aarav
Please enter an unique user_name: aarav
Please enter a password: 12345
Please confirm the password: 12345
Succesfully created the account
```

3. Login to your account
```
> login
Enter the username: aarav
```

4. Send an email to a user with a known username (drac).
```
> compose
Enter the reciever username: drac
Enter the subject of matter: hi    
Type your message: hi drac, How are you?
Succesfully sent the email to drac from aarav
```

5. Sync the emails (from drac's device)
```
> sync
Succesfully downloaded all the emails
Decrypting downloaded emails
Succesfully synced all the emails
```

6. List all the emails (in drac's device)
```
> list-emails
aarav
2023-12-21 18:56:25
SUBJECT: hi

hi drac, How are you?
--------------------------------


```