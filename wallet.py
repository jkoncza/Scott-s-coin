import secrets
from crypto import sha256

def create_wallet():
    secret = secrets.token_hex(32)
    address = sha256(secret)[:32]
    return address, secret
