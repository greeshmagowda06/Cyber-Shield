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
    import argparse

    parser = argparse.ArgumentParser(description="Secure chat server")
    parser.add_argument("--auto", action="store_true", help="Automatically reply to client messages (non-interactive)")
    args = parser.parse_args()

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
            def recv_all(sock, n):
                data = b""
                while len(data) < n:
                    part = sock.recv(n - len(data))
                    if not part:
                        return None
                    data += part
                return data

            key_len_bytes = recv_all(conn, 4)
            if not key_len_bytes:
                return
            key_len = int.from_bytes(key_len_bytes, "big")
            enc_key = recv_all(conn, key_len)
            if enc_key is None:
                return

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
                len_bytes = recv_all(conn, 4)
                if not len_bytes:
                    break
                msg_len = int.from_bytes(len_bytes, "big")
                enc_msg = recv_all(conn, msg_len)
                if enc_msg is None:
                    break
                try:
                    msg = f.decrypt(enc_msg).decode()
                except Exception:
                    print("[!] Decryption failed")
                    break

                print("Client:", msg)
                if msg.strip().lower() == "exit":
                    break
                if args.auto:
                    # auto-reply with a simple echo
                    reply = f"Echo: {msg}"
                    print(f"Auto-reply: {reply}")
                else:
                    reply = input("You: ")
                enc_reply = f.encrypt(reply.encode())
                conn.sendall(len(enc_reply).to_bytes(4, "big") + enc_reply)
            print("Connection closed.")

if __name__ == "__main__":
    main()
