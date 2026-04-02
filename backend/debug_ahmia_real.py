import asyncio
from playwright.async_api import async_playwright

async def debug_ahmia_real():
    async with async_playwright() as pw:
        # Launch without Tor for discovery
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to https://ahmia.fi ...")
        await page.goto("https://ahmia.fi", wait_until="networkidle")
        
        print("Filling search form with 'bitcoin'...")
        # Most search engines have an input named 'q'
        await page.fill('input[name="q"]', "bitcoin")
        await page.press('input[name="q"]', "Enter")
        
        print("Waiting for results at URL: ", page.url)
        await page.wait_for_timeout(5000) # Wait a few seconds for results to load
        
        # Take a screenshot of the result page to see what's happening
        await page.screenshot(path="ahmia_results.png")
        print("Screenshot saved to ahmia_results.png")

        # Inspect the page
        html = await page.content()
        print("Page Title:", await page.title())
        print("Found any 'li' tags?", await page.locator('li').count())
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_ahmia_real())
