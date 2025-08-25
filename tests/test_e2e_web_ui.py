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

from .const import MOCK_ALL_DATA

TEST_PORT = 9999
MOCK_SETTINGS = {"scan_interval": 300}


@pytest.fixture(name="setup_integration")
async def setup_integration_fixture(hass: HomeAssistant):
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

    with patch(
        "custom_components.meraki_ha.MerakiDataCoordinator._async_update_data",
        return_value=MOCK_ALL_DATA,
    ), patch(
        "custom_components.meraki_ha.async_register_webhook",
        return_value=None,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        yield config_entry


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_dashboard_loads_and_displays_data(
    hass: HomeAssistant, setup_integration
):
    """Test that the dashboard loads and displays network data, but not clients."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")

        content = page.locator("main")

        # Check for the network card using data-testid
        network_card = content.locator("[data-testid=network-card]")
        await expect(network_card).to_be_visible()
        await expect(network_card.locator("p.font-medium")).to_have_text("Test Network")

        await browser.close()


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_navigation_to_network_detail(hass: HomeAssistant, setup_integration):
    """Test navigation to a network detail page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")

        content = page.locator("main")
        await expect(content.locator("[data-testid=network-card]")).to_be_visible()

        await content.locator("[data-testid=network-card]").click()

        await expect(page).to_have_url(f"http://localhost:{TEST_PORT}/networks/N_12345")

        await page.screenshot(path="e2e-network-detail-failure.png")

        detail_content = page.locator("main")
        await expect(detail_content.locator("h2")).to_have_text("Test Network")

        await browser.close()


@pytest.mark.enable_socket
@pytest.mark.asyncio
async def test_navigation_to_settings_page(hass: HomeAssistant, setup_integration):
    """Test navigation to the settings page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"http://localhost:{TEST_PORT}/")

        await page.locator("a:has-text('Settings')").click()

        await expect(page).to_have_url(f"http://localhost:{TEST_PORT}/settings")

        settings_content = page.locator("main")
        header = settings_content.locator("[data-testid=settings-header]")
        await expect(header).to_be_visible()

        await browser.close()
