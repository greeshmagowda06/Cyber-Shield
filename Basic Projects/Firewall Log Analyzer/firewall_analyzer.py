import os
def analyze_logs(sample_log):
    suspicious_count = 0
    total_lines = 0
    try:
        with open(sample_log, "r", encoding="utf-8") as file:
            for line in file:
                total_lines += 1
                if "DENY" in line or "BLOCK" in line or "FAILED" in line:
                    suspicious_count += 1
                    print("⚠️ Suspicious Entry:", line.strip())
    except FileNotFoundError:
        print(f"Error: log file not found: {sample_log}")
        return
    except PermissionError:
        print(f"Error: permission denied when opening: {sample_log}")
        return

    print(f"\nTotal entries: {total_lines}")
    print(f"Suspicious entries: {suspicious_count}")

if __name__ == "__main__":
    print("Firewall Log Analyzer")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_log = os.path.join(script_dir, "sample_log.txt")

    user_input = input(f"Enter log file path (press Enter to use default: {default_log}): ").strip()
    log_file = user_input if user_input else default_log

    analyze_logs(log_file)
