"""End-to-end tests for device status display in the Meraki Web UI."""

from __future__ import annotations

import http.server
import json
import os
import socketserver
import threading
from typing import Any
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

TEST_PORT = 9989  # Different port to avoid conflict
MOCK_SETTINGS = {"scan_interval": 300, "enable_device_status": True}

# Create a modified mock data with an unavailable device
MOCK_UNAVAILABLE_DEVICE = {
    "serial": "Q234-UNAVAILABLE",
    "name": "Unavailable Device",
    "model": "MR33",
    "networkId": "N_12345",
    "productType": "wireless",
    "lanIp": "1.2.3.7",
    "status": "online",  # Meraki says online
    "entity_id": "switch.unavailable_device",  # HA entity
}

MOCK_REPRO_DATA: dict[str, Any] = MOCK_ALL_DATA.copy()
MOCK_REPRO_DATA["devices"] = [MOCK_UNAVAILABLE_DEVICE]
if MOCK_REPRO_DATA["networks"]:
    MOCK_REPRO_DATA["networks"][0]["is_enabled"] = True
    MOCK_REPRO_DATA["networks"][0]["ssids"] = []  # Clear SSIDs to simplify


class ReuseAddrTCPServer(socketserver.TCPServer):
    """TCPServer that allows address reuse."""

    allow_reuse_address = True


@pytest.fixture(name="setup_integration")
async def setup_integration_fixture(
    hass: HomeAssistant,
    socket_enabled: None,
) -> MockConfigEntry:
    """Set up the Meraki integration with the web UI enabled."""
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
            return_value=MOCK_REPRO_DATA,
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
@pytest.mark.skip(reason="Requires playwright browser automation")
async def test_repro_unavailable_status(
    hass: HomeAssistant,
    setup_integration: MockConfigEntry,
) -> None:
    """Test that unavailable HA entity causes unavailable status in UI."""
    original_cwd = os.getcwd()
    os.chdir("custom_components/meraki_ha/www")
    # Build not strictly needed if we assume previous build is good,
    # but let's do it to be safe or rely on previous
    # os.system("npm run build")

    with open("test_repro_index.html", "w") as f:
        f.write(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Test Panel</title>
            </head>
            <body>
                <script type="module" src="/meraki-panel.js"></script>
            </body>
            </html>
            """
        )

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = None
    httpd_thread = None
    try:
        httpd = ReuseAddrTCPServer(("", TEST_PORT), Handler)
        httpd_thread = threading.Thread(target=httpd.serve_forever)
        httpd_thread.daemon = True
        httpd_thread.start()

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            mock_data = MOCK_REPRO_DATA.copy()
            mock_data["options"] = MOCK_SETTINGS
            mock_data_json = json.dumps(mock_data)

            await page.add_init_script(
                f"""
                // Define mock HA elements (simplified)
                class HACard extends HTMLElement {{
                    constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                    connectedCallback() {{
                        this.shadowRoot.innerHTML = `<div><slot></slot></div>`;
                        this.style.display = 'block';
                    }}
                }}
                class HAIcon extends HTMLElement {{
                    constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                    connectedCallback() {{
                        this.shadowRoot.innerHTML = `<span>icon</span>`;
                    }}
                }}
                class HASwitch extends HTMLElement {{
                    constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                    connectedCallback() {{
                        this.shadowRoot.innerHTML = `<input type="checkbox" />`;
                    }}
                }}

                if (!customElements.get('ha-card')) {{
                    customElements.define('ha-card', HACard);
                }}
                if (!customElements.get('ha-icon')) {{
                    customElements.define('ha-icon', HAIcon);
                }}
                if (!customElements.get('ha-switch')) {{
                    customElements.define('ha-switch', HASwitch);
                }}

                document.addEventListener('DOMContentLoaded', () => {{
                    const panel = document.createElement('meraki-panel');
                    document.body.appendChild(panel);
                    panel.panel = {{ config: {{ config_entry_id: 'test-e2e_entry' }} }};
                    panel.hass = {{
                        callWS: async (msg) => {{
                            if (msg.type === 'meraki_ha/get_config') {{
                                return {mock_data_json};
                            }}
                            return {{}};
                        }},
                        states: {{
                            "switch.unavailable_device": {{ state: "unavailable" }}
                        }}
                    }};
                }});
                """
            )

            await page.goto(f"http://127.0.0.1:{TEST_PORT}/test_repro_index.html")

            # Wait for content
            network_header = page.locator("span", has_text="[Network] Main Office")
            await expect(network_header).to_be_visible()

            # Expand network (assuming collapsed by default in NetworkView)
            # Find the header div and click it (NetworkView.tsx logic)
            # It has a click handler on the card-header
            header_div = page.locator("ha-card").locator("div.card-header")
            await header_div.click()

            # Check for device status
            # In DeviceTable, the status column is the 3rd one.
            # Row has "Unavailable Device"
            row = page.locator("tr", has_text="Unavailable Device")
            await expect(row).to_be_visible()

            # The status cell text should be "unavailable" currently, but we want it
            # to be "online" because the Meraki API status is "online" even if
            # the HA entity is unavailable.
            status_cell = row.locator("td").nth(2)
            await expect(status_cell).to_contain_text("online", ignore_case=True)

            await browser.close()
    finally:
        if httpd:
            httpd.shutdown()
        if httpd_thread:
            httpd_thread.join()
        if os.path.exists("test_repro_index.html"):
            os.remove("test_repro_index.html")
        os.chdir(original_cwd)
