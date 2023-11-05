### Quantum Secure Email Client

# Overview
The problem with currently popular encryption algorithms is that their security relies on three hard mathematical problems which can be easily solved a sufficiently powerful quantum computer running Shor's algorithm.<br>

This repository contians a prototype of a Quantum secure email client which uses a modified version of TLS algorithm, to send peer to peer encrypted emails.<br>

# Flow Chart of the encryption algorithm.
The above chart contains the encryption work flow when a Sender tries to send a message to a reciever. A mutually secret key is common among both the parties which remains the same throughout a session and is shared using an asymmetric quantum secure algorithm, <strong>*Crystal-Kyber*</strong>. A message is sent to the reciever which may involve a server in between encrypted using a symmetric algorithm called <strong>*AES-256*</strong>. The reason why AES-256 is used because of its effeciency to encrypt large data. The encrypted message and the encrypted secret key are sent to the reciever along with a tag obtained from applying MAC algorithm on the concatenation of both, to verify whether the data was not tampered.



# Flow Chat of the decryption algorithm.
The reciever takes the recieved encrypted message and the encrypted key to verify it against the tag to check whether they still match. If yes, the reciever decrypts the secret key usign its private key by applying Crystal-Kyber. After obtaining the secret key, it decrypts the message by applying AES-256 to obtain the original message.