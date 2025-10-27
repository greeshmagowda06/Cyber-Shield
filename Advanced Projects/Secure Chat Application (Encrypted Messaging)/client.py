"""
Secure chat client:
 - Connects to server, receives server public RSA key
 - Generates a Fernet symmetric key, encrypts it with server RSA pubkey and sends it
 - Then sends/receives encrypted messages using Fernet
"""

import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

SERVER = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER, PORT))
        # receive server public key PEM
        pub_pem = b""
        while True:
            part = s.recv(1024)
            pub_pem += part
            # PEM ends with -----END PUBLIC KEY-----\n
            if b"-----END PUBLIC KEY-----" in pub_pem:
                break

        server_pub = serialization.load_pem_public_key(pub_pem)

        # generate symmetric key and encrypt it with server's public key
        sym_key = Fernet.generate_key()
        enc_key = server_pub.encrypt(
            sym_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        # send length prefix + encrypted key
        s.sendall(len(enc_key).to_bytes(4, "big") + enc_key)

        f = Fernet(sym_key)
        print("Secure channel established. Type 'exit' to quit.")
        while True:
            msg = input("You: ")
            enc = f.encrypt(msg.encode())
            s.sendall(len(enc).to_bytes(4, "big") + enc)

            # receive server reply
            len_bytes = s.recv(4)
            if not len_bytes:
                break
            reply_len = int.from_bytes(len_bytes, "big")
            enc_reply = s.recv(reply_len)
            reply = f.decrypt(enc_reply).decode()
            print("Server:", reply)
            if msg.strip().lower() == "exit":
                break

if __name__ == "__main__":
    main()
