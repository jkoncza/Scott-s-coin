import socket, threading, json
from chain import Blockchain
from block import Block

PORT = 6060
PEERS = []  # add friend IPs

bc = Blockchain()

def handle(conn):
    data = json.loads(conn.recv(999999).decode())
    chain = [Block(**b) for b in data["chain"]]
    if len(chain) > len(bc.chain):
        bc.chain = chain
        bc.balances = data["balances"]
        bc.supply = data["supply"]
    conn.close()

def listen():
    s = socket.socket()
    s.bind(("", PORT))
    s.listen()
    while True:
        c,_ = s.accept()
        handle(c)

def broadcast():
    msg = json.dumps({
        "chain":[b.__dict__ for b in bc.chain],
        "balances":bc.balances,
        "supply":bc.supply
    }).encode()

    for p in PEERS:
        try:
            s = socket.socket()
            s.connect((p, PORT))
            s.sendall(msg)
            s.close()
        except:
            pass

threading.Thread(target=listen, daemon=True).start()
