import time
import json
from crypto import sha256

class Block:
    def __init__(self, height, prev_hash, txs, nonce=0, timestamp=None):
        self.height = height
        self.prev_hash = prev_hash
        self.txs = txs
        self.nonce = nonce
        self.time = timestamp or time.time()
        self.hash = self.calc_hash()

    def calc_hash(self):
        return sha256(f"{self.height}{self.prev_hash}{json.dumps(self.txs)}{self.nonce}{self.time}")

    def mine(self, difficulty, stats):
        target = "0"*difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calc_hash()
            stats["failed"] += 1
        stats["completed"] += 1
