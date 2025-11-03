import os
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("🔑 Key generated and saved as secret.key")

def load_key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        print("Error: 'secret.key' not found. Please generate a key first (option 1).")
        exit()

def encrypt_file(filename):
    key = load_key()
    fernet = Fernet(key)

    with open(filename, "rb") as file:
        data = file.read()

    encrypted = fernet.encrypt(data)
    with open(filename + ".enc", "wb") as file:
        file.write(encrypted)
    print(f"✅ File '{filename}' encrypted successfully!")

def decrypt_file(filename):
    key = load_key()
    fernet = Fernet(key)

    with open(filename, "rb") as file:
        data = file.read()

    decrypted = fernet.decrypt(data)
    original_name = filename.replace(".enc", "_decrypted.txt")
    with open(original_name, "wb") as file:
        file.write(decrypted)
    print(f"🔓 File decrypted successfully as '{original_name}'")

if __name__ == "__main__":
    print("🔒 File Encryption & Decryption Tool 🔒")
    print("1 Generate Key\n2 Encrypt File\n3 Decrypt File")
    choice = input("Choose an option: ")

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if choice == "1":
        generate_key()
    elif choice == "2":
        fname = input("Enter filename to encrypt: ")
        # Convert to absolute path if not already
        if not os.path.isabs(fname):
            fname = os.path.join(script_dir, fname)
        if not os.path.exists(fname):
            print(f"Error: File not found: {fname}")
            exit()
        encrypt_file(fname)
    elif choice == "3":
        fname = input("Enter filename to decrypt: ")
        # Convert to absolute path if not already
        if not os.path.isabs(fname):
            fname = os.path.join(script_dir, fname)
        if not os.path.exists(fname):
            print(f"Error: File not found: {fname}")
            exit()
        decrypt_file(fname)
