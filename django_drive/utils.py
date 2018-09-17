import hashlib


def hashed_pwd(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()
