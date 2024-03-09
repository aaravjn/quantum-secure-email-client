import json
import crypto.crypto as crypto
import os
import time

parent_dir = os.path.expanduser("~")
path = os.path.join(parent_dir, "quantsec/")

with open(path + f"aarav.json", "r") as f:
    data = json.load(f)
    reciever_public_key = data["Kyber Public Key"]
    reciever_private_key = data['Kyber Private Key']

a1 = time.perf_counter()
data = crypto.encrypt("a" * (10**3), reciever_public_key)
b1 = time.perf_counter()
c1 = b1 - a1
print(c1 * 10**3)

a2 = time.perf_counter()
msg = crypto.decrypt(data['tag'], data['concatenated_string'], 'aarav')
b2 = time.perf_counter()
c2 = b2 - a2
print(c2 * 10**3)
