from services.scraper import DarkDumpScraper
import json

scraper = DarkDumpScraper(use_tor=True)
query = "market"
print(f"[DEBUG] Searching Ahmia for '{query}'...")

results = scraper.search_ahmia(query, amount=5)
if results:
    print(f"[SUCCESS] Found {len(results)} results.")
    for r in results:
        print(f" - {r['title']} ({r['url']})")
else:
    print("[FAILURE] No results found on Ahmia. This might be a block on Ahmia's end or a proxy issue.")
