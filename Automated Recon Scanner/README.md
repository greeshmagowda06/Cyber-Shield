<!-- Automated_Recon_Scanner_Python (Simulated) -->

Status: Educational simulation only — NO network packets are sent.

## Purpose
This repository demonstrates the workflow of a reconnaissance tool (host discovery + port checking) 

Safely by simulating network responses. Use this for learning, UI/UX development, and documentation without scanning real networks.

## Contents
- `scanner/mock_scanner.py` — safe, simulated scanner (reads `data/sample_network.json`).
- `data/sample_network.json` — sample hosts and open ports used for simulation.
- `scanner/arp_discovery.md` & `scanner/port_scanner.md` — conceptual protocol explanations.
- `tests/` — unit tests for the simulator.
- `screenshots/` — add your simulated run screenshot here for proof in the README.
- `README.md` — this file.

<!-- Quick start -->
1. Clone the repo.
2. (Optional) create and activate a virtualenv.
3. Install test dependency for unit tests:
