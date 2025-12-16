import hashlib

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def sign(message, secret):
    return sha256(message + secret)
