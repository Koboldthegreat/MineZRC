from passlib.hash import sha256_crypt

def encryptPassword(password):
    hash = sha256_crypt.encrypt(password)
    return hash

def checkPassword(password, hash):
    return sha256_crypt.verify(password, hash)
