"""
Secure chat server:
 - Generates RSA keypair
 - Accepts a connection, sends public key
 - Receives encrypted symmetric key (Fernet), decrypts with RSA private key
 - Uses Fernet to decrypt incoming messages and send encrypted replies
"""

import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

HOST = "0.0.0.0"
PORT = 5000

def generate_rsa_keys():
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = priv.public_key()
    return priv, pub

def main():
    priv, pub = generate_rsa_keys()
    pub_pem = pub.public_bytes(encoding=serialization.Encoding.PEM,
                               format=serialization.PublicFormat.SubjectPublicKeyInfo)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            # send public key
            conn.sendall(pub_pem)

            # receive encrypted symmetric key length + data
            key_len_bytes = conn.recv(4)
            if not key_len_bytes:
                return
            key_len = int.from_bytes(key_len_bytes, "big")
            enc_key = conn.recv(key_len)

            # decrypt symmetric key
            sym_key = priv.decrypt(
                enc_key,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                             algorithm=hashes.SHA256(),
                             label=None)
            )

            f = Fernet(sym_key)
            print("Secure channel established. Type 'exit' to quit.")
            while True:
                # receive encrypted message length + payload
                len_bytes = conn.recv(4)
                if not len_bytes:
                    break
                msg_len = int.from_bytes(len_bytes, "big")
                enc_msg = conn.recv(msg_len)
                try:
                    msg = f.decrypt(enc_msg).decode()
                except Exception:
                    print("[!] Decryption failed")
                    break

                print("Client:", msg)
                if msg.strip().lower() == "exit":
                    break
                reply = input("You: ")
                enc_reply = f.encrypt(reply.encode())
                conn.sendall(len(enc_reply).to_bytes(4, "big") + enc_reply)
            print("Connection closed.")

if __name__ == "__main__":
    main()
