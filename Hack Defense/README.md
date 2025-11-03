`Password Vault (Encrypted Credential Manager)`
- Goal: securely store/retrieve credentials locally.
Must-haves
- AES-GCM or cryptography.Fernet for encryption
- Master password → PBKDF2/HKDF to derive key
- CRUD CLI (add/get/delete/list)
- Encrypted file storage (JSON or SQLite)
Stretch
- GUI (Tkinter), auto-lock timeout, clipboard auto-clear
Deps: cryptography
Tests: encrypt->decrypt roundtrip, wrong master password denies access
Deliverable: vault.py, README, sample encrypted DB

`Steganography Image Encoder/Decoder`
- Goal: hide/retrieve text messages inside images (LSB).
Must-haves
- LSB encode/decode for PNG
- Option to encrypt message before embedding (use vault key)
- CLI: embed/extract
Stretch
- Support for audio/wav, stego-detection simple check
Deps: Pillow
Tests: embed -> extract equals original; image quality diff small
Deliverable: stego.py, examples, brief visual before/after

`Blockchain-Based File Integrity Verifier`
- Goal: tamper-evident audit chain of file hashes.
Must-haves
- Hash files (SHA256), chain as blocks (prev_hash + timestamp + filename)
- Simple Flask UI to register/verify files (optional)
- Export/import chain, verify integrity routine
Stretch
- Use lightweight blockchain lib or store chain on IPFS (optional research)
Deps: Flask (optional)
Tests: tamper file → verify fails; chain rebuild verifies history
Deliverable: chain.py, verify.py, sample chain

`AI-Powered Phishing Email Classifier`
- Goal: classify emails as phishing or benign.
Must-haves
- Dataset preprocessing (headers, subject, body, URL tokens)
- Train/test split, baseline model (Logistic Regression or RandomForest)
- Evaluation: precision/recall, confusion matrix
Stretch
- LSTM or transformer fine-tune for text, explainability (SHAP)
Deps: scikit-learn, pandas, nltk or spacy
Datasets: Enron + public phishing corpora (use only publicly available)
Tests: cross-validation, sample email predictions
Deliverable: Jupyter notebook with training + predict.py

`AI Network Intrusion Detector`
- Goal: detect malicious flows using ML (supervised or unsupervised).
Must-haves
- Use NSL-KDD or CIC datasets
- Feature engineering (flow stats, flags, packet size)
- Baseline: RandomForest / IsolationForest for anomalies
- Metrics: ROC, precision/recall
Stretch
- Deep models, real-time stream processing, dashboard
Deps: scikit-learn, pandas, (optional tensorflow)
Tests: train/test on dataset, simulate local attack and evaluate
Deliverable: notebook + detector.py that scores CSV flows

`Digital Forensics Analyzer`
- Goal: extract forensic artifacts & metadata from files/devices.
Must-haves
- EXIF extraction for images, file timeline parsing (mtime/ctime)
- Bulk scan folder and produce CSV report
- Simple timeline visualization (matplotlib)
Stretch
- Parse Windows Prefetch, NTFS $MFT (advanced), or browser history
Deps: exifread, pandas, pytsk3 (advanced)
Tests: known test files with metadata → extracted correctly
Deliverable: forensic_scan.py, sample report

`Keylogger & Malware Behavior Sandbox (Safe Simulation)`
- Goal: simulate suspicious behaviors and detect them (non-malicious).
Must-haves
- Simulate file modifications, registry-like persistence files, high-frequency keyboard events (simulation)
- Detector using heuristics and process monitoring (psutil)
- Logging & alerting
Stretch
- YARA-like pattern matching for file names, integrate with VM snapshot (advanced)
Deps: psutil
Tests: run simulations and ensure detector flags behaviors, low false positives
Deliverable: sandbox_sim.py, detector.py, sample logs

`Dark Web Crawler (Safe Version)`
- Goal: research-only crawler for onion metadata (must use Tor safely).
Must-haves
- Use stem to control Tor or route requests via Tor SOCKS proxy
- Collect metadata only (title, response code, links) — no scraping of illegal content
- Respect ethics and law; require explicit confirmation before run
Stretch
- Aggregate stats, graph connectivity, anonymized dataset
Deps: requests[socks], stem
Tests: run against known benign .onion research nodes (or local Tor hidden service)
Deliverable: tor_crawler.py, research notes, caution doc