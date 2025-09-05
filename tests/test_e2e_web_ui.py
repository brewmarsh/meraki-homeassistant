"""End-to-end tests for the Meraki Web UI."""

import json
import pytest
from unittest.mock import patch

from playwright.async_api import async_playwright, expect
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_ENABLE_WEB_UI,
    CONF_WEB_UI_PORT,
)

from .const import MOCK_ALL_DATA

TEST_PORT = 9999
MOCK_SETTINGS = {"scan_interval": 300}


@pytest.fixture(name="setup_integration")
async def setup_integration_fixture(hass: HomeAssistant, socket_enabled):
    """Set up the Meraki integration with the web UI enabled."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_e2e_entry",
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={
            CONF_ENABLE_WEB_UI: True,
            CONF_WEB_UI_PORT: TEST_PORT,
            **MOCK_SETTINGS,
        },
    )
    config_entry.add_to_hass(hass)

    # This patch is now for the backend, which the UI no longer directly uses in this test setup
    with (
        patch(
            "custom_components.meraki_ha.MerakiDataCoordinator._async_update_data",
            return_value=MOCK_ALL_DATA,
        ),
        patch(
            "custom_components.meraki_ha.api.websocket.ws_subscribe_meraki_data",
            return_value=None,
        ),
        patch(
            "custom_components.meraki_ha.async_register_webhook",
            return_value=None,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        yield config_entry


@pytest.mark.asyncio
async def test_dashboard_loads_and_displays_data(
    hass: HomeAssistant, setup_integration
):
    """Test that the dashboard loads and displays network data."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text()}"))

        # Serialize the mock data to be injected into the page
        mock_data_json = json.dumps(MOCK_ALL_DATA)

        try:
            await page.goto(f"http://localhost:{TEST_PORT}/")

            # Create the mock hass object in the page
            await page.evaluate(
                f"""
                window.mockHass = {{
                    connection: {{
                        subscribeMessage: async (callback, subscription) => {{
                            console.log('Mock subscribeMessage called with:', subscription);
                            const mockData = {mock_data_json};
                            const message = {{
                                type: 'result',
                                success: true,
                                result: mockData
                            }};
                            callback(message);
                            return () => Promise.resolve();
                        }}
                    }}
                }};
                """
            )

            # Get the panel and set the hass property
            await page.evaluate("document.querySelector('meraki-ha-panel').setAttribute('config_entry_id', 'test_e2e_entry')")
            await page.evaluate("document.querySelector('meraki-ha-panel').hass = window.mockHass")

            # Wait for the network card to be visible, which indicates the data has loaded
            await page.wait_for_selector("[data-testid=network-card]", timeout=10000)

            # Now that we know it's there, we can make assertions
            network_card = page.locator("[data-testid=network-card]")
            await expect(network_card).to_be_visible()
            await expect(network_card.locator("p")).to_have_text("Test Network")

        finally:
            await browser.close()


# @pytest.mark.asyncio
# async def test_navigation_to_network_detail(hass: HomeAssistant, setup_integration):
#     """Test navigation to a network detail page."""
#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         page = await browser.new_page()

#         mock_data_json = json.dumps(MOCK_ALL_DATA)
#         await page.add_init_script(
#             f"""
#               window.hass = {{
#                 connection: {{
#                   subscribeMessage: async (callback, subscription) => {{
#                     const mockData = {mock_data_json};
#                     const message = {{ type: 'result', success: true, result: mockData }};
#                     callback(message);
#                     return () => Promise.resolve();
#                   }}
#                 }}
#               }};
#             """
#         )

#         await page.goto(f"http://localhost:{TEST_PORT}/")

#         network_card = page.locator("[data-testid=network-card]")
#         await expect(network_card).to_be_visible()

#         await network_card.click()

#         # Add a small delay to allow React to re-render
#         await page.wait_for_timeout(500)

#         await page.screenshot(path="e2e-network-detail-failure.png")

#         # Use a more specific locator for the header
#         await expect(page.locator("h2:has-text('Network Information')")).to_be_visible()

#         await browser.close()
