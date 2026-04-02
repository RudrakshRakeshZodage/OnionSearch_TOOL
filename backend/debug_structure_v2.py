import requests
from bs4 import BeautifulSoup

def debug_no_proxy():
    url = "https://ahmia.fi/search/?q=market"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0"}
    
    print(f"Fetching {url} WITHOUT PROXY...")
    r = requests.get(url, headers=headers, timeout=15)
    print(f"Status Code: {r.status_code}")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Check all 'li' elements
    all_li = soup.find_all('li')
    print(f"Total LI tags: {len(all_li)}")
    
    for i, li in enumerate(all_li[:30]):
        # Print class and a snippet of text
        print(f"LI {i}: class={li.get('class')}, text={li.text.strip()[:50]}")
        link = li.find('a')
        if link:
            print(f"  -> Link: {link.get('href')}")

debug_no_proxy()
