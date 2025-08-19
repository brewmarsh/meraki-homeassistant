"""End-to-end tests for the Meraki Web UI."""

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

TEST_PORT = 9999
MOCK_DATA = {
    "networks": [{"id": "N_12345", "name": "Test Network", "tags": "e2e-test"}],
    "clients": [], # Clients are no longer displayed in the UI
}
MOCK_SETTINGS = {
    "scan_interval": 300
}

@pytest.fixture(name="setup_integration")
async def setup_integration_fixture(hass: HomeAssistant):
    """Set up the Meraki integration with the web UI enabled."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_e2e_entry",
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={CONF_ENABLE_WEB_UI: True, CONF_WEB_UI_PORT: TEST_PORT, **MOCK_SETTINGS},
    )
    config_entry.add_to_hass(hass)

    with patch(
        "custom_components.meraki_ha.MerakiDataCoordinator._async_update_data",
        return_value=MOCK_DATA,
    ), patch(
        "custom_components.meraki_ha.async_register_webhook",
        return_value=None,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        yield config_entry


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_dashboard_loads_and_displays_data(hass: HomeAssistant, setup_integration):
    """Test that the dashboard loads and displays network data, but not clients."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")

        content = page.locator("#page-content")

        # Check for the network card
        network_card_header = content.locator("h2:has-text('Networks (1)')")
        await expect(network_card_header).to_be_visible()

        network_name = content.locator("p.font-medium:has-text('Test Network')")
        await expect(network_name).to_be_visible()

        # The client card should no longer be present
        client_card_header = content.locator("h2:has-text('Clients')")
        await expect(client_card_header).not_to_be_visible()

        await browser.close()


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_navigation_to_network_detail(hass: HomeAssistant, setup_integration):
    """Test navigation to a network detail page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")

        content = page.locator("#page-content")
        await expect(content.locator("h2:has-text('Networks (1)')")).to_be_visible()

        await content.locator("a:has-text('Test Network')").click()

        await expect(page).to_have_url(f"http://localhost:{TEST_PORT}/networks/N_12345")

        detail_content = page.locator("#page-content")
        placeholder = detail_content.locator("div:has-text('Network Detail Page Placeholder')")
        await expect(placeholder).to_be_visible()

        await browser.close()


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_navigation_to_settings_page(hass: HomeAssistant, setup_integration):
    """Test navigation to the settings page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")

        await expect(page.locator("h1:has-text('Meraki UI')")).to_be_visible()

        await page.locator("a:has-text('Settings')").click()

        await expect(page).to_have_url(f"http://localhost:{TEST_PORT}/settings")

        settings_content = page.locator("#page-content")
        header = settings_content.locator("h2:has-text('Integration Settings')")
        await expect(header).to_be_visible()

        await browser.close()
