from crypto import generate_keypair, pubkey_to_address, sign_message, VerifyingKey, verify_signature

def create_wallet():
    sk, vk = generate_keypair()
    address = pubkey_to_address(vk)
    return {
        "private_key": sk.to_string().hex(),
        "public_key": vk.to_string().hex(),
        "address": address,
        "sk_obj": sk,
        "vk_obj": vk
    }

def create_tx(sender_wallet, to_address, amount):
    tx = {
        "from": sender_wallet["address"],
        "to": to_address,
        "amount": amount,
        "public_key": sender_wallet["public_key"]
    }
    tx_str = f"{tx['from']}{tx['to']}{tx['amount']}"
    signature = sign_message(sender_wallet["sk_obj"], tx_str)
    tx["signature"] = signature
    return tx

def verify_tx(tx):
    if tx["from"] == "COINBASE":
        return True
    vk = VerifyingKey.from_string(bytes.fromhex(tx["public_key"]), curve=SECP256k1)
    tx_str = f"{tx['from']}{tx['to']}{tx['amount']}"
    return verify_signature(vk, tx_str, tx["signature"])
