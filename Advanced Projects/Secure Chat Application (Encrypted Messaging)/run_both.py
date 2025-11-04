# run_both.py
# Launches server.py and client.py as subprocesses (auto mode).
# Requires server.py and client.py in the same folder.
import subprocess, sys, time, os, signal

PY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))

def start_process(cmd, stdout=None, stderr=None):
    return subprocess.Popen(cmd, cwd=HERE, stdout=stdout, stderr=stderr, text=True)

def main():
    # Start server in auto mode (it will auto-reply)
    server_cmd = [PY, "server.py", "--auto"]
    server_proc = start_process(server_cmd)

    # Give server a moment to bind
    time.sleep(1.0)

    # Start client in auto mode with messages (customize below)
    # Example messages: hello,how are you,exit
    client_cmd = [PY, "client.py", "--auto", "--messages", "Hello,How are you?,exit"]
    client_proc = start_process(client_cmd)

    try:
        # Forward server/client output to this terminal
        while True:
            if server_proc.poll() is not None and client_proc.poll() is not None:
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Stopping processes...")
    finally:
        for p in (client_proc, server_proc):
            if p and p.poll() is None:
                try:
                    p.send_signal(signal.SIGINT)
                except Exception:
                    p.terminate()
        print("Done.")

if __name__ == "__main__":
    main()
