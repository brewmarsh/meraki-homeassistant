"""End-to-end tests for the Meraki Web UI."""

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

TEST_PORT = 9988
MOCK_SETTINGS = {"scan_interval": 300, "enable_device_status": True}


class ReuseAddrTCPServer(socketserver.TCPServer):
    """TCPServer that allows address reuse."""

    allow_reuse_address = True


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
async def test_e2e_panel_comprehensive(
    hass: HomeAssistant,
    setup_integration: MockConfigEntry,
) -> None:
    """Test the panel comprehensive flow: load, details, settings.

    Args:
    ----
        hass: The Home Assistant instance.
        setup_integration: The setup_integration fixture.
    """
    # Use a simple python http server to serve the www directory
    # This is to avoid issues with the HA server not serving the files
    os.chdir("custom_components/meraki_ha/www")
    # Build the frontend to make sure the latest changes are included
    os.system("npm run build")

    # Create a test index.html that points to the compiled JS
    with open("test_index.html", "w") as f:
        f.write(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Test Panel</title>
                <style>
                    body { margin: 0; padding: 0; }
                </style>
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

            # Capture console logs and errors
            page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
            page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))

            # Prepare mock data with enabled network
            # We copy MOCK_ALL_DATA and ensure the first network is enabled
            mock_data: dict[str, Any] = MOCK_ALL_DATA.copy()
            if mock_data["networks"]:
                mock_data["networks"][0]["is_enabled"] = True

            # Ensure options are present in the mock data
            mock_data["options"] = MOCK_SETTINGS

            mock_data_json = json.dumps(mock_data)

            # Define Custom Elements and Mock HASS
            await page.add_init_script(
                f"""
                // Initialize calls storage if not exists
                if (!sessionStorage.getItem('mockCallWS')) {{
                    sessionStorage.setItem('mockCallWS', JSON.stringify([]));
                }}

                // Define mock HA elements
                class HACard extends HTMLElement {{
                    constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                    connectedCallback() {{
                        this.shadowRoot.innerHTML = `
                            <div style="
                                border: 1px solid #ccc;
                                padding: 16px;
                                display: block;">
                                <slot></slot>
                            </div>
                        `;
                        this.style.display = 'block';
                    }}
                }}
                class HAIcon extends HTMLElement {{
                    constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                    connectedCallback() {{
                        this.shadowRoot.innerHTML = `<span>icon</span>`;
                        this.style.display = 'inline-block';
                        this.style.width = '24px';
                        this.style.height = '24px';
                    }}
                }}
                class HASwitch extends HTMLElement {{
                    constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                    connectedCallback() {{
                        this.shadowRoot.innerHTML = `<input type="checkbox" />`;
                        this.style.display = 'inline-block';
                    }}
                    set checked(val) {{
                        const input = this.shadowRoot.querySelector('input');
                        if (input) input.checked = val;
                    }}
                    get checked() {{
                        const input = this.shadowRoot.querySelector('input');
                        return input ? input.checked : false;
                    }}
                    // Simulate click dispatch
                    click() {{
                        const input = this.shadowRoot.querySelector('input');
                        if (input) {{
                            input.click();
                            // Dispatch change event manually as react needs it
                            const event = new Event('change', {{ bubbles: true }});
                        }}
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
                    panel.panel = {{
                        config: {{
                            config_entry_id: 'test-entry-id-from-panel'
                        }}
                    }};
                    panel.hass = {{
                        callWS: async (msg) => {{
                            console.log("callWS called with type: " + msg.type);

                            // Store in sessionStorage to persist across reloads
                            const calls = JSON.parse(
                                sessionStorage.getItem('mockCallWS')
                            );
                            calls.push(msg);
                            sessionStorage.setItem('mockCallWS', JSON.stringify(calls));

                            if (msg.type === 'meraki_ha/get_config') {{
                                return {mock_data_json};
                            }}
                            if (msg.type === 'meraki_ha/update_options') {{
                                return {{}};
                            }}
                            return {{}};
                        }},
                    }};
                }});
                """
            )

            # Use test_index.html which points to the compiled JS
            await page.goto(f"http://127.0.0.1:{TEST_PORT}/test_index.html")

            # 1. Panel Loading
            # Wait for the loading indicator to disappear
            loading_indicator = page.get_by_text("Loading...")
            await expect(loading_indicator).to_be_hidden(timeout=10000)

            # Check for the network card
            network_card = page.locator("ha-card").first
            await expect(network_card).to_be_visible()
            await expect(
                network_card.locator("span", has_text="[Network]")
            ).to_contain_text("Main Office")

            # 2. Panel Details Appearing
            # Expand the network card
            expand_button = network_card.locator("ha-icon[icon='mdi:chevron-down']")
            await expand_button.click()

            # Check if devices are displayed in the table
            device_table = page.locator("table").first
            await expect(device_table).to_be_visible()

            # Check for specific devices from MOCK_ALL_DATA
            await expect(page.get_by_text("Test Device")).to_be_visible()
            await expect(page.get_by_text("Test MX Device")).to_be_visible()
            await expect(page.get_by_text("Test GX Device")).to_be_visible()

            # 3. Device Details Navigation
            # Find the details button for "Test Device" (MR33)
            # The row contains "Test Device", find the button in that row
            device_row = page.locator("tr", has_text="Test Device")
            details_button = device_row.locator("button[title='View Details']")
            await details_button.click()

            # Verify we navigated to Device View
            await expect(page.get_by_text("Test Device", exact=True)).to_be_visible()
            await expect(page.get_by_text("Model: MR33")).to_be_visible()
            await expect(page.get_by_text("Serial: Q234-ABCD-5678")).to_be_visible()

            # Navigate back to dashboard
            back_button = page.get_by_role("button", name="Back to Dashboard")
            await back_button.click()

            # Verify we are back
            await expect(network_card).to_be_visible()
            # Ensure table is still visible (it might not be if state wasn't persisted)
            # but let's check basic visibility
            # NetworkView persists state in sessionStorage, so it should remain open.
            await expect(device_table).to_be_visible()

            # 4. Panel Settings Changes
            # Click settings button
            settings_button = page.locator("button[title='Settings']")
            await settings_button.click()

            # Wait for settings modal
            settings_modal = page.locator("div.fixed.inset-0")
            await expect(settings_modal).to_be_visible()

            # Toggle "Device & Entity Model" (key: enable_device_status)
            # Find the switch for this label
            # The structure is label -> parent -> ha-switch
            # We can find the row by text
            settings_row = settings_modal.locator(
                "div.flex.items-center.justify-between",
                has_text="Device & Entity Model",
            )
            toggle_switch = settings_row.locator("ha-switch")

            # Click the switch to toggle it
            await toggle_switch.click()

            # Click Save & Reload
            save_button = settings_modal.locator("button", has_text="Save & Reload")
            await save_button.click()

            # Verify settings modal closed
            await expect(settings_modal).to_be_hidden()

            # Verify update_options was called
            calls = await page.evaluate(
                "JSON.parse(sessionStorage.getItem('mockCallWS'))"
            )
            # We expect at least one get_config and one update_options
            update_call = next(
                (c for c in calls if c["type"] == "meraki_ha/update_options"), None
            )

            if update_call is None:
                print(f"DEBUG: All calls: {calls}")

            assert update_call is not None, "meraki_ha/update_options was not called"

            # We explicitly set "enable_device_status": True in mock data
            # So toggling it should make it False
            assert update_call["options"]["enable_device_status"] is False

            await browser.close()
    finally:
        if httpd:
            httpd.shutdown()
        if httpd_thread:
            httpd_thread.join()
        # Clean up the test html file
        if os.path.exists("test_index.html"):
            os.remove("test_index.html")
        # Change back to the original directory
        os.chdir("../../../..")
