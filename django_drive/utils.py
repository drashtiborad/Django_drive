import hashlib
from _datetime import datetime


def hashed_pwd(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def generate_filename(filename, id):
    return hashlib.md5((filename+str(id)+datetime.strftime(datetime.now(),format='%Y%m%d%H%M%S')).encode('utf-8'))\
            .hexdigest()
