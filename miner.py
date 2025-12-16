from wallet import create_wallet
from node import bc, broadcast

address, secret = create_wallet()
stats = {"completed":0,"failed":0}

print("SOI address:", address)
print("Save secret:", secret)

while True:
    block = bc.add_block(address, [], stats)
    if block:
        broadcast()
        print("⛏ Block:", block.height)
        print("Hash:", block.hash)
        print("Completed hashes:", stats["completed"])
        print("Failed hashes:", stats["failed"])
        print("Supply:", round(bc.supply,6))
        print("Difficulty:", bc.difficulty)
        print("-"*40)
