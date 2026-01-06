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

# Check if hass_frontend is available (required for this test)
try:
    import hass_frontend  # noqa: F401

    HAS_FRONTEND = True
except ImportError:
    HAS_FRONTEND = False

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
@pytest.mark.skipif(not HAS_FRONTEND, reason="hass_frontend not installed")
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
async def test_e2e_panel_comprehensive(
    hass: HomeAssistant,
    setup_integration: MockConfigEntry,
) -> None:
    """Test the panel comprehensive flow: load, details, settings, and new scenarios.

    Args:
    ----
        hass: The Home Assistant instance.
        setup_integration: The setup_integration fixture.
    """
    # Use a simple python http server to serve the www directory
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

            # Prepare mock data with enabled network and enhanced devices
            mock_data: dict[str, Any] = MOCK_ALL_DATA.copy()
            if mock_data["networks"]:
                mock_data["networks"][0]["is_enabled"] = True

            # Add a switch with ports to mock data
            switch_device = {
                "serial": "Q234-ABCD-SW1",
                "name": "Office Switch",
                "model": "MS220",
                "networkId": "N_12345",
                "productType": "switch",
                "status": "online",
                "ports_statuses": [
                    {"portId": "1", "status": "Connected", "enabled": True},
                    {"portId": "2", "status": "Disconnected", "enabled": False},
                ],
                "entity_id": "switch.office_switch",
            }
            # Add a camera to mock data
            camera_device = {
                "serial": "Q234-ABCD-CAM1",
                "name": "Front Door Camera",
                "model": "MV12",
                "networkId": "N_12345",
                "productType": "camera",
                "status": "online",
                "lanIp": "192.168.1.50",
                "entity_id": "camera.front_door_camera",
            }
            # Add SSID with entity_id for toggling check
            ssid_data = {
                "number": 0,
                "name": "Guest WiFi",
                "enabled": True,
                "networkId": "N_12345",
                "entity_id": "switch.guest_wifi",
            }

            mock_data["devices"] = mock_data.get("devices", []) + [
                switch_device,
                camera_device,
            ]
            mock_data["ssids"] = mock_data.get("ssids", []) + [ssid_data]
            mock_data["networks"][0]["ssids"] = mock_data["ssids"]

            # Add enabled_networks to ensure networks are shown
            mock_data["enabled_networks"] = ["N_12345"]

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
                        const icon = this.getAttribute('icon');
                        this.shadowRoot.innerHTML = `
                            <span style="display: flex; align-items: center;
                                         justify-content: center;">
                                icon: ${{icon}}
                            </span>
                        `;
                        this.style.display = 'inline-block';
                        this.style.width = '24px';
                        this.style.height = '24px';
                    }}
                    static get observedAttributes() {{ return ['icon']; }}
                    attributeChangedCallback(name, oldValue, newValue) {{
                        if (name === 'icon') {{
                            this.shadowRoot.innerHTML = `
                                <span style="display: flex; align-items: center;
                                             justify-content: center;">
                                    icon: ${{newValue}}
                                </span>
                            `;
                        }}
                    }}
                }}
                class HASwitch extends HTMLElement {{
                    constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                    connectedCallback() {{
                        this.shadowRoot.innerHTML = `<input type="checkbox" />`;
                        this.style.display = 'inline-block';
                        const input = this.shadowRoot.querySelector('input');
                        input.checked = this.hasAttribute('checked');
                        input.addEventListener('change', (e) => {{
                           this.dispatchEvent(new CustomEvent('change', {{
                               detail: {{ value: e.target.checked }},
                               bubbles: true,
                               composed: true
                           }}));
                        }});
                    }}
                    set checked(val) {{
                        const input = this.shadowRoot.querySelector('input');
                        if (input) input.checked = val;
                        if (val) this.setAttribute('checked', '');
                        else this.removeAttribute('checked');
                    }}
                    get checked() {{
                        const input = this.shadowRoot.querySelector('input');
                        return input ? input.checked : false;
                    }}
                    click() {{
                        const input = this.shadowRoot.querySelector('input');
                        if (input) {{
                            input.click();
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
                        states: {{
                            "switch.office_switch": {{ state: "on", attributes: {{}} }},
                            "camera.front_door_camera": {{
                                state: "idle",
                                attributes: {{}}
                            }},
                            "switch.guest_wifi": {{ state: "on", attributes: {{}} }}
                        }},
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
                             if (msg.type === 'call_service') {{
                                return {{}};
                            }}
                            return {{}};
                        }},
                        callService: async (domain, service, data) => {{
                             console.log(`callService: ${{domain}}.${{service}}`, data);
                              const calls = JSON.parse(
                                sessionStorage.getItem('mockCallWS')
                            );
                            calls.push({{
                                type: 'call_service',
                                domain,
                                service,
                                service_data: data
                            }});
                            sessionStorage.setItem('mockCallWS', JSON.stringify(calls));
                        }}
                    }};
                }});
                """
            )

            # Use test_index.html which points to the compiled JS
            await page.goto(f"http://127.0.0.1:{TEST_PORT}/test_index.html")

            # 1. Panel Loading & Navigation
            # Wait for the loading indicator to disappear
            loading_indicator = page.get_by_text("Loading...")
            await expect(loading_indicator).to_be_hidden(timeout=10000)

            # Check for the network card (uses .network-card class)
            network_card = page.locator(".network-card").first
            await expect(network_card).to_be_visible(timeout=10000)
            # Network name is in h2 inside .title
            await expect(network_card.locator(".title h2")).to_contain_text(
                "Main Office"
            )

            # 2. Device Expansion
            # Expand the network card (click the header to expand if collapsed)
            network_header = network_card.locator(".network-header")
            # Check if network is already expanded (device table visible)
            device_table = page.locator(".device-table").first
            if not await device_table.is_visible():
                await network_header.click()

            # Check if devices are displayed in the table
            await expect(device_table).to_be_visible(timeout=10000)

            # Verify visibility of devices in table
            await expect(page.get_by_text("Office Switch")).to_be_visible()
            await expect(page.get_by_text("Front Door Camera")).to_be_visible()

            # 3. Device Row Interaction
            # Click on the device row to navigate to device view
            switch_row = page.locator("tr.device-row", has_text="Office Switch")
            await switch_row.click()

            # Verify Device View loaded (shows device name in h1)
            device_name = page.locator(".device-header h1, .device-info h1").first
            await expect(device_name).to_contain_text("Office Switch")

            # Go back to dashboard using the back button
            back_button = page.locator(".back-button")
            await back_button.click()

            # Verify we're back on the network view
            await expect(network_card).to_be_visible()

            # Re-expand network (state is lost when Dashboard remounts)
            device_table = page.locator(".device-table").first
            if not await device_table.is_visible():
                network_header = network_card.locator(".network-header")
                await network_header.click()
                await expect(device_table).to_be_visible(timeout=5000)

            # 4. Camera Visibility in Device Table
            # Verify camera is shown in device table with status
            camera_row = page.locator("tr.device-row", has_text="Front Door Camera")
            await expect(camera_row).to_be_visible(timeout=5000)
            # Status is shown in the row with .status-badge class
            await expect(camera_row.locator(".status-badge")).to_contain_text("online")

            # 5. SSID Visibility (if shown in expanded network)
            # Check if SSID list is visible (new class name)
            ssid_list = page.locator(".ssid-list")
            if await ssid_list.count() > 0:
                # Find Guest WiFi SSID item (new class name)
                ssid_item = page.locator(".ssid-item", has_text="Guest WiFi")
                await expect(ssid_item).to_be_visible()

            await browser.close()
    finally:
        if httpd:
            httpd.shutdown()
        if httpd_thread:
            httpd_thread.join()
        if os.path.exists("test_index.html"):
            os.remove("test_index.html")
        os.chdir("../../../..")
