import json
import os
from scanner import mock_scanner

BASE = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE, "data", "sample_network.json")


def test_load_sample_network():
    data = mock_scanner.load_sample_network(DATA_FILE)
    assert "hosts" in data
    assert isinstance(data["hosts"], list)


def test_simulate_arp_discovery():
    data = mock_scanner.load_sample_network(DATA_FILE)
    hosts = mock_scanner.simulate_arp_discovery("192.168.1.0/24", data)
    assert len(hosts) == len(data["hosts"])
    for ip, mac in hosts:
        assert isinstance(ip, str)
        assert isinstance(mac, str)


def test_simulate_port_scan_known_open():
    data = mock_scanner.load_sample_network(DATA_FILE)
    # host 192.168.1.10 has open ports 22 and 80 in sample file
    res = mock_scanner.simulate_port_scan("192.168.1.10", [22, 80, 443], data)
    assert res[22] == "open"
    assert res[80] == "open"
    assert res[443] == "closed"
