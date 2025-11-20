"""Live end-to-end tests for the Meraki Web UI, running against a live HA instance."""

import os
import pytest
from playwright.async_api import async_playwright, expect

# The base URL of the Home Assistant instance
HA_BASE_URL = "http://localhost:8123"


@pytest.mark.asyncio
async def test_live_dashboard_loads():
    """
    Test that the live dashboard loads after logging in.
    This test assumes that the Home Assistant instance is already set up with a user.
    """
    username = os.environ.get("HA_USERNAME")
    password = os.environ.get("HA_PASSWORD")

    if not username or not password:
        pytest.skip(
            "HA_USERNAME and HA_PASSWORD environment variables must be set to run this test."
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            await page.goto(HA_BASE_URL)

            # Check if we need to onboard (fresh instance)
            onboarding_header = page.locator("h1", has_text="Welcome home!")
            if await onboarding_header.count() > 0:
                # This is a fresh instance, we need to onboard.
                # For simplicity, this test assumes an existing user.
                # A more complex test would handle the onboarding process here.
                # For now, we'll just log that and skip the test.
                print("Detected a fresh Home Assistant instance. Skipping test.")
                pytest.skip(
                    "This test requires an already configured Home Assistant instance."
                )

            # Log in
            await page.locator("ha-textfield[label='Username']").fill(username)
            await page.locator("ha-textfield[label='Password']").fill(password)
            await page.get_by_role("button", name="Log In").click()

            # Wait for the main dashboard to load
            await expect(page.locator("home-assistant-main")).to_be_visible()

            # Navigate to the Meraki panel
            await page.goto(f"{HA_BASE_URL}/meraki-panel")

            # Check that the Meraki panel loads and shows some expected content
            # (e.g., the network card from the original e2e test)
            network_card = page.locator("[data-testid=network-card]")
            await expect(network_card).to_be_visible()
            await expect(network_card.locator("p")).to_have_text(
                "Test Network"
            )  # This will depend on the data in the live instance

        finally:
            await browser.close()
