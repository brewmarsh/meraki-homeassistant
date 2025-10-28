"""End-to-end tests for the Meraki Web UI."""
from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from homeassistant.core import HomeAssistant
from playwright.async_api import async_playwright, expect
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DOMAIN,
)

from .const import MOCK_ALL_DATA

TEST_PORT = 9988
MOCK_SETTINGS = {"scan_interval": 300}


@pytest.fixture(name="setup_integration")
async def setup_integration_fixture(
    hass: HomeAssistant,
    socket_enabled: None,
) -> MockConfigEntry:
    """
    Set up the Meraki integration with the web UI enabled.

    Args:
    ----
        hass: The Home Assistant instance.
        socket_enabled: The socket_enabled fixture.

    Returns
    -------
        The mock config entry.

    """
    hass.config.external_url = "https://example.com"
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_e2e_entry",
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={
            **MOCK_SETTINGS,
        },
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.MerakiDataUpdateCoordinator._async_update_data",
            return_value=MOCK_ALL_DATA,
        ),
        patch(
            "custom_components.meraki_ha.api.websocket.ws_subscribe_meraki_data",
            return_value=None,
        ),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        yield config_entry


@pytest.mark.asyncio
async def test_dashboard_loads_and_displays_data(
    hass: HomeAssistant,
    setup_integration: MockConfigEntry,
) -> None:
    """
    Test that the dashboard loads and displays network data.

    Args:
    ----
        hass: The Home Assistant instance.
        setup_integration: The setup_integration fixture.

    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Serialize the mock data to be injected into the page
        mock_data_json = json.dumps(MOCK_ALL_DATA)

        # This script runs before the page's scripts, creating a mock hass object
        await page.add_init_script(
            f"""
              window.hass = {{
                connection: {{
                  subscribeMessage: async (callback, subscription) => {{
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
            """,
        )

        await page.goto(f"http://localhost:{TEST_PORT}/")

        # Check for the network card, which should now be rendered with mock data
        network_card = page.locator("[data-testid=network-card]")
        await expect(network_card).to_be_visible()
        await expect(network_card.locator("p")).to_have_text("Test Network")

        await browser.close()
