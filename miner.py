from wallet import create_wallet
from chain import Blockchain
from node import broadcast_block, mempool

bc = Blockchain()
wallet = create_wallet()
address = wallet["address"]
stats = {"completed":0,"failed":0}

print("SOI address:", address)
print("Private key:", wallet["private_key"])
print("Public key:", wallet["public_key"])

while True:
    # Grab pending transactions from mempool
    txs_to_mine = mempool[:10]  # up to 10 txs per block
    block = bc.add_block(address, txs_to_mine, stats)

    # Remove mined transactions from mempool
    for tx in txs_to_mine:
        if tx in mempool: mempool.remove(tx)

    # Broadcast new block
    broadcast_block(block)

    if block:
        print("⛏ Block mined:", block.height)
        print("Hash:", block.hash)
        print("Completed hashes:", stats["completed"])
        print("Failed hashes:", stats["failed"])
        print("Supply:", round(bc.supply,6))
        print("Difficulty:", bc.difficulty)
        print("-"*40)
