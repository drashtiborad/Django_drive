import hashlib
from datetime import datetime


def hashed_pwd(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def generate_filename(filename, id):
    return hashlib.md5((filename + str(id) + datetime.strftime(datetime.now(), format='%Y%m%d%H%M%S')).encode('utf-8')) \
        .hexdigest()


def now():
    return datetime.now()


def num_sec(timeObj):
    return int((timeObj - datetime(2001, 1, 1)).total_seconds())
