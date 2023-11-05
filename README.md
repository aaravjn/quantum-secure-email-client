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
