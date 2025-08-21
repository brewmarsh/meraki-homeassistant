import asyncio
from playwright.async_api import async_playwright, Page, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://localhost:9988/networks")

        # Wait for the table to be visible
        await expect(page.get_by_role("table")).to_be_visible()

        # Get the name of the first network
        first_network_name = await page.locator("tbody tr:first-child td:first-child").inner_text()
        print(f"Ignoring network: {first_network_name}")

        # Click the "Ignore" button on the first row
        await page.locator("tbody tr:first-child button").click()

        # The UI should update to remove the row. We can check that the network name is no longer visible.
        await expect(page.get_by_text(first_network_name)).not_to_be_visible()

        # Take a screenshot
        await page.screenshot(path="jules-scratch/verification/ignore_button.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
