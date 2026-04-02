import requests
import json
import time

def test_api_quick_scrape():
    url = "http://localhost:8000/api/intel/quick-scrape"
    payload = {
        "url": "http://twcd7fo4eepxznx7vajl5njkfpkz3g3z6qhynffcy3hb6n42dov2omid.onion",
        "primary_keyword": "PayPal",
        "include_images": True
    }
    
    print(f"[API Test] Triggering deep-scrape via API: {payload['url']}...")
    try:
        response = requests.post(url, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            print("\n[SUCCESS] API returned valid intelligence data:")
            print(f"TITLE: {data.get('title')}")
            print(f"EMAILS FOUND: {len(data.get('emails', []))}")
            print(f"RELEVANCE: {data.get('score')}")
        else:
            print(f"[FAIL] API returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}. Is the FastAPI server running on port 8000?")

if __name__ == "__main__":
    test_api_quick_scrape()
