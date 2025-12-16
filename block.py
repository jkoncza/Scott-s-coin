import time
from crypto import sha256

class Block:
    def __init__(self, height, prev_hash, txs, nonce=0):
        self.height = height
        self.prev_hash = prev_hash
        self.txs = txs
        self.time = time.time()
        self.nonce = nonce
        self.hash = self.calc()

    def calc(self):
        return sha256(f"{self.height}{self.prev_hash}{self.txs}{self.time}{self.nonce}")

    def mine(self, difficulty, stats):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calc()
            stats["failed"] += 1
        stats["completed"] += 1
