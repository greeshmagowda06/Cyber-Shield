#!/usr/bin/env python3
"""
mock_scanner.py

A safe simulation of an ARP discovery + TCP SYN port check tool.

This script DOES NOT send any network packets. It reads a local JSON file (sample_network.json)
and simulates ARP replies and SYN responses to demonstrate program flow, output, and reporting.
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Tuple

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sample_network.json")


def load_sample_network(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)


def simulate_arp_discovery(subnet: str, sample_data: Dict) -> List[Tuple[str, str]]:
    """
    Simulate ARP discovery by returning IP/MAC tuples from sample data that fall into the subnet.
    This is a pure simulation: no network activity occurs.
    """
    # For the mock, we trust the sample file's subnet and return all hosts.
    hosts = []
    for h in sample_data.get("hosts", []):
        hosts.append((h["ip"], h["mac"]))
    return hosts


def simulate_port_scan(host_ip: str, ports: List[int], sample_data: Dict) -> Dict[int, str]:
    """
    Simulate checking ports on host_ip by comparing to sample_data "open_ports".
    Returns a mapping port -> state ("open" / "closed").
    """
    # Find host entry
    host_entry = next((h for h in sample_data.get("hosts", []) if h["ip"] == host_ip), None)
    open_ports = set(host_entry.get("open_ports", [])) if host_entry else set()
    result = {}
    for p in ports:
        result[p] = "open" if p in open_ports else "closed"
    return result


def pretty_print_discovery(active_hosts: List[Tuple[str, str]]) -> None:
    print("Discovered hosts (simulated):")
    print("----------------------------")
    for ip, mac in active_hosts:
        print(f"{ip:<16} {mac}")
    print()


def pretty_print_port_results(host_ip: str, port_results: Dict[int, str]) -> None:
    print(f"Port scan results for {host_ip} (simulated):")
    print("--------------------------------------------")
    for port in sorted(port_results):
        state = port_results[port]
        print(f"  {port:<6} {state}")
    print()


def parse_ports(ports_str: str) -> List[int]:
    if not ports_str:
        return [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 3389]
    parts = ports_str.split(",")
    out = []
    for p in parts:
        p = p.strip()
        if "-" in p:
            a, b = p.split("-", 1)
            out.extend(list(range(int(a), int(b) + 1)))
        else:
            out.append(int(p))
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Mock Recon Scanner (safe simulation)")
    parser.add_argument("--target", "-t", required=False, default="192.168.1.0/24",
                        help="Target subnet (simulated)")
    parser.add_argument("--ports", "-p", required=False,
                        help="Comma-separated list of ports or ranges (e.g. 22,80,8000-8010). If omitted a default set is used.")
    parser.add_argument("--data-file", "-d", required=False, default=DATA_FILE,
                        help="Path to sample network JSON (for simulation)")
    args = parser.parse_args(argv)

    # load sample network
    try:
        sample = load_sample_network(os.path.abspath(args.data_file))
    except FileNotFoundError:
        print("Sample data file not found. Please ensure data/sample_network.json exists.", file=sys.stderr)
        sys.exit(2)

    ports = parse_ports(args.ports) if args.ports else parse_ports(None)

    # Simulate ARP discovery
    active_hosts = simulate_arp_discovery(args.target, sample)
    pretty_print_discovery(active_hosts)

    # Simulate port scanning each host
    final_report = {}
    for ip, mac in active_hosts:
        res = simulate_port_scan(ip, ports, sample)
        pretty_print_port_results(ip, res)
        final_report[ip] = {
            "mac": mac,
            "ports": res
        }

    # Save simulated report to JSON for use in README / screenshot demonstration
    out_path = os.path.join(os.path.dirname(__file__), "..", "simulated_report.json")
    with open(out_path, "w") as f:
        json.dump(final_report, f, indent=2)
    print(f"Simulation complete. Report saved to: {out_path}\n")


if __name__ == "__main__":
    main()
