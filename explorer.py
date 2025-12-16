from chain import Blockchain

bc = Blockchain()

def show_balances():
    print("\n=== Balances ===")
    for addr, bal in bc.balances.items():
        print(f"{addr}: {round(bal,6)} SOI")
    print("================\n")

def show_blocks(last_n=10):
    print(f"\n=== Last {last_n} Blocks ===")
    for block in bc.chain[-last_n:]:
        print(f"Block #{block.height} | Hash: {block.hash}")
        print("Txs:")
        for tx in block.txs:
            print(f"  {tx['from']} → {tx['to']} : {tx['amount']} SOI")
        print("-"*40)
    print("================\n")

while True:
    print("1. Show balances")
    print("2. Show last blocks")
    choice = input("Choice: ")
    if choice == "1":
        show_balances()
    elif choice == "2":
        show_blocks()
    else:
        print("Invalid choice")
