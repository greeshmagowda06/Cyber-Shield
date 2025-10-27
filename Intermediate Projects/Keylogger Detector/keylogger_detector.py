import psutil

def detect_keyloggers():
    keylogger_keywords = ["keylogger", "hook", "keyboard", "logger"]
    suspicious = []

    for process in psutil.process_iter(['pid', 'name']):
        name = process.info['name']
        if any(keyword in name.lower() for keyword in keylogger_keywords):
            suspicious.append(name)

    if suspicious:
        print("⚠️ Suspicious keylogger-like processes found:")
        for name in suspicious:
            print(f" - {name}")
    else:
        print("✅ No keylogger processes detected.")

if __name__ == "__main__":
    print("Keylogger Detector")
    detect_keyloggers()
