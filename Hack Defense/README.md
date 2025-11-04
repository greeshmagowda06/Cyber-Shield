## A collection of 8 cybersecurity projects ranging from encryption and digital forensics to AI-based threat detection.

`Password Vault (Encrypted Credential Manager)` vault.py
Securely stores usernames and passwords by encrypting them with a master key, protecting sensitive credentials from unauthorized access.

`Steganography Image Encoder/Decoder` stego.py
Hides secret text messages inside image pixels using Least Significant Bit (LSB) encoding, ensuring covert data communication.
Usage:
- Encode: python stego.py encode in.png out.png "hello"
- Decode: python stego.py decode out.png

`Blockchain-Based File Integrity Verifier` chain.py
Uses blockchain principles to record file hashes, ensuring that any tampering or modification of files can be easily detected.

`AI-Powered Phishing Email Classifier` train_and_predict.py
Applies machine learning to analyze and classify emails as phishing or legitimate based on textual patterns and features.
Usage:
- Train & save: python train_and_predict.py
- Predict: python train_and_predict.py predict "Please update password"

`AI Network Intrusion Detector` detector.py
Detects abnormal network activity and potential cyber attacks using machine learning models trained on network traffic data.

`Digital Forensics Analyzer` forensic_scan.py
Extracts metadata and timestamps from files and folders to assist in digital investigations and evidence collection.

`Keylogger & Malware Behavior Sandbox (Safe Simulation)` sandbox_sim.py & detector.py
Simulates malware-like behaviors in a controlled environment and detects them using heuristic analysis — without causing harm.
Note: Run sandbox_sim.py in one terminal, detector.py in another.

`Dark Web Crawler (Safe Version)` tor_crawler.py
Safely connects through the Tor network to collect metadata from .onion websites for research and cyber threat intelligence.
Note: Do not crawl or access illegal content. Use .onion addresses only for research or controlled targets.