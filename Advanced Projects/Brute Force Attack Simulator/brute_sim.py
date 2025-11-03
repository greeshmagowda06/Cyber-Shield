"""
Brute-force / dictionary attack simulator (educational).
Uses SHA256 hashes and a small dictionary. Only for testing on hashes
you own (e.g., hashes you generate locally). This is NOT intended
for attacking third-party systems.
"""

import hashlib
import itertools
import time

# small sample dictionary (you can replace with a file list)
DICTIONARY = ["password", "123456", "admin", "letmein", "qwerty", "welcome"]

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def dictionary_attack(target_hash, wordlist):
    start = time.time()
    for word in wordlist:
        if sha256_hex(word) == target_hash:
            return word, time.time() - start
    return None, time.time() - start

def brute_charset_attack(target_hash, charset, max_len=4):
    start = time.time()
    for length in range(1, max_len + 1):
        for cand in itertools.product(charset, repeat=length):
            s = "".join(cand)
            if sha256_hex(s) == target_hash:
                return s, time.time() - start
    return None, time.time() - start

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Educational brute-force / dictionary attack simulator."
                                                 " Use only on hashes you control.")
    parser.add_argument("--secret", help="Secret/password to hash (if omitted, runs interactively)")
    parser.add_argument("--mode", choices=["dictionary", "brute"], default="dictionary",
                        help="Attack mode: dictionary or brute (default: dictionary)")
    parser.add_argument("--wordlist", help="Path to a wordlist file (one password per line)")
    parser.add_argument("--charset", default="abc123",
                        help="Charset to use for brute-force (default: 'abc123')")
    parser.add_argument("--max-len", type=int, default=3, help="Max length for brute-force (default: 3)")
    args = parser.parse_args()

    print("=== Brute Force Simulator (educational) ===")
    # interactive path if no secret provided
    if not args.secret:
        secret = input("Enter a secret/password to hash (this is local test): ").strip()
        target = sha256_hex(secret)
        print(f"Target SHA256 hash (local): {target}\n")

        print("1) Run dictionary attack")
        print("2) Run small charset brute-force (a-z, max length 3)")
        choice = input("Choose option (1/2): ").strip()

        if choice == "1":
            # use built-in DICTIONARY
            found, elapsed = dictionary_attack(target, DICTIONARY)
            if found:
                print(f"[FOUND] '{found}' in {elapsed:.2f}s")
            else:
                print(f"Not found in dictionary (took {elapsed:.2f}s)")
        else:
            charset = "abc123"  # small charset to keep runtime low
            found, elapsed = brute_charset_attack(target, charset, max_len=3)
            if found:
                print(f"[FOUND] '{found}' in {elapsed:.2f}s")
            else:
                print(f"Not found (took {elapsed:.2f}s). Increase charset/length for deeper search.")
    else:
        target = sha256_hex(args.secret)
        print(f"Target SHA256 hash (local): {target}\n")
        if args.mode == "dictionary":
            if args.wordlist:
                try:
                    with open(args.wordlist, "r", encoding="utf-8") as wl:
                        words = [w.strip() for w in wl if w.strip()]
                except FileNotFoundError:
                    print(f"Wordlist not found: {args.wordlist}")
                    raise
            else:
                words = DICTIONARY
            found, elapsed = dictionary_attack(target, words)
            if found:
                print(f"[FOUND] '{found}' in {elapsed:.2f}s")
            else:
                print(f"Not found in dictionary (took {elapsed:.2f}s)")
        else:
            found, elapsed = brute_charset_attack(target, args.charset, max_len=args.max_len)
            if found:
                print(f"[FOUND] '{found}' in {elapsed:.2f}s")
            else:
                print(f"Not found (took {elapsed:.2f}s). Increase charset/length for deeper search.")
