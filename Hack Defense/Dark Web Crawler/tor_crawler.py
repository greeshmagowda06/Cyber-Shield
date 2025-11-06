#!/usr/bin/env python3
"""
tor_crawler.py — Safe, interactive .onion metadata crawler (research use only)

What it does:
 - Connects via Tor (SOCKS5 proxy at 127.0.0.1:9050)
 - Performs HEAD (then a tiny GET for title/snippet if allowed) to collect metadata:
   status_code, response_time, server header, content-type, small snippet or <title>
 - Rate-limits requests, logs results to CSV
 - Interactive menu to add targets, test Tor connection, crawl, view saved results

Important safety & setup notes:
 - You MUST run Tor locally (tor service) before using this. Typical SOCKS5 proxy:
     localhost:9050
 - Install deps: pip install requests pysocks pandas
 - ONLY probe .onion hosts you are permitted to research. Avoid illegal material.
"""

import requests
import socks  # PySocks backend used by requests via requests' socks support
import re
import time
import csv
import os
from datetime import datetime
import sys

# Configuration
TOR_SOCKS_PROXY = "socks5h://127.0.0.1:9150"  # socks5h forces remote DNS resolution through Tor
PROXIES = {"http": TOR_SOCKS_PROXY, "https": TOR_SOCKS_PROXY}
USER_AGENT = "SafeOnionCrawler/1.0 (+research)"
RATE_LIMIT_SECONDS = 5  # minimum seconds between requests
RESULTS_CSV = "onion_results.csv"
MAX_BYTES_TO_READ = 2048  # only read up to this number of bytes from response body

ONION_RE = re.compile(r"^[a-z2-7]{16,56}\.onion$", re.IGNORECASE)  # v2 (16) & v3 (56) compatible-ish


# ----------------------
# Utility functions
# ----------------------
def valid_onion(host: str) -> bool:
    host = host.strip().lower()
    return bool(ONION_RE.match(host))


def safe_snippet_from_body(content_bytes: bytes) -> str:
    """Return a short safe-text snippet from bytes, strip binary and limit length."""
    try:
        text = content_bytes.decode("utf-8", errors="ignore")
    except Exception:
        text = content_bytes.decode("latin-1", errors="ignore")
    # extract <title> if present
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        return title[:250]
    # fallback: return first non-empty line snippet
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return (lines[0][:250] if lines else "") if lines else ""


def ensure_tor_proxy_available(timeout=5) -> bool:
    """Quick test that the Tor proxy is reachable by requesting httpbin.org/ip through it."""
    test_url = "http://httpbin.org/ip"
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(test_url, proxies=PROXIES, headers=headers, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False


def append_result(row: dict):
    header = ["timestamp", "onion", "status_code", "response_time_s", "server", "content_type", "snippet"]
    exists = os.path.exists(RESULTS_CSV)
    with open(RESULTS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


# ----------------------
# Core crawler logic
# ----------------------
def fetch_metadata(onion: str, timeout=30) -> dict:
    """
    Fetch lightweight metadata for an .onion host.
    - Uses HEAD first for headers
    - If content-type is text/html, performs a tiny GET (stream) and reads up to MAX_BYTES_TO_READ
    Returns a dict of metadata (or raises).
    """
    url = f"http://{onion}/"  # many hidden services respond on http - user should provide schemeless
    headers = {"User-Agent": USER_AGENT}
    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "onion": onion,
        "status_code": None,
        "response_time_s": None,
        "server": "",
        "content_type": "",
        "snippet": "",
    }

    # Perform HEAD
    start = time.time()
    try:
        head = requests.head(url, headers=headers, proxies=PROXIES, timeout=timeout, allow_redirects=True)
        latency = time.time() - start
        result["status_code"] = head.status_code
        result["response_time_s"] = round(latency, 3)
        result["server"] = head.headers.get("Server", "")
        result["content_type"] = head.headers.get("Content-Type", "")
    except requests.RequestException as e:
        # Could be timeout, connection refused, ProxyError etc.
        raise RuntimeError(f"HEAD request failed: {e}")

    # If HTML-like, fetch a small chunk to extract title/snippet
    ct = result["content_type"].lower()
    if "html" in ct or ct == "" or "text" in ct:
        try:
            start = time.time()
            r = requests.get(url, headers=headers, proxies=PROXIES, timeout=timeout, stream=True, allow_redirects=True)
            latency = time.time() - start
            # update status/time if different
            result["status_code"] = r.status_code
            result["response_time_s"] = round(latency, 3)
            result["server"] = result["server"] or r.headers.get("Server", "")
            result["content_type"] = result["content_type"] or r.headers.get("Content-Type", "")

            # read a small amount only and close
            content_bytes = b""
            try:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        content_bytes += chunk
                    if len(content_bytes) >= MAX_BYTES_TO_READ:
                        break
            finally:
                r.close()
            result["snippet"] = safe_snippet_from_body(content_bytes)
        except requests.RequestException:
            # ignore snippet fetch errors but keep header info
            pass

    return result


# ----------------------
# Interactive UI
# ----------------------
def menu():
    targets = []
    last_request_time = 0.0

    print("=== Safe .onion metadata crawler ===")
    print("WARNING: Use only for lawful research and on addresses you control or are authorized to test.")
    confirm = input("Do you confirm you will not access illegal content? (y/n): ").strip().lower()
    if confirm != "y":
        print("Aborting. You must confirm lawful use.")
        return

    # quick check Tor proxy
    print("\nChecking local Tor SOCKS5 proxy (127.0.0.1:9050)...")
    if not ensure_tor_proxy_available():
        print("⚠️ Tor proxy check failed. Make sure Tor is running locally and listening on 127.0.0.1:9050.")
        print("Example: start tor (system service) or 'tor' on terminal. Aborting.")
        return
    print("✅ Tor proxy reachable.\n")

    while True:
        print("\nMenu:")
        print("1. Add .onion target")
        print("2. List current targets")
        print("3. Crawl a target now (one-by-one)")
        print("4. Crawl all targets (rate-limited)")
        print("5. View results file (print head)")
        print("6. Exit")
        choice = input("Select option (1-6): ").strip()

        if choice == "1":
            v = input("Enter .onion host (example: abcdefghijklmnop.onion or v3...onion): ").strip().lower()
            if not valid_onion(v):
                print("❌ Not a valid-looking .onion hostname. Make sure you entered only host (no scheme).")
            else:
                if v not in targets:
                    targets.append(v)
                    print(f"Added {v}")
                else:
                    print("Already in list.")

        elif choice == "2":
            if not targets:
                print("No targets added yet.")
            else:
                print("Targets:")
                for i, t in enumerate(targets, 1):
                    print(f" {i}. {t}")

        elif choice == "3":
            if not targets:
                print("No targets to crawl; add some first.")
                continue
            idx = input("Enter target number to crawl (or '0' for first): ").strip()
            try:
                i = int(idx) - 1 if idx else 0
                if i < 0:
                    i = 0
                onion = targets[i]
            except Exception:
                print("Invalid index.")
                continue

            # rate limit enforcement
            elapsed = time.time() - last_request_time
            if elapsed < RATE_LIMIT_SECONDS:
                wait = RATE_LIMIT_SECONDS - elapsed
                print(f"Rate limit: waiting {wait:.1f}s before request...")
                time.sleep(wait)

            try:
                print(f"Crawling {onion} ...")
                meta = fetch_metadata(onion)
                append_result({
                    "timestamp": meta["timestamp"],
                    "onion": meta["onion"],
                    "status_code": meta["status_code"],
                    "response_time_s": meta["response_time_s"],
                    "server": meta["server"],
                    "content_type": meta["content_type"],
                    "snippet": meta["snippet"],
                })
                print("✅ Saved metadata. Snippet/title:", meta["snippet"] or "<none>")
            except Exception as e:
                print("❌ Error fetching metadata:", e)
            last_request_time = time.time()

        elif choice == "4":
            if not targets:
                print("No targets to crawl; add some first.")
                continue
            confirm_all = input(f"This will query {len(targets)} targets (rate {RATE_LIMIT_SECONDS}s). Continue? (y/n): ").strip().lower()
            if confirm_all != "y":
                continue
            for onion in targets:
                elapsed = time.time() - last_request_time
                if elapsed < RATE_LIMIT_SECONDS:
                    time.sleep(RATE_LIMIT_SECONDS - elapsed)
                print(f"Crawling {onion} ...")
                try:
                    meta = fetch_metadata(onion)
                    append_result({
                        "timestamp": meta["timestamp"],
                        "onion": meta["onion"],
                        "status_code": meta["status_code"],
                        "response_time_s": meta["response_time_s"],
                        "server": meta["server"],
                        "content_type": meta["content_type"],
                        "snippet": meta["snippet"],
                    })
                    print("  Saved. Snippet/title:", meta["snippet"] or "<none>")
                except Exception as e:
                    print("  Error:", e)
                last_request_time = time.time()

        elif choice == "5":
            if not os.path.exists(RESULTS_CSV):
                print("No results file yet.")
            else:
                print(f"\n--- Head of {RESULTS_CSV} ---")
                with open(RESULTS_CSV, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f):
                        print(line.rstrip())
                        if i >= 9:
                            break

        elif choice == "6":
            print("Exiting. Stay lawful and safe.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
