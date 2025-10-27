from scapy.all import sniff

def packet_callback(packet):
    print(f"📦 Packet: {packet.summary()}")

print("🌍 Network Packet Sniffer (Press Ctrl+C to stop)")
sniff(prn=packet_callback, count=10)
