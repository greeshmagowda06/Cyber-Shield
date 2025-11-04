<!-- Intrusion Detection System (IDS) -->

I’ll implement a practical, deeper IDS here that combines rule-based detection and a simple ML anomaly detector (IsolationForest). It will:
- sniff TCP packets (requires root/admin) and extract features per source IP per time window,
- compute features: number of distinct dest ports, SYN count, total packets, avg packet size,
- feed feature vectors into an IsolationForest to score anomalies (unsupervised),
- raise alerts with reasons, and log events to a CSV.

Dependencies
- scapy (pip install scapy)
- scikit-learn (pip install scikit-learn)
- pandas (pip install pandas) — optional for CSV handling
- Run as root/Administrator because packet sniffing needs privileges.

`How this IDS works (summary)`

- Baseline collection: collects feature vectors for TRAINING_INTERVAL seconds and trains an IsolationForest unsupervised model to recognize "normal" traffic patterns.
- Features per source IP: number of distinct destination ports, SYN count, total packets, average packet length (windowed).
- Detection: uses ML score (IsolationForest) and rule-based thresholds (port-scan and SYN rate). Alerts are logged to CSV.
- Why this is useful: combining rules + unsupervised model reduces false positives and can detect unknown anomalous behaviours.

`How to test safely (recommended)`

1. Run sudo python ids_advanced.py. Let baseline collect (~60s).
2. Generate normal traffic: browse web, ping remote, run curl requests.
3. Generate controlled anomalies (on same LAN/local machine):
    - Port scan: nmap -p 1-200 localhost (or use nc to hit many ports).
    - SYN flood/emulation: tools exist but be careful — instead, write a small script that opens many TCP connections to different ports on localhost.
4. Watch console alerts and ids_alerts.csv.

`Improvements you can add next`

- Persist and periodically retrain model; weekly baseline updates.
- More features: inter-packet arrival time, packet direction ratios, payload entropy.
- Replace IsolationForest with autoencoder (deep learning) for richer patterns.
- Add web dashboard (Flask + charts) for alerts, top talkers, timeline.
- Integrate with syslog / SIEM or email push alerts.

<!-- Ethics & Legal reminder -->

Only run scanning/sniffing/active tests on systems/networks you own or have explicit permission to test. Misuse of these tools may be illegal.