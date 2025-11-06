import json, os, sys, base64
import msvcrt  # Windows-only keyboard input
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

DB_FILE = "vault.db"
SALT = b"vault_salt_12345"


# -----------------------------
# 🔑 Key Derivation
# -----------------------------
def derive_key(master_password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=200_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


# -----------------------------
# 🧠 Cross-platform secure password input (shows *)
# -----------------------------
def input_password(prompt="Password: "):
    """Secure password input that displays * instead of blank (Windows/macOS/Linux)."""
    print(prompt, end="", flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b"\r", b"\n"}:  # Enter pressed
            print()
            break
        elif ch == b"\x08":  # Backspace
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write("\b \b")
        elif ch == b"\x03":  # Ctrl+C
            raise KeyboardInterrupt
        else:
            try:
                char = ch.decode("utf-8")
            except UnicodeDecodeError:
                continue
            password += char
            sys.stdout.write("*")
    return password


# -----------------------------
# 🗂️ Database I/O
# -----------------------------
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("⚠️  Error reading vault database — creating a new one.")
        return {}


def save_db(data: dict):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# 🔒 Vault Operations
# -----------------------------
def add_entry(key_name, username, password, fernet):
    db = load_db()
    if key_name in db:
        overwrite = input("Entry exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != "y":
            print("❌ Cancelled.")
            return
    encrypted_secret = fernet.encrypt(password.encode()).decode()
    db[key_name] = {"username": username, "secret": encrypted_secret}
    save_db(db)
    print("✅ Entry saved.")


def get_entry(key_name, fernet):
    db = load_db()
    if key_name not in db:
        print("❌ No entry found for that key.")
        return
    entry = db[key_name]
    try:
        decrypted = fernet.decrypt(entry["secret"].encode()).decode()
        print(f"\n🔎 Key: {key_name}")
        print(f"👤 Username: {entry['username']}")
        print(f"🔑 Password: {decrypted}\n")
    except Exception:
        print("⚠️  Could not decrypt — wrong master password?")


def list_entries():
    db = load_db()
    if not db:
        print("📭 Vault is empty.")
        return
    print("\n🗝️ Stored Keys:")
    for k in db.keys():
        print(f" - {k}")
    print()


def delete_entry(key_name):
    db = load_db()
    if key_name not in db:
        print("❌ No entry found.")
        return
    confirm = input(f"Are you sure you want to delete '{key_name}'? (y/n): ").strip().lower()
    if confirm == "y":
        del db[key_name]
        save_db(db)
        print("🗑️  Entry deleted.")
    else:
        print("❌ Cancelled.")


# -----------------------------
# 🧭 Interactive Menu
# -----------------------------
def main():
    print("🔐 Secure Password Vault")
    try:
        master = input_password("Enter master password: ")
    except KeyboardInterrupt:
        print("\n❌ Cancelled.")
        return

    fernet = Fernet(derive_key(master))

    while True:
        print("""
=========================
1️⃣  Add new credential
2️⃣  Retrieve credential
3️⃣  List all keys
4️⃣  Delete credential
5️⃣  Exit
=========================
""")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            key = input("Enter key name (e.g., gmail, github): ").strip()
            user = input("Username: ").strip()
            secret = input_password("Password: ")
            add_entry(key, user, secret, fernet)

        elif choice == "2":
            key = input("Enter key name to retrieve: ").strip()
            get_entry(key, fernet)

        elif choice == "3":
            list_entries()

        elif choice == "4":
            key = input("Enter key name to delete: ").strip()
            delete_entry(key)

        elif choice == "5":
            print("👋 Exiting vault. Stay secure!")
            break

        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    main()
