import requests
from bs4 import BeautifulSoup

def debug_selectors():
    proxy = {"http": "socks5h://127.0.0.1:9150", "https": "socks5h://127.0.0.1:9150"}
    url = "https://ahmia.fi/search/?q=market"
    r = requests.get(url, proxies=proxy, timeout=30)
    soup = BeautifulSoup(r.text, 'html.parser')

    print("Checking for ID 'ahmiaResultsPage':", bool(soup.find(id='ahmiaResultsPage')))
    
    # Let's find all 'li' with classes to see what's there
    for li in soup.find_all('li')[:20]:
        print(f"LI tag: {li.get('class')}")
    
    # Try finding the results via a different approach
    results = soup.find_all('li', class_='result')
    print(f"Results with 'li.result': {len(results)}")
    
    # Maybe it's just 'result' class?
    results_any = soup.find_all(class_='result')
    print(f"Total elements with 'result' class: {len(results_any)}")

debug_selectors()
