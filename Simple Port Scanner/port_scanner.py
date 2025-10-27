import socket

def scan_ports(target, ports=[21, 22, 80, 443, 8080]):
    print(f"\n🔍 Scanning target: {target}")
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"✅ Port {port} is OPEN")
        else:
            print(f"❌ Port {port} is CLOSED")
        s.close()

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    scan_ports(target_ip)
