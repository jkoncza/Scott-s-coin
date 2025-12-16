from wallet import create_tx
from node import broadcast_tx, mempool
from miner import wallet  # assumes miner.py is running or wallet object is available

def send_coins(to_address, amount):
    tx = create_tx(wallet, to_address, amount)
    mempool.append(tx)
    broadcast_tx(tx)
    print(f"✅ Sent {amount} SOI to {to_address}")

if __name__ == "__main__":
    print("Your address:", wallet["address"])
    while True:
        to_addr = input("Recipient address: ").strip()
        amt = float(input("Amount to send: ").strip())
        send_coins(to_addr, amt)
