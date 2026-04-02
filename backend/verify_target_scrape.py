import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.scraper import DarkDumpScraper

async def test_deep_scrape():
    url = "http://twcd7fo4eepxznx7vajl5njkfpkz3g3z6qhynffcy3hb6n42dov2omid.onion"
    # Ensure Tor is running
    scraper = DarkDumpScraper(use_tor=True)
    
    print(f"Testing deep intelligence extraction for: {url}")
    print("[Deep Intel] Launching Playwright via Tor Proxy (9150)...")
    
    result = scraper.scrape_onion(
        url, 
        primary_keyword="PayPal", 
        secondary_keywords=["email", "credential", "database"],
        include_images=True
    )
    
    if not result:
        print(f"FAIL: Could not scrape {url}. Ensure Tor is running on port 9150.")
        return

    print(f"\n[INTEL REPORT] {result.title}")
    print(f"RELEVANCE SCORE: {result.score}")
    print(f"KEYWORDS MATCHED: {result.matched_keywords}")
    
    # Check for extracted entities (Emails, Documents)
    emails = result.emails
    docs = result.metadata.get("documents", [])
    
    print(f"\n--- Extracted Intelligence ---")
    print(f"Emails Found ({len(emails)}): {emails[:5]}...")
    print(f"Leak Vectors Found: {list(result.metadata.get('leaks', {}))}")
    print(f"Visual Evidence (Images): {len(result.images)} items captured")
    
    print("\n[SUCCESS] Deep intelligence extraction completed successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(test_deep_scrape())
    except Exception as e:
        print(f"[ERROR] Scrape execution failed: {e}")
