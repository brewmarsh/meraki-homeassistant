"""End-to-end tests for the Meraki Web UI."""

from __future__ import annotations

import dataclasses
import http.server
import json
import socketserver
import threading
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from playwright.async_api import Error, Page, async_playwright, expect
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.const_conf import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from homeassistant.core import HomeAssistant

from .const import MOCK_ALL_DATA

MOCK_SETTINGS = {"scan_interval": 300, "enable_device_status": True}


# JavaScript Templates for Playwright init script
JS_TEMPLATE = """
// Initialize calls storage if not exists
if (!sessionStorage.getItem('mockCallWS')) {{
    sessionStorage.setItem('mockCallWS', JSON.stringify([]));
}}

// Define mock HA elements
{ha_elements_js}

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
                sessionStorage.getItem('mockCallWS') || '[]'
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
                sessionStorage.getItem('mockCallWS') || '[]'
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

HA_ELEMENTS_JS = """
class HACard extends HTMLElement {
    constructor() { super(); this.attachShadow({mode: 'open'}); }
    connectedCallback() {
        this.shadowRoot.innerHTML = `
            <div style="
                border: 1px solid #ccc;
                padding: 16px;
                display: block;">
                <slot></slot>
            </div>
        `;
        this.style.display = 'block';
    }
}
class HAIcon extends HTMLElement {
    constructor() { super(); this.attachShadow({mode: 'open'}); }
    connectedCallback() {
        const icon = this.getAttribute('icon');
        this.shadowRoot.innerHTML = `
            <span style="display: flex; align-items: center;
                         justify-content: center;">
                icon: ${icon}
            </span>
        `;
        this.style.display = 'inline-block';
        this.style.width = '24px';
        this.style.height = '24px';
    }
    static get observedAttributes() { return ['icon']; }
    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'icon') {
            this.shadowRoot.innerHTML = `
                <span style="display: flex; align-items: center;
                             justify-content: center;">
                    icon: ${newValue}
                </span>
            `;
        }
    }
}
class HASwitch extends HTMLElement {
    constructor() { super(); this.attachShadow({mode: 'open'}); }
    connectedCallback() {
        this.shadowRoot.innerHTML = `<input type="checkbox" />`;
        this.style.display = 'inline-block';
        const input = this.shadowRoot.querySelector('input');
        input.checked = this.hasAttribute('checked');
        input.addEventListener('change', (e) => {
           this.dispatchEvent(new CustomEvent('change', {
               detail: { value: e.target.checked },
               bubbles: true,
               composed: true
           }));
        });
    }
    set checked(val) {
        const input = this.shadowRoot.querySelector('input');
        if (input) input.checked = val;
        if (val) this.setAttribute('checked', '');
        else this.removeAttribute('checked');
    }
    get checked() {
        const input = this.shadowRoot.querySelector('input');
        return input ? input.checked : false;
    }
    click() {
        const input = this.shadowRoot.querySelector('input');
        if (input) {
            input.click();
        }
    }
}

if (!customElements.get('ha-card')) {
    customElements.define('ha-card', HACard);
}
if (!customElements.get('ha-icon')) {
    customElements.define('ha-icon', HAIcon);
}
if (!customElements.get('ha-switch')) {
    customElements.define('ha-switch', HASwitch);
}
"""


class ReuseAddrTCPServer(socketserver.TCPServer):
    """TCPServer that allows address reuse."""

    allow_reuse_address = True


class _MerakiTestHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler to serve files from a specific directory."""

    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        """Initialize the handler with a specific directory."""
        super().__init__(*args, directory=directory, **kwargs)


@pytest.fixture(name="setup_integration")
async def setup_integration_fixture(
    hass: HomeAssistant,
    socket_enabled: None,  # pylint: disable=unused-argument
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


@pytest.fixture(name="http_server_and_test_file")
def http_server_and_test_file_fixture() -> tuple[int, str]:
    """Set up and tear down a simple HTTP server to serve the www directory."""
    original_cwd = Path.cwd()
    www_dir = original_cwd / "custom_components" / "meraki_ha" / "www"
    assert www_dir.is_dir(), f"WWW directory not found: {www_dir}"

    test_index_content = """
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
    # Create a temporary file inside the www_dir to be served
    temp_html_filename = "test_e2e_index.html"
    temp_html_path = www_dir / temp_html_filename
    temp_html_path.write_text(test_index_content)

    httpd: ReuseAddrTCPServer | None = None
    httpd_thread: threading.Thread | None = None
    try:
        # Use port 0 to let the OS choose an available port
        with ReuseAddrTCPServer(
            ("", 0),
            lambda *args, **kwargs: _MerakiTestHTTPHandler(
                *args, directory=str(www_dir), **kwargs
            ),
        ) as s:
            port = s.server_address[1]
            httpd = s
            httpd_thread = threading.Thread(target=httpd.serve_forever)
            httpd_thread.daemon = True
            httpd_thread.start()
            yield port, f"http://127.0.0.1:{port}/{temp_html_filename}"
    finally:
        if httpd:
            httpd.shutdown()
        if httpd_thread:
            httpd_thread.join()
        if temp_html_path.exists():
            temp_html_path.unlink()


@pytest.fixture(name="playwright_browser_page")
async def playwright_browser_page_fixture() -> Page:
    """Launches a Playwright browser and provides a page."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            yield page
            await browser.close()
    except Error as e:
        if "Executable doesn't exist at" in str(e):
            pytest.skip(
                "Playwright browsers not installed. "
                "Run `playwright install` to run this test."
            )
        raise


@pytest.fixture(name="mock_hass_config_data")
def mock_hass_config_data_fixture() -> dict[str, Any]:
    """Generates comprehensive mock data for the Home Assistant frontend."""
    mock_data: dict[str, Any] = MOCK_ALL_DATA.copy()
    # Convert dataclasses to dicts for frontend consumption
    mock_data["networks"] = [
        dataclasses.asdict(n) if dataclasses.is_dataclass(n) else n
        for n in mock_data.get("networks", [])
    ]
    mock_data["devices"] = [
        dataclasses.asdict(d) if dataclasses.is_dataclass(d) else d
        for d in mock_data.get("devices", [])
    ]

    # Ensure at least one network is enabled
    if mock_data["networks"]:
        mock_data["networks"][0]["is_enabled"] = True

    # Add specific devices and SSIDs for detailed testing
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
    ssid_data = {
        "number": 0,
        "name": "Guest WiFi",
        "enabled": True,
        "networkId": "N_12345",
        "entity_id": "switch.guest_wifi",
    }

    mock_data["devices"].extend([switch_device, camera_device])
    mock_data["ssids"] = mock_data.get("ssids", []) + [ssid_data]
    if mock_data["networks"]:
        mock_data["networks"][0]["ssids"] = mock_data["ssids"]

    mock_data["options"] = MOCK_SETTINGS

    return mock_data


@pytest.fixture(name="javascript_init_script")
def javascript_init_script_fixture(mock_hass_config_data: dict[str, Any]) -> str:
    """Generates the full JavaScript init script for Playwright."""
    mock_data_json = json.dumps(mock_hass_config_data)
    return JS_TEMPLATE.format(
        ha_elements_js=HA_ELEMENTS_JS,
        mock_data_json=mock_data_json,
    )


# Helper functions for UI interactions
async def _wait_for_loading_to_hide(page: Page) -> None:
    """Waits for the loading indicator to disappear."""
    loading_indicator = page.get_by_text("Loading...")
    await expect(loading_indicator).to_be_hidden(timeout=10000)


async def _expand_network_card(page: Page, network_name: str) -> None:
    """Expands a specific network card."""
    network_card = page.locator("ha-card").filter(has_text=network_name).first
    expand_button = network_card.locator("ha-icon[icon='mdi:chevron-down']")
    await expand_button.click()
    await expect(page.locator("table").first).to_be_visible()


async def _verify_device_visibility(page: Page, device_names: list[str]) -> None:
    """Verifies that specified devices are visible in the device table."""
    for name in device_names:
        await expect(page.get_by_text(name)).to_be_visible()


async def _view_device_details(page: Page, device_name: str) -> None:
    """Clicks to view details of a specific device."""
    device_row = page.locator("tr", has_text=device_name)
    details_button = device_row.locator("button[title='View Details']")
    await details_button.click()
    await expect(page.get_by_text(device_name, exact=True)).to_be_visible()
    await expect(page.get_by_text("Entities")).to_be_visible()


async def _go_back_to_dashboard(page: Page) -> None:
    """Clicks the 'Back to Dashboard' button."""
    back_button = page.get_by_role("button", name="Back to Dashboard")
    await back_button.click()
    # Expect a network card to be visible again
    await expect(page.locator("ha-card").first).to_be_visible()


async def _verify_ssid_card_status(
    page: Page, ssid_name: str, expected_status: str
) -> None:
    """Verifies the status text of an SSID card."""
    ssid_card = page.locator("div.bg-light-card", has_text=ssid_name).first
    await expect(ssid_card).to_be_visible()
    await expect(ssid_card).to_contain_text(expected_status)


async def _verify_camera_status(
    page: Page, camera_name: str, expected_status: str
) -> None:
    """Verifies the status of a specific camera device."""
    camera_row = page.locator("tr", has_text=camera_name)
    status_cell = camera_row.locator("td").nth(2)  # 0=Name, 1=Model, 2=Status
    await expect(status_cell).to_contain_text(expected_status)


async def _navigate_to_settings(page: Page) -> None:
    """Clicks the settings button to open the settings modal."""
    settings_button = page.locator("button[title='Settings']")
    await settings_button.click()
    # Settings modal locator uses common Tailwind CSS classes for fixed overlays
    await expect(page.locator("div.fixed.inset-0")).to_be_visible()


async def _toggle_setting_and_save(page: Page, setting_text: str) -> None:
    """Toggles a specific setting switch and clicks Save & Reload."""
    settings_modal = page.locator("div.fixed.inset-0")
    settings_row = settings_modal.locator(
        "div.flex.items-center.justify-between",
        has_text=setting_text,
    )
    toggle_switch = settings_row.locator("ha-switch")
    await toggle_switch.click()
    save_button = settings_modal.locator("button", has_text="Save & Reload")
    await save_button.click()
    await expect(settings_modal).to_be_hidden()  # Verify settings modal closed


async def _get_websocket_calls(page: Page) -> list[dict[str, Any]]:
    """Retrieves stored WebSocket calls from sessionStorage."""
    # The '|| "[]"' handles cases where sessionStorage.getItem('mockCallWS') might be null
    return await page.evaluate(
        "JSON.parse(sessionStorage.getItem('mockCallWS') || '[]')"
    )


@pytest.mark.asyncio
async def test_e2e_panel_comprehensive(
    hass: HomeAssistant,  # pylint: disable=unused-argument
    setup_integration: MockConfigEntry,  # pylint: disable=unused-argument
    http_server_and_test_file: tuple[int, str],
    playwright_browser_page: Page,
    javascript_init_script: str,
) -> None:
    """Test the panel comprehensive flow: load, details, settings, and new scenarios.

    Args:
    ----
        hass: The Home Assistant instance.
        setup_integration: The setup_integration fixture.
        http_server_and_test_file: Tuple containing HTTP server port and base URL.
        playwright_browser_page: The Playwright page object.
        javascript_init_script: The JavaScript init script for the page.
    """
    _port, base_url = http_server_and_test_file
    page = playwright_browser_page

    # Capture console logs and errors from the browser
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))

    # Inject mock Home Assistant environment and custom elements
    await page.add_init_script(javascript_init_script)

    # Navigate to the test panel
    await page.goto(base_url)

    # 1. Panel Loading & Initial Navigation
    await _wait_for_loading_to_hide(page)
    network_card = page.locator("ha-card").first
    await expect(network_card).to_be_visible()
    await expect(network_card.locator("span", has_text="[Network]")).to_contain_text(
        "Main Office"
    )

    # 2. Device Expansion
    await _expand_network_card(page, "Main Office")
    await _verify_device_visibility(page, ["Office Switch", "Front Door Camera"])

    # 3. Switch Port Control (View Details & Back)
    await _view_device_details(page, "Office Switch")
    await _go_back_to_dashboard(page)

    # 4. SSID Visibility Check
    await _verify_ssid_card_status(page, "Guest WiFi", "Enabled")

    # 5. Camera Visibility
    await _verify_camera_status(page, "Front Door Camera", "Online")

    # 6. Panel Settings Changes
    await _navigate_to_settings(page)
    await _toggle_setting_and_save(page, "Device & Entity Model")

    # Verify that 'meraki_ha/update_options' was called with the correct data
    calls = await _get_websocket_calls(page)
    update_call = next(
        (c for c in calls if c["type"] == "meraki_ha/update_options"), None
    )

    assert update_call is not None, "meraki_ha/update_options was not called"
    assert (
        update_call["options"]["enable_device_status"] is False
    ), "enable_device_status option was not updated to False"
