import psutil
import os
import time
from datetime import datetime

def check_suspicious_paths():
    """Check common paths where keyloggers might hide their files."""
    suspicious_paths = []
    common_locations = [
        os.path.expanduser("~\\AppData\\Local\\Temp"),
        os.path.expanduser("~\\AppData\\Roaming"),
        "C:\\Windows\\Temp",
        "C:\\Program Files",
        "C:\\Program Files (x86)"
    ]
    
    suspicious_extensions = [".log", ".txt", ".dat", ".key", ".keylog"]
    
    print("\nChecking suspicious file locations...")
    for location in common_locations:
        if not os.path.exists(location):
            continue
            
        try:
            for root, _, files in os.walk(location):
                for file in files:
                    if any(file.endswith(ext) for ext in suspicious_extensions):
                        try:
                            file_path = os.path.join(root, file)
                            # Check if file was modified recently (last 24 hours)
                            mtime = os.path.getmtime(file_path)
                            if time.time() - mtime < 86400:  # 24 hours in seconds
                                suspicious_paths.append({
                                    'path': file_path,
                                    'modified': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                                })
                        except (PermissionError, OSError):
                            continue
        except (PermissionError, OSError):
            continue
    
    return suspicious_paths

def detect_keyloggers():
    """Detect potential keylogger processes and suspicious files."""
    # Common keywords found in keylogger process names or descriptions
    keylogger_keywords = [
        "keylogger", "hook", "keyboard", "logger", "spy", "monitor", "capture",
        "input", "record", "track", "type", "keys", "intercept", "listen"
    ]
    suspicious_processes = []
    total_processes = 0

    print("\n🔍 Scanning running processes for keylogger-like activity...")

    for process in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'username']):
        total_processes += 1
        try:
            process_info = process.info
            name = str(process_info.get('name', '')).lower()
            exe_path = str(process_info.get('exe', '')).lower()
            cmdline = process_info.get('cmdline', [])
            cmdline_str = ' '.join(str(cmd) for cmd in cmdline).lower() if cmdline else ''
            username = process_info.get('username')

            # Skip system processes
            if username and ('system' in username.lower() or 'local service' in username.lower()):
                continue

            # Check if any keyword is present in the process details
            if any(keyword in name or keyword in exe_path or keyword in cmdline_str 
                  for keyword in keylogger_keywords):
                suspicious_processes.append({
                    'pid': process_info['pid'],
                    'name': process_info['name'],
                    'exe': process_info.get('exe', 'Unknown'),
                    'cmdline': process_info.get('cmdline', []),
                    'username': username
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Check for suspicious files
    suspicious_files = check_suspicious_paths()
    
    print(f"\n📊 Scan Results:")
    print(f"Total processes scanned: {total_processes}")
    
    if suspicious_processes:
        print("\n⚠️ Suspicious processes detected:")
        for proc in suspicious_processes:
            print(f"\nPID: {proc['pid']}")
            print(f"Name: {proc['name']}")
            print(f"Executable: {proc['exe']}")
            print(f"Command line: {' '.join(proc['cmdline'])}")
            print(f"User: {proc['username']}")
    else:
        print("\n✅ No suspicious processes detected")
    
    if suspicious_files:
        print("\n⚠️ Suspicious files detected:")
        for file in suspicious_files:
            print(f"\nPath: {file['path']}")
            print(f"Last modified: {file['modified']}")
    else:
        print("\n✅ No suspicious files detected")
    
    print("\n🛡️ Scan complete!")

if __name__ == "__main__":
    print("🔍 Keylogger Detector")
    print("=====================")
    detect_keyloggers()
