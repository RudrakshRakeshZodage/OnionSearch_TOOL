import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.scraper import DarkDumpScraper

async def test_discovery():
    scraper = DarkDumpScraper(use_tor=False)
    query = "paypal"
    print(f"Testing discovery for query: {query}")
    
    results = scraper.search_ahmia(query, amount=5)
    
    if not results:
        print("FAIL: No results found.")
    else:
        print(f"SUCCESS: Found {len(results)} results.")
        for i, res in enumerate(results):
            print(f"[{i+1}] {res['title']} - {res['url']}")

if __name__ == "__main__":
    asyncio.run(test_discovery())
