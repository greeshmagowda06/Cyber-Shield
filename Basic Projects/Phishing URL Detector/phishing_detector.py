import re

def check_url(url):
    suspicious_patterns = [
        "https?://[0-9]{1,3}",      # IP address instead of domain
        "https?://.*@.*",           # @ symbol in URL
        "login|verify|update|free|bonus",  # common phishing words
        "https?://.*\..*\..*\.",    # too many subdomains
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, url.lower()):
            return "⚠️ Suspicious URL Detected!"
    return "✅ URL looks safe."

if __name__ == "__main__":
    print("Phishing URL Detector")
    user_url = input("Enter a URL to check: ")
    print(check_url(user_url))
