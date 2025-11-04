# sandbox/detector.py
import psutil, time, os
from collections import defaultdict

# simple heuristic: many file creates in short time in a folder
def monitor(path="sandbox_files"):
    observed = defaultdict(int)
    print("Monitoring folder for rapid creations...")
    prev = set(os.listdir(path)) if os.path.exists(path) else set()
    while True:
        time.sleep(1)
        cur = set(os.listdir(path))
        new = cur - prev
        if len(new) > 5:
            print("ALERT: rapid file creation:", len(new))
        prev = cur

if __name__=="__main__":
    os.makedirs("sandbox_files", exist_ok=True)
    monitor()
