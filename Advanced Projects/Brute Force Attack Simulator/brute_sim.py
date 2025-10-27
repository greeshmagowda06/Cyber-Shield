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
    print("=== Brute Force Simulator (educational) ===")
    secret = input("Enter a secret/password to hash (this is local test): ").strip()
    target = sha256_hex(secret)
    print(f"Target SHA256 hash (local): {target}\n")

    print("1) Run dictionary attack")
    print("2) Run small charset brute-force (a-z, max length 3)")
    choice = input("Choose option (1/2): ").strip()

    if choice == "1":
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
