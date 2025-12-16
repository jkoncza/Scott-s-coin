from block import Block
import time

MAX_SUPPLY = 100_000_000
REWARD = 0.001
TARGET_TIME = 120

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, "0", [], 0)]
        self.balances = {}
        self.supply = 0
        self.difficulty = 4
        self.last_time = time.time()

    def last(self):
        return self.chain[-1]

    def add_block(self, miner, txs, stats):
        if self.supply >= MAX_SUPPLY:
            return None

        reward = min(REWARD, MAX_SUPPLY - self.supply)
        txs.append({"from":"COINBASE","to":miner,"amount":reward})

        block = Block(len(self.chain), self.last().hash, txs)
        block.mine(self.difficulty, stats)

        now = time.time()
        delta = now - self.last_time
        self.last_time = now

        if delta < TARGET_TIME:
            self.difficulty += 1
        elif delta > TARGET_TIME * 2 and self.difficulty > 1:
            self.difficulty -= 1

        for tx in txs:
            self.balances[tx["to"]] = self.balances.get(tx["to"],0) + tx["amount"]
            if tx["from"] != "COINBASE":
                self.balances[tx["from"]] -= tx["amount"]

        self.supply += reward
        self.chain.append(block)
        return block
