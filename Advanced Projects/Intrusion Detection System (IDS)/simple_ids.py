
from scapy.all import sniff, TCP, IP
from collections import defaultdict, deque
import sys
import time
import threading

# Config
PORT_SCAN_THRESHOLD = 10       
SYN_RATE_THRESHOLD = 20       
WINDOW = 10                   

# state
recent_ports = defaultdict(lambda: deque())  # src_ip -> deque of (timestamp, dst_port)
recent_syns = defaultdict(lambda: deque())   # src_ip -> deque of timestamps

def clean_old_entries():
    """Periodically prune old events"""
    now = time.time()
    for d in (recent_ports, recent_syns):
        for ip, dq in list(d.items()):
            while dq and (now - dq[0][0] if isinstance(dq[0], tuple) else now - dq[0]) > WINDOW:
                dq.popleft()

def handle_packet(pkt):
    if IP in pkt and TCP in pkt:
        ip_layer = pkt[IP]
        tcp_layer = pkt[TCP]
        src = ip_layer.src
        dst_port = tcp_layer.dport
        flags = tcp_layer.flags

        now = time.time()
        # Track ports per source
        recent_ports[src].append((now, dst_port))
        # Track SYNs
        if flags & 0x02:  # SYN flag
            recent_syns[src].append(now)

        # evaluate port-scan: count distinct ports in window
        ports_in_window = {p for (ts, p) in recent_ports[src] if now - ts <= WINDOW}
        syns_in_window = sum(1 for ts in recent_syns[src] if now - ts <= WINDOW)

        if len(ports_in_window) >= PORT_SCAN_THRESHOLD:
            print(f"[ALERT] Possible port scan from {src} -> {len(ports_in_window)} distinct ports in last {WINDOW}s")

        if syns_in_window >= SYN_RATE_THRESHOLD:
            print(f"[ALERT] High SYN rate from {src} -> {syns_in_window} SYNs in last {WINDOW}s")

def pruner():
    while True:
        clean_old_entries()
        time.sleep(1)

if __name__ == "__main__":
    print("=== Simple IDS (educational) ===")
    
    # Check for administrator privileges
    if sys.platform.startswith('win'):
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Error: This script requires administrator privileges to run on Windows.")
            print("Please run the script as an administrator.")
            sys.exit(1)

    print("Sniffing interface. Press Ctrl+C to stop. (Run as root/Administrator)")
    # start pruner thread
    t = threading.Thread(target=pruner, daemon=True)
    t.start()
    # sniff packets (prn=handle_packet). You can add filter like "tcp" to limit traffic.
    sniff(filter="tcp", prn=handle_packet, store=False)
