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
    "clients": [{"id": "c_67890", "mac": "00:11:22:33:44:55", "description": "Test Client"}],
}

@pytest.fixture(name="setup_integration")
async def setup_integration_fixture(hass: HomeAssistant):
    """Set up the Meraki integration with the web UI enabled."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_e2e_entry",
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={CONF_ENABLE_WEB_UI: True, CONF_WEB_UI_PORT: TEST_PORT},
    )
    config_entry.add_to_hass(hass)

    with patch(
        "custom_components.meraki_ha.MerakiDataCoordinator._async_update_data",
        return_value=MOCK_DATA,
    ), patch(
        "custom_components.meraki_ha.async_register_webhook",
        return_value=None,
    ):
        # Use the standard HA test helper to set up the integration
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        yield config_entry


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_dashboard_loads_and_displays_data(hass: HomeAssistant, setup_integration):
    """
    Test Case UI-P0-01: View Dashboard with Data.
    Ensures the dashboard loads and displays data from the coordinator.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")

        # Check for the network card
        network_card = page.locator(".text-xl.font-semibold:has-text('Networks (1)')")
        await expect(network_card).to_be_visible()

        network_name = page.locator("p.font-medium:has-text('Test Network')")
        await expect(network_name).to_be_visible()

        # Check for the client card
        client_card = page.locator(".text-xl.font-semibold:has-text('Clients (1)')")
        await expect(client_card).to_be_visible()

        client_description = page.locator("p.font-medium:has-text('Test Client')")
        await expect(client_description).to_be_visible()

        await browser.close()


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_navigation_to_network_detail(hass: HomeAssistant, setup_integration):
    """
    Test Case UI-P0-02: Navigate to Network Detail View.
    Ensures clicking a network card navigates to the correct detail page.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")
        await page.locator("p.font-medium:has-text('Test Network')").click()

        await expect(page).to_have_url(f"http://localhost:{TEST_PORT}/networks/N_12345")

        header = page.locator("h3:has-text('Network Information')")
        await expect(header).to_be_visible()

        network_id_detail = page.locator("dd:has-text('N_12345')")
        await expect(network_id_detail).to_be_visible()

        await browser.close()


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_navigation_to_client_detail(hass: HomeAssistant, setup_integration):
    """
    Test Case UI-P0-03: Navigate to Client Detail View.
    Ensures clicking a client card navigates to the correct detail page.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")
        await page.locator("p.font-medium:has-text('Test Client')").click()

        await expect(page).to_have_url(f"http://localhost:{TEST_PORT}/clients/00:11:22:33:44:55")

        header = page.locator("h3:has-text('Client Information')")
        await expect(header).to_be_visible()

        client_mac_detail = page.locator("dd:has-text('00:11:22:33:44:55')")
        await expect(client_mac_detail).to_be_visible()

        await browser.close()
