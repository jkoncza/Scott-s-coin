import json, os
from block import Block
from wallet import verify_tx

MAX_SUPPLY = 100_000_000
REWARD = 0.001
TARGET_TIME = 120
CHAIN_FILE = "chain.json"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.balances = {}
        self.supply = 0
        self.difficulty = 4
        self.last_time = 0
        self.load_chain()

    def load_chain(self):
        if os.path.exists(CHAIN_FILE):
            with open(CHAIN_FILE,"r") as f:
                data = json.load(f)
                for b in data["chain"]:
                    block = Block(**b)
                    self.chain.append(block)
                self.balances = data["balances"]
                self.supply = data["supply"]
                self.last_time = data.get("last_time",0)
        else:
            genesis = Block(0,"0",[])
            self.chain.append(genesis)
            self.last_time = genesis.time
            self.save_chain()

    def save_chain(self):
        with open(CHAIN_FILE,"w") as f:
            json.dump({
                "chain":[b.__dict__ for b in self.chain],
                "balances": self.balances,
                "supply": self.supply,
                "last_time": self.last_time
            }, f, indent=2)

    def last_block(self):
        return self.chain[-1]

    def validate_tx(self, tx):
        if not verify_tx(tx):
            return False
        if tx["from"] != "COINBASE" and self.balances.get(tx["from"],0) < tx["amount"]:
            return False
        return True

    def add_block(self, miner, txs, stats):
        valid_txs = [tx for tx in txs if self.validate_tx(tx)]
        reward = min(REWARD, MAX_SUPPLY - self.supply)
        if self.supply < MAX_SUPPLY:
            valid_txs.append({"from":"COINBASE","to":miner,"amount":reward,"public_key":None,"signature":None})

        block = Block(len(self.chain), self.last_block().hash, valid_txs)
        block.mine(self.difficulty, stats)

        now = block.time
        delta = now - self.last_time
        self.last_time = now
        if delta < TARGET_TIME:
            self.difficulty += 1
        elif delta > TARGET_TIME*2 and self.difficulty > 1:
            self.difficulty -= 1

        for tx in valid_txs:
            self.balances[tx["to"]] = self.balances.get(tx["to"],0) + tx["amount"]
            if tx["from"] != "COINBASE":
                self.balances[tx["from"]] -= tx["amount"]

        self.supply += reward
        self.chain.append(block)
        self.save_chain()
        return block
