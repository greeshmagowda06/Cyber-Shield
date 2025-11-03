"""
Advanced Educational IDS:
 - Rule-based detections (port-scan, high-SYN rate)
 - Unsupervised anomaly detection using IsolationForest
 - Logging alerts to CSV
USAGE: sudo python ids_advanced.py
"""

import time
import threading
from collections import defaultdict, deque
from scapy.all import sniff, IP, TCP
from sklearn.ensemble import IsolationForest
import numpy as np
import csv
import os

# ---- Config ----
WINDOW = 10                     # sliding window in seconds
PORT_SCAN_THRESHOLD = 15        # distinct dest ports within WINDOW
SYN_RATE_THRESHOLD = 30         # SYN packets within WINDOW
TRAINING_INTERVAL = 60          # seconds to collect normal data before training
MODEL_PERSIST = "if_model.pkl"  # not implemented persistence, placeholder
ALERT_CSV = "ids_alerts.csv"

# ---- State ----
recent_events = defaultdict(lambda: deque())   # src_ip -> deque of (timestamp, dst_port, pkt_len, is_syn)
feature_history = []  # store feature vectors for training
model = None

# ---- Helpers ----
def extract_features_for_ip(src):
    """
    builds feature vector for src based on events in WINDOW:
    [distinct_ports_count, syn_count, total_packets, avg_pkt_len]
    """
    now = time.time()
    dq = recent_events[src]
    # prune old
    while dq and now - dq[0][0] > WINDOW:
        dq.popleft()
    if not dq:
        return np.array([0,0,0,0], dtype=float)

    ports = {p for (_, p, _, _) in dq}
    syn_count = sum(1 for (_, _, _, is_syn) in dq if is_syn)
    total = len(dq)
    avg_len = np.mean([l for (_, _, l, _) in dq]) if total > 0 else 0.0
    return np.array([len(ports), syn_count, total, avg_len], dtype=float)

def log_alert(src, score, reason):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    row = [timestamp, src, f"{score:.4f}", reason]
    write_header = not os.path.exists(ALERT_CSV)
    with open(ALERT_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp","src_ip","anomaly_score","reason"])
        writer.writerow(row)
    print(f"[ALERT] {timestamp} | {src} | score={score:.4f} | reason={reason}")

def train_model_from_history(history):
    """
    history: list of feature vectors (np.array)
    Returns trained IsolationForest
    """
    if len(history) < 20:
        return None
    X = np.vstack(history)
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(X)
    return model

# ---- Packet handler ----
def handle_packet(pkt):
    if IP in pkt and TCP in pkt:
        ip_layer = pkt[IP]
        tcp_layer = pkt[TCP]
        src = ip_layer.src
        dst_port = tcp_layer.dport
        pkt_len = len(pkt)
        flags = tcp_layer.flags
        is_syn = bool(flags & 0x02)

        now = time.time()
        recent_events[src].append((now, dst_port, pkt_len, is_syn))

        # Build features vector
        feat = extract_features_for_ip(src)

        # Collect training data until model exists
        global model
        if model is None:
            feature_history.append(feat)
        else:
            # predict anomaly
            score = model.decision_function([feat])[0]  # higher is more normal, lower is anomalous
            # Also compute rule-based reasons
            reasons = []
            if feat[0] >= PORT_SCAN_THRESHOLD:
                reasons.append(f"port_scan_distinct_ports={int(feat[0])}")
            if feat[1] >= SYN_RATE_THRESHOLD:
                reasons.append(f"high_syns={int(feat[1])}")
            # If model says anomalous or rule-based triggers
            if score < -0.2 or reasons:
                reason_text = ";".join(reasons) if reasons else "anomaly_model"
                # invert score so lower -> more suspicious; map to positive magnitude
                log_alert(src, -score, reason_text)

# ---- Background trainer ----
def background_trainer():
    global model, feature_history
    print("[TRAINER] Collecting baseline traffic for model...")
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed >= TRAINING_INTERVAL and model is None:
            print(f"[TRAINER] Training model on {len(feature_history)} samples...")
            model = train_model_from_history(feature_history)
            if model is None:
                print("[TRAINER] Not enough data to train, collecting more...")
                start = time.time()
            else:
                print("[TRAINER] Model trained. IDS active with ML detection.")
            # clear history to avoid memory bloat
            feature_history = []
        time.sleep(2)

# ---- Main ----
def main():
    # start trainer
    t = threading.Thread(target=background_trainer, daemon=True)
    t.start()
    print("=== Advanced IDS ===")
    print("Collecting baseline for", TRAINING_INTERVAL, "seconds. Run some normal traffic to train.")
    print("Sniffing on active interface. Press Ctrl+C to stop.")
    sniff(filter="tcp", prn=handle_packet, store=False)

if __name__ == "__main__":
    main()
