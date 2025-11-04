# ARP Discovery — Conceptual Notes

**Goal:** Identify live hosts on the same Ethernet/LAN segment.

**Protocol:** ARP (Address Resolution Protocol)
- ARP "who-has" queries ask "who has IP X?" and a host owning IP X replies with "is-at" including its MAC.
- Works only on the same broadcast domain / local segment (not routed).

**Important safety & ethics:** Do not perform ARP sweeps on networks you don't own/authorize.

**Note:** This repo uses a simulated ARP (JSON-based). Real ARP scanning requires specialized libraries and authorization.
