import hashlib
import aes
from crystals.kyber import Kyber512
import json

def encrypt(message, reciever_kyber_public_key):

    # Request it from the server
    
    # Encrypt the key using crystals-kyber
    encrypted_aes_shared_passkey, aes_shared_passkey = Kyber512.enc(reciever_kyber_public_key)
    
    encrypted_data = aes.encrypt(message, aes_shared_passkey)
    aes_cipher_text = encrypted_data['cipher_text']
    aes_salt = encrypted_data['salt']

    # Generate a tag for verification purposes
    concetanated_string = json.dumps({
        'salt': aes_salt,
        'cipher_text': aes_cipher_text,
        'encrypted_passkey': encrypted_aes_shared_passkey
    })
    
    tag = hashlib.sha256(concetanated_string)
    return {
        "tag": tag,
        "concatenated_string": concetanated_string
    }

def decrypt(tag, salt, cipher_text, encrypted_passkey, reciever_private_key):
    # Verify it against the tag
    gen_tag = hashlib.sha256(json.dumps({
        'salt': salt,
        'cipher_text': cipher_text,
        'encrypted_passkey': encrypted_passkey
    }))
    assert tag == gen_tag
    
    # Decrypt the passkey
    passkey = Kyber512.dec(cipher_text, reciever_private_key)
    
    # Decrypt the cipher text using the decrypted passkey
    decrypted_cipher = aes.decrypt({
        'salt': salt,
        'cipher_text': cipher_text
    }, passkey)

    return decrypted_cipher