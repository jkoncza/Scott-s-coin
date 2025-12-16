import socket, threading, json
from chain import Blockchain
from block import Block

PORT = 6060
PEERS = []  # add IPs of friends/nodes like ["192.168.1.5"]
bc = Blockchain()
mempool = []  # pending transactions
seen_blocks = set()
seen_txs = set()

def handle(conn):
    try:
        data = json.loads(conn.recv(10_000_000).decode())
        msg_type = data.get("type")
        payload = data.get("data")
        if msg_type == "block":
            block_hash = payload["hash"]
            if block_hash in seen_blocks: return
            seen_blocks.add(block_hash)
            block = Block(**payload)
            # Only add if valid and height correct
            if block.height == len(bc.chain):
                bc.chain.append(block)
                for tx in block.txs:
                    if tx in mempool: mempool.remove(tx)
                    # update balances
                    bc.balances[tx["to"]] = bc.balances.get(tx["to"],0)+tx["amount"]
                    if tx["from"] != "COINBASE":
                        bc.balances[tx["from"]] -= tx["amount"]
                bc.save_chain()
                broadcast_block(block)
        elif msg_type == "tx":
            tx_id = json.dumps(payload, sort_keys=True)
            if tx_id in seen_txs: return
            seen_txs.add(tx_id)
            mempool.append(payload)
            broadcast_tx(payload)
    except Exception as e:
        print("Error handling peer:", e)
    finally:
        conn.close()

def listen():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("",PORT))
    s.listen()
    print(f"Node listening on port {PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle,args=(conn,),daemon=True).start()

def broadcast(msg):
    for p in PEERS:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((p,PORT))
            s.sendall(msg)
            s.close()
        except: pass

def broadcast_block(block):
    msg = json.dumps({"type":"block","data":block.__dict__}).encode()
    broadcast(msg)

def broadcast_tx(tx):
    msg = json.dumps({"type":"tx","data":tx}).encode()
    broadcast(msg)

threading.Thread(target=listen,daemon=True).start()
