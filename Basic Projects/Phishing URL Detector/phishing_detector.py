import re

def check_url(url):
    suspicious_patterns = [
        r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", 
        r"(?i)login|verify|update|free|bonus|secure|account|webscr|ebayisapi|signin", 
        r"https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+/[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+",
        r"bit\.ly|goo\.gl|tinyurl\.com|ow\.ly|t\.co", 
        r"^(?!https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+)", 
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, url.lower()):
            return "⚠️ Suspicious URL Detected!"
    return "✅ URL looks safe."

if __name__ == "__main__":
    print("Phishing URL Detector")
    while True:
        user_url = input("Enter a URL to check (or 'q' to quit): ")
        if user_url.lower() == 'q':
            break
        print(check_url(user_url))
