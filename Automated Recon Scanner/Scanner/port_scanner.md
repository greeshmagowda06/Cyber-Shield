# Port Scanning (TCP SYN) — Conceptual Notes

**Goal:** Determine whether target TCP ports are open, closed, or filtered.

**Method (SYN scan):**
- Send a TCP packet with the SYN flag to the target port.
- Responses:
  - SYN-ACK → port likely OPEN (standard practice is to send RST to avoid completing handshake).
  - RST → port CLOSED.
  - No response / ICMP unreachable / TTL exceeded → FILTERED or dropped.

**Important safety & ethics:** Port scanning can be intrusive. Always obtain explicit permission and constrain scans to limited ports and rate-limits in real deployments.

**Note:** This repo contains a simulated port scanner only.
