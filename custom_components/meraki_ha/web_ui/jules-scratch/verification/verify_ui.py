import asyncio
from playwright.async_api import async_playwright, Page, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to Settings page
        await page.goto("http://localhost:9988/settings")
        await expect(page.get_by_role("heading", name="Integration Settings")).to_be_visible()
        await page.screenshot(path="jules-scratch/verification/settings_page.png")

        # Navigate to Networks page
        await page.goto("http://localhost:9988/networks")
        await expect(page.get_by_role("heading", name="Networks")).to_be_visible()
        await page.screenshot(path="jules-scratch/verification/networks_page.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
