import asyncio
from playwright.async_api import async_playwright, Page, expect


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://localhost:9988/index.html")

        # Click the "Parental Controls" link in the sidebar
        await page.get_by_role("link", name="Parental Controls").click()

        # Verify that the page has loaded
        await expect(
            page.get_by_role("heading", name="Content Filtering")
        ).to_be_visible()
        await expect(page.get_by_role("heading", name="Client Devices")).to_be_visible()

        # Get the initial state of the first toggle button
        first_toggle = page.locator("tbody tr:first-child button")
        initial_class = await first_toggle.get_attribute("class")

        # Click the first toggle button
        await first_toggle.click()

        # Verify that the toggle button's state has changed
        await expect(first_toggle).not_to_have_class(initial_class)

        # Take a screenshot
        await page.screenshot(
            path="jules-scratch/verification/parental_controls_feature.png"
        )

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
