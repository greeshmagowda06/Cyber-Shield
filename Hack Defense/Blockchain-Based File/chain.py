# file_chain/chain.py
import hashlib, json, time, os, sys, argparse

CHAIN = "chain.json"
GENESIS_PREV_HASH = "0" * 64

def sha256(fpath):
    """Calculates the SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(fpath, "rb") as f:
        # Read the file in chunks to handle large files efficiently
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def load_chain():
    """Loads the blockchain from the chain file."""
    if not os.path.exists(CHAIN):
        return []
    try:
        with open(CHAIN, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading chain file: {e}")
        sys.exit(1)

def save_chain(ch):
    """Saves the blockchain to the chain file."""
    with open(CHAIN, "w") as f:
        json.dump(ch, f, indent=2)

def get_block_hash(block_data):
    """Calculates the hash of a block's data."""
    block_str = json.dumps(block_data, sort_keys=True).encode()
    return hashlib.sha256(block_str).hexdigest()

def add_file(fpath):
    """Adds a file to the blockchain."""
    if not os.path.exists(fpath):
        print(f"Error: File not found at '{fpath}'")
        return

    chain = load_chain()
    prev = chain[-1]["block_hash"] if chain else GENESIS_PREV_HASH
    filehash = sha256(fpath)

    block = {"timestamp": time.time(), "file": os.path.basename(fpath), "sha256": filehash, "prev": prev}
    block["block_hash"] = get_block_hash(block)

    chain.append(block)
    save_chain(chain)
    print(f"✅ File '{os.path.basename(fpath)}' added to the chain. Block hash: {block['block_hash']}")

def verify_chain():
    """Verifies the integrity of the entire blockchain."""
    chain = load_chain()
    for i, block in enumerate(chain):
        # Verify block hash
        block_data = {k: v for k, v in block.items() if k != "block_hash"}
        calculated_hash = get_block_hash(block_data)
        if calculated_hash != block["block_hash"]:
            print(f"❌ Tamper detected at block {i} ('{block.get('file')}'). Hash mismatch.")
            print(f"   Expected:   {block['block_hash']}")
            print(f"   Calculated: {calculated_hash}")
            return

        # Verify link to previous block
        if i > 0 and block["prev"] != chain[i - 1]["block_hash"]:
            print(f"❌ Broken chain detected at block {i}. Previous block hash mismatch.")
            print(f"   Expected: {chain[i-1]['block_hash']}")
            print(f"   Got:      {block['prev']}")
            return
    print("✅ Chain integrity verified. OK.")

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description="A simple blockchain-based file integrity checker."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
    
    # 'add' command parser
    parser_add = subparsers.add_parser("add", help="Add a file to the blockchain.")
    parser_add.add_argument("filepath", type=str, help="The path to the file to add.")
    
    # 'verify' command parser
    parser_verify = subparsers.add_parser("verify", help="Verify the integrity of the blockchain.")
    
    args = parser.parse_args()
    if args.command == "add":
        add_file(args.filepath)
    elif args.command == "verify":
        verify_chain()
