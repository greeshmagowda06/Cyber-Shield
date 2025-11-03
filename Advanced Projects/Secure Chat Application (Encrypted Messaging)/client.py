"""
Secure chat client:
 - Connects to server, receives server public RSA key
 - Generates a Fernet symmetric key, encrypts it with server RSA pubkey and sends it
 - Then sends/receives encrypted messages using Fernet
"""

import socket
import time
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet
SERVER = "127.0.0.1"
PORT = 5000


def recv_all(sock, n):
    data = b""
    while len(data) < n:
        part = sock.recv(n - len(data))
        if not part:
            return None
        data += part
    return data


def client_run(auto=False, messages=None, delay=0.5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER, PORT))
        pub_pem = b""
        while True:
            part = s.recv(1024)
            if not part:
                break
            pub_pem += part
            if b"-----END PUBLIC KEY-----" in pub_pem:
                break

        server_pub = serialization.load_pem_public_key(pub_pem)

        sym_key = Fernet.generate_key()
        enc_key = server_pub.encrypt(
            sym_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        s.sendall(len(enc_key).to_bytes(4, "big") + enc_key)

        f = Fernet(sym_key)
        print("Secure channel established. Type 'exit' to quit.")

        if auto:
            for msg in messages or ["hello", "exit"]:
                enc = f.encrypt(msg.encode())
                s.sendall(len(enc).to_bytes(4, "big") + enc)
                # receive server reply
                len_bytes = recv_all(s, 4)
                if not len_bytes:
                    break
                reply_len = int.from_bytes(len_bytes, "big")
                enc_reply = recv_all(s, reply_len)
                if not enc_reply:
                    break
                reply = f.decrypt(enc_reply).decode()
                print("Server:", reply)
                time.sleep(delay)
                if msg.strip().lower() == "exit":
                    break
        else:
            while True:
                msg = input("You: ")
                enc = f.encrypt(msg.encode())
                s.sendall(len(enc).to_bytes(4, "big") + enc)

                # receive server reply
                len_bytes = recv_all(s, 4)
                if not len_bytes:
                    break
                reply_len = int.from_bytes(len_bytes, "big")
                enc_reply = recv_all(s, reply_len)
                if not enc_reply:
                    break
                reply = f.decrypt(enc_reply).decode()
                print("Server:", reply)
                if msg.strip().lower() == "exit":
                    break


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Secure chat client")
    parser.add_argument("--auto", action="store_true", help="Run non-interactively; send messages and exit")
    parser.add_argument("--messages", help="Comma-separated messages to send in auto mode (default: hello,exit)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between auto messages in seconds")
    args = parser.parse_args()

    msgs = None
    if args.messages:
        msgs = [m for m in args.messages.split(",")]

    client_run(auto=args.auto, messages=msgs, delay=args.delay)
