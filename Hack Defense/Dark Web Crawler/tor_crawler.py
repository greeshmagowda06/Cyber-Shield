# tor_crawler/tor_crawler.py
import requests, sys
from urllib.parse import urlparse
# Requires Tor running locally with SOCKS proxy at 9050 (or configure differently)
PROXIES = {"http":"socks5h://127.0.0.1:9050","https":"socks5h://127.0.0.1:9050"}

def fetch(url):
    try:
        r = requests.get(url, proxies=PROXIES, timeout=15)
        return r.status_code, r.text[:500]
    except Exception as e:
        return None, str(e)

if __name__=="__main__":
    if len(sys.argv)<2:
        print("Usage: python tor_crawler.py http://expyuzz4wqqyqhjn.onion")
        sys.exit(1)
    code, snippet = fetch(sys.argv[1])
    print("Status:",code)
    print(snippet)
