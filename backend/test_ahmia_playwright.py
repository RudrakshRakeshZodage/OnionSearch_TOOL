import asyncio
from playwright.async_api import async_playwright
import json

async def test_ahmia_playwright():
    url = "https://ahmia.fi/search/?q=market"
    async with async_playwright() as pw:
        # Launch WITHOUT Tor first for discovery, as it's a public site
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"Navigating to {url} via Playwright...")
        await page.goto(url, wait_until="networkidle")
        
        # Wait for either results or a timeout
        try:
            await page.wait_for_selector('li.result', timeout=10000)
        except:
            print("Timed out waiting for 'li.result'")

        # Capture results
        results = await page.eval_on_selector_all('li.result', 
            "items => items.map(i => ({ title: i.querySelector('a')?.innerText, url: i.querySelector('cite')?.innerText }))"
        )
        
        print(f"Found {len(results)} results via Playwright.")
        for r in results[:5]:
            print(f" - {r['title']} ({r['url']})")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_ahmia_playwright())
