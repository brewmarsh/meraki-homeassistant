"""End-to-end tests for the Meraki Web UI."""

from __future__ import annotations

import http.server
import json
import os
import socketserver
import threading
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

TEST_PORT = 9995
MOCK_SETTINGS = {"scan_interval": 300}


@pytest.fixture(name="setup_integration")
async def setup_integration_fixture(
    hass: HomeAssistant,
    socket_enabled: None,
) -> MockConfigEntry:
    """Set up the Meraki integration with the web UI enabled.

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
            "custom_components.meraki_ha.MerakiDataCoordinator._async_update_data",
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
    """Test that the dashboard loads and displays network data.

    Args:
    ----
        hass: The Home Assistant instance.
        setup_integration: The setup_integration fixture.
    """
    # Use a simple python http server to serve the www directory
    # This is to avoid issues with the HA server not serving the files

    # Change to the www directory to serve files from there
    os.chdir("custom_components/meraki_ha/www")

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = None
    httpd_thread = None
    try:
        httpd = socketserver.TCPServer(("", TEST_PORT), Handler)
        httpd_thread = threading.Thread(target=httpd.serve_forever)
        httpd_thread.start()

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Create a basic HTML file to load the panel
            with open("test_index.html", "w") as f:
                f.write(
                    """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Test</title>
                    </head>
                    <body>
                        <div id="root"></div>
                        <script type="module" src="/meraki-panel.js"></script>
                        <script>
                            customElements.whenDefined('meraki-panel').then(() => {
                                const panel = document.createElement('meraki-panel');
                                panel.hass = window.hass;
                                panel.panel = { config: {
                                    config_entry_id: 'test_entry'
                                }};
                                document.body.appendChild(panel);
                            });
                        </script>
                    </body>
                    </html>
                """
                )

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
                      }},
                      sendMessagePromise: async (message) => {{
                        return {mock_data_json};
                      }}
                    }}
                  }};
                """,
            )

            await page.goto(f"http://localhost:{TEST_PORT}/test_index.html")

            # Check for the network card, which should now be rendered with mock data
            network_card = page.locator("ha-card").filter(
                has_text="[Network] Test Network"
            )
            await expect(network_card).to_be_visible()

            await browser.close()
    finally:
        if httpd:
            httpd.shutdown()
        if httpd_thread:
            httpd_thread.join()
        # Change back to the original directory
        os.chdir("../../../..")
