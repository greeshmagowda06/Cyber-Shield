import sys
import os
from datetime import datetime
try:
    from scapy.all import sniff, IP, TCP, UDP
except ImportError:
    print("Error: Scapy package is not installed.")
    print("Please install it using: pip install scapy")
    sys.exit(1)

def check_privileges():
    """Check if the script is running with administrator privileges."""
    try:
        return os.geteuid() == 0
    except AttributeError:  # Windows doesn't have geteuid
        try:
            return os.environ['ADMINISTRATOR'] == 'True'
        except KeyError:
            return False

def packet_callback(packet):
    """Process and display packet information."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Basic packet info
    summary = f"📦 [{timestamp}] "
    
    if IP in packet:
        summary += f"IP {packet[IP].src} → {packet[IP].dst}"
        
        if TCP in packet:
            summary += f" | TCP Port {packet[TCP].sport} → {packet[TCP].dport}"
            if packet[TCP].flags:
                summary += f" | Flags: {packet[TCP].flags}"
        elif UDP in packet:
            summary += f" | UDP Port {packet[UDP].sport} → {packet[UDP].dport}"
    else:
        summary += packet.summary()
    
    print(summary)

def start_sniffer(packet_count=None):
    """Start the packet sniffer with optional count limit."""
    try:
        if not check_privileges():
            print("\n⚠️ Warning: This script may require administrator privileges.")
            print("Some packet capture features might be limited.\n")
        
        print("🌍 Network Packet Sniffer")
        print("Press Ctrl+C to stop capturing packets...")
        print("\nStarting packet capture...")
        
        # Start sniffing
        sniff(prn=packet_callback, count=packet_count, store=0)
        
        print("\n✅ Packet capture finished.")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Capture stopped by user.")
    except Exception as e:
        print(f"\n❌ Error during packet capture: {str(e)}")
        print("Make sure you have the necessary permissions.")

if __name__ == "__main__":
    # Default to capturing 50 packets, can be modified as needed
    start_sniffer(packet_count=50)
