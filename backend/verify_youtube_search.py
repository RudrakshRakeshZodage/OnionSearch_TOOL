import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.scraper import DarkDumpScraper

async def test_discovery():
    scraper = DarkDumpScraper(use_tor=False)
    query = "YouTube leaks credentials database"
    print(f"Testing discovery for query: {query}")
    
    results = scraper.search_ahmia(query, amount=10)
    
    if not results:
        print("FAIL: No results found for YouTube related intelligence.")
    else:
        print(f"SUCCESS: Found {len(results)} targets.")
        # Safe printing for Windows terminals with non-ASCII characters
        for i, res in enumerate(results):
            try:
                title = res['title'].encode('ascii', 'ignore').decode('ascii')
                print(f"[{i+1}] {title} - {res['url']}")
            except:
                print(f"[{i+1}] Target found - {res['url']}")

if __name__ == "__main__":
    asyncio.run(test_discovery())
