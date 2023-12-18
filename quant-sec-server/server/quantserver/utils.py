import hashlib


def verifyUser(user_object, pswd) -> bool:
    hashed_pswd = hashlib.sha256(
        str(pswd + user_object.salt).encode("utf-8")
    ).hexdigest()

    if user_object.hashed_password != hashed_pswd:
        return False
    return True
