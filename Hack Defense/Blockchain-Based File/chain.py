# file_chain/chain.py
import hashlib, json, time, os, sys

CHAIN = "chain.json"

def sha256(fpath):
    h=hashlib.sha256()
    with open(fpath,"rb") as f:
        while True:
            b = f.read(4096)
            if not b: break
            h.update(b)
    return h.hexdigest()

def load_chain():
    if not os.path.exists(CHAIN): return []
    return json.load(open(CHAIN))

def save_chain(ch):
    json.dump(ch, open(CHAIN,"w"), indent=2)

def add_file(fpath):
    chain = load_chain()
    prev = chain[-1]["block_hash"] if chain else "0"*64
    filehash = sha256(fpath)
    block = {"timestamp": time.time(), "file": os.path.basename(fpath), "sha256": filehash, "prev": prev}
    block_str = json.dumps(block, sort_keys=True).encode()
    block_hash = hashlib.sha256(block_str).hexdigest()
    block["block_hash"] = block_hash
    chain.append(block)
    save_chain(chain)
    print("Added block:", block_hash)

def verify_chain():
    chain = load_chain()
    for i,b in enumerate(chain):
        data = dict(b); data.pop("block_hash")
        if hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest() != b["block_hash"]:
            print("Tamper at index", i); return
        if i>0 and b["prev"] != chain[i-1]["block_hash"]:
            print("Broken chain at", i); return
    print("Chain OK")

if __name__=="__main__":
    cmd = sys.argv[1]
    if cmd=="add": add_file(sys.argv[2])
    elif cmd=="verify": verify_chain()
    else: print("add/verify")