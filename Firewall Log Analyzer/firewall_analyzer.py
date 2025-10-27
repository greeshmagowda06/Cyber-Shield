def analyze_logs(file_path):
    suspicious_count = 0
    total_lines = 0

    with open(file_path, "r") as file:
        for line in file:
            total_lines += 1
            if "DENY" in line or "BLOCK" in line or "FAILED" in line:
                suspicious_count += 1
                print("⚠️ Suspicious Entry:", line.strip())

    print(f"\nTotal entries: {total_lines}")
    print(f"Suspicious entries: {suspicious_count}")

if __name__ == "__main__":
    print("Firewall Log Analyzer")
    log_file = input("Enter log file path (e.g., sample_log.txt): ")
    analyze_logs(log_file)
