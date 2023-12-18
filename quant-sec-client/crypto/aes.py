import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import os


def pad(s):
    block_size = 16
    remainder = len(s) % block_size
    padding_needed = block_size - remainder
    return s + padding_needed * " "


def unpad(s):
    return s.rstrip()


def encrypt(plain_text, passkey):
    salt = os.urandom(AES.block_size)
    private_key = hashlib.scrypt(
        passkey.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32
    )
    padded_text = pad(plain_text)
    cipher_config = AES.new(private_key, AES.MODE_ECB)

    return {
        "cipher_text": str(
            base64.b64encode(cipher_config.encrypt(bytes(padded_text, "UTF-8"))),
            encoding="utf-8",
        ),
        "salt": str(base64.b64encode(salt), encoding="utf-8"),
    }


def decrypt(enc_dict, passkey):
    salt = base64.b64decode(enc_dict["salt"])
    enc = base64.b64decode(enc_dict["cipher_text"])
    private_key = hashlib.scrypt(
        passkey.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32
    )

    cipher = AES.new(private_key, AES.MODE_ECB)
    decrypted = cipher.decrypt(enc)
    original = unpad(decrypted)

    return original
