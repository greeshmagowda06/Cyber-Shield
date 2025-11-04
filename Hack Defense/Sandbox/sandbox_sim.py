# sandbox/sandbox_sim.py
import time, threading, os

def simulate_activity(path="sandbox_files"):
    os.makedirs(path, exist_ok=True)
    # create many files quickly (simulate rapid file writes)
    for i in range(50):
        with open(os.path.join(path,f"temp{i}.txt"),"w") as f:
            f.write("x"*1000)
        time.sleep(0.05)
    print("Simulation done")

if __name__=="__main__":
    simulate_activity()
