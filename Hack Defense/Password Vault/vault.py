# password_vault/vault.py
import json, os, getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64

DB = "vault.db"
SALT = b"vault_salt_12345"

def derive_key(password: str) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT, iterations=100_000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def load_db():
    if not os.path.exists(DB):
        return {}
    return json.load(open(DB))

def save_db(d):
    json.dump(d, open(DB,"w"))

def add_entry(key, username, secret, f):
    db = load_db()
    db[key] = {"user": username, "secret": f.encrypt(secret.encode()).decode()}
    save_db(db)

def get_entry(key, f):
    db = load_db()
    if key not in db:
        print("Not found")
        return
    info = db[key]
    print("User:", info["user"])
    print("Secret:", f.decrypt(info["secret"].encode()).decode())

def main():
    pw = getpass.getpass("Master password: ")
    key = derive_key(pw)
    f = Fernet(key)
    print("1:add 2:get 3:list")
    cmd = input("> ").strip()
    if cmd=="1":
        k = input("Key name: ")
        u = input("Username: ")
        s = getpass.getpass("Secret: ")
        add_entry(k,u,s,f); print("Saved.")
    elif cmd=="2":
        k = input("Key name: "); get_entry(k,f)
    elif cmd=="3":
        print(load_db().keys())
    else:
        print("bye")

if __name__=="__main__":
    main()