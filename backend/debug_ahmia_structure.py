import requests
from bs4 import BeautifulSoup

def debug_ahmia():
    query = "paypal"
    url = f"https://ahmia.fi/search/?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0'
    }
    
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for common result patterns
            results = soup.find_all('li', class_='result')
            print(f"Found {len(results)} 'li.result' items.")
            
            if len(results) == 0:
                print("Checking for alternative structures...")
                # Maybe divs or different classes
                all_lis = soup.find_all('li')
                print(f"Found {len(all_lis)} total <li> items.")
                for i, li in enumerate(all_lis[:5]):
                    print(f"LI {i} classes: {li.get('class', 'No class')}")
            
            for i, res in enumerate(results[:3]):
                print(f"\n--- Result {i} ---")
                print(res.prettify()[:500])
        else:
            print(f"Failed to fetch. Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_ahmia()
