import requests
import sys

def check_proxy(label, proxy_url):
    proxies = {'http': proxy_url, 'https': proxy_url}
    print(f"[CHECK] Testing {label} at {proxy_url}...")
    try:
        # We test a clearnet site via the proxy first
        response = requests.get("https://check.torproject.org/api/ip", proxies=proxies, timeout=10)
        if response.status_code == 200:
            data = response.json()
            is_tor = data.get('IsTor', False)
            ip = data.get('IP')
            print(f"[SUCCESS] {label} is working! Tor Active: {is_tor}, IP: {ip}")
            return True
        else:
            print(f"[FAILURE] {label} returned status {response.status_code}")
    except Exception as e:
        print(f"[FAILURE] {label} connection failed: {e}")
    return False

# Common Tor ports
tor_browser_proxy = "socks5h://127.0.0.1:9150"
tor_service_proxy = "socks5h://127.0.0.1:9050"

found = False
if check_proxy("Tor Browser Proxy", tor_browser_proxy): found = True
print("-" * 30)
if check_proxy("Tor Service Proxy", tor_service_proxy): found = True

if not found:
    print("\n[CRITICAL] No active Tor proxy found!")
    print("Search and Scrape functions will fail unless you start Tor Browser or the Tor Service.")
    print("Tip: If you want to search WITHOUT Tor, we need to disable the proxy in main.py.")
