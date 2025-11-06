import hashlib, json, time, os

CHAIN = "chain.json"
GENESIS_PREV_HASH = "0" * 64

# -----------------------------------
# 🧩 Utility Functions
# -----------------------------------
def sha256(fpath):
    """Calculate SHA256 hash of a file (efficient for large files)."""
    h = hashlib.sha256()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def load_chain():
    """Load blockchain from disk."""
    if not os.path.exists(CHAIN):
        return []
    try:
        with open(CHAIN, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️  Error loading chain file: {e}")
        return []

def save_chain(chain):
    """Save blockchain to disk."""
    with open(CHAIN, "w") as f:
        json.dump(chain, f, indent=2)

def get_block_hash(block_data):
    """Compute hash for a block."""
    block_str = json.dumps(block_data, sort_keys=True).encode()
    return hashlib.sha256(block_str).hexdigest()


# -----------------------------------
# 🧱 Blockchain Core Functions
# -----------------------------------
def add_file(filepath):
    """Add a file's hash to the blockchain."""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    chain = load_chain()
    prev_hash = chain[-1]["block_hash"] if chain else GENESIS_PREV_HASH
    filehash = sha256(filepath)

    block = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "file": os.path.basename(filepath),
        "path": os.path.abspath(filepath),
        "sha256": filehash,
        "prev": prev_hash,
    }
    block["block_hash"] = get_block_hash(block)
    chain.append(block)
    save_chain(chain)
    print(f"✅ File '{os.path.basename(filepath)}' added to blockchain.")
    print(f"   Block hash: {block['block_hash']}\n")


def verify_chain():
    """Verify blockchain integrity."""
    chain = load_chain()
    if not chain:
        print("⚠️  No chain data found. Add files first.")
        return

    for i, block in enumerate(chain):
        # Check block hash validity
        block_data = {k: v for k, v in block.items() if k != "block_hash"}
        calc_hash = get_block_hash(block_data)
        if calc_hash != block["block_hash"]:
            print(f"❌ Tamper detected at block {i} ({block['file']}) — block hash mismatch!")
            print(f"   Expected: {block['block_hash']}")
            print(f"   Calculated: {calc_hash}\n")
            return

        # Check chain link
        if i > 0 and block["prev"] != chain[i - 1]["block_hash"]:
            print(f"❌ Chain broken between block {i-1} and {i} ({block['file']})!")
            return

    print("✅ Blockchain integrity verified. All records are intact.\n")


def list_blocks():
    """List all stored file records."""
    chain = load_chain()
    if not chain:
        print("⚠️  No files have been added yet.")
        return
    print("\n📜 Blockchain Records:")
    for i, block in enumerate(chain, start=1):
        print(f"{i}. {block['file']} — SHA256: {block['sha256'][:10]}...  ({block['timestamp']})")
    print()


# -----------------------------------
# 🖥️ Interactive Menu
# -----------------------------------
def main():
    print("===============================================")
    print("🔐 Blockchain-Based File Integrity Verifier")
    print("===============================================")

    while True:
        print("""
1️⃣  Add a file to blockchain
2️⃣  Verify blockchain integrity
3️⃣  List all recorded files
4️⃣  Exit
""")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            fpath = input("Enter file path to add: ").strip()
            if fpath:
                add_file(fpath)
            else:
                print("⚠️  No path provided.")
        elif choice == "2":
            verify_chain()
        elif choice == "3":
            list_blocks()
        elif choice == "4":
            print("👋 Exiting verifier. Stay secure!")
            break
        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    main()
