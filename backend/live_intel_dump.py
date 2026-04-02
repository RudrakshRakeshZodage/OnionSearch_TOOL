import sys
import os
import asyncio
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.scraper import DarkDumpScraper

async def live_intel_dump():
    # Target some of the discovered YouTube/Threat links
    targets = [
        "http://fraudgptcri76abwyzswmmf44awao2lfrowulh7l2j4udeus3wndsrad.onion",
        "http://gptfkuovke3jxhes5icipzmdsicmh2s7ijdhbnnng4crmpqmrgargsyd.onion",
        "http://twcd7fo4eepxznx7vajl5njkfpkz3g3z6qhynffcy3hb6n42dov2omid.onion"
    ]
    
    scraper = DarkDumpScraper(use_tor=True)
    
    print("="*80)
    print(" LIVE INTELLIGENCE EXTRACTION DUMP ")
    print("="*80)
    
    for url in targets:
        print(f"\n[TARGET] {url}")
        print("-" * 40)
        
        try:
            # Deep scrape with JS rendering
            result = scraper.scrape_onion(
                url, 
                primary_keyword="YouTube", 
                secondary_keywords=["email", "database", "leak", "login"],
                include_images=True
            )
            
            if not result:
                print(f"[!] Target Unreachable or Blocked.")
                continue

            # Display Extracted Data
            print(f"TITLE:    {result.title}")
            print(f"SCORE:    {result.score} (Relevance)")
            print(f"SNIPPET:  {result.snippet[:150]}...")
            
            print(f"\n--- EXTRACTED ENTITIES ---")
            print(f"EMAILS:   {result.emails if result.emails else 'None Detected'}")
            print(f"VECTORS:  {list(result.metadata.get('leaks', {}))}")
            print(f"IMAGES:   {len(result.images)} URLs captured")
            
            # Print raw metadata for the user to see the internal structure
            print(f"\n--- RAW INTEL METADATA (JSON) ---")
            print(json.dumps(result.metadata, indent=2))
            
        except Exception as e:
            print(f"[ERROR] Extraction failed for {url}: {e}")
            
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(live_intel_dump())
