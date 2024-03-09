import hashlib
import crypto.aes as aes
from crypto.crystal.kyber import Kyber512
import json
import base64
import os


def encrypt(message, reciever_kyber_public_key):
    # Encrypt the key using crystals-kyber
    reciever_kyber_public_key = base64.b64decode(reciever_kyber_public_key)
    encrypted_aes_shared_passkey, aes_shared_passkey = Kyber512.enc(
        reciever_kyber_public_key
    )

    aes_shared_passkey = str(base64.b64encode(aes_shared_passkey), encoding="utf-8")
    encrypted_data = aes.encrypt(message, aes_shared_passkey)
    aes_cipher_text = encrypted_data["cipher_text"]
    aes_salt = encrypted_data["salt"]

    # Generate a tag for verification purposes
    concetanated_string = json.dumps(
        {
            "salt": aes_salt,
            "cipher_text": aes_cipher_text,
            "encrypted_passkey": str(
                base64.b64encode(encrypted_aes_shared_passkey), encoding="utf-8"
            ),
        }
    )

    tag = hashlib.sha256(concetanated_string.encode()).hexdigest()
    return {"tag": tag, "concatenated_string": concetanated_string}


def decrypt(tag, concetanated_string, username):
    # Verify it against the tag
    gen_tag = hashlib.sha256(concetanated_string.encode()).hexdigest()
    assert tag == gen_tag

    enc_data = json.loads(concetanated_string)
    cipher_text = enc_data["cipher_text"]
    encrypted_passkey = enc_data["encrypted_passkey"]
    salt = enc_data["salt"]

    reciever_private_key = ""
    parent_dir = os.path.expanduser("~")
    path = os.path.join(parent_dir, "quantsec/")

    with open(path + f"{username}.json", "r") as f:
        data = json.load(f)
        reciever_private_key = data["Kyber Private Key"]

    # Decrypt the passkey
    passkey = Kyber512.dec(
        base64.b64decode(encrypted_passkey), base64.b64decode(reciever_private_key)
    )

    # Decrypt the cipher text using the decrypted passkey
    decrypted_cipher = aes.decrypt(
        {"salt": salt, "cipher_text": cipher_text},
        str(base64.b64encode(passkey), encoding="utf-8"),
    )

    return str(decrypted_cipher, encoding="utf-8")
