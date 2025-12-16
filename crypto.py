import hashlib
from ecdsa import SigningKey, SECP256k1, VerifyingKey

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def generate_keypair():
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    return sk, vk

def sign_message(sk: SigningKey, message: str):
    return sk.sign(message.encode()).hex()

def verify_signature(vk: VerifyingKey, message: str, signature: str):
    try:
        return vk.verify(bytes.fromhex(signature), message.encode())
    except:
        return False

def pubkey_to_address(vk: VerifyingKey):
    return sha256(vk.to_string().hex())[:32]
