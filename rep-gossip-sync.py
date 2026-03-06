import requests
import hashlib
import json

NODES = [
    "http://127.0.0.1:8080"
]

def sha256_hex(data):
    return hashlib.sha256(data.encode()).hexdigest()

def get_chain_hash(node):
    try:
        r = requests.get(node + "/chain-hash", timeout=5)
        return r.json()["chain_hash"]
    except:
        return None

def gossip_check():

    hashes = {}

    for node in NODES:
        h = get_chain_hash(node)
        hashes[node] = h

    unique_hashes = set(hashes.values())

    if len(unique_hashes) == 1:
        print("PASS: network chain hash agreement")
    else:
        print("FAIL: chain hash mismatch")

    print(json.dumps(hashes, indent=2))


if __name__ == "__main__":
    gossip_check()
