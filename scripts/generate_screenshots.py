"""Script to generate screenshots for the README."""

import http.server
import json
import os
import socketserver
import threading
import time
from functools import partial

from playwright.sync_api import sync_playwright

TEST_PORT = 9988
MOCK_SETTINGS = {"scan_interval": 300, "enable_device_status": True}
REPO_ROOT = os.getcwd()
SCREENSHOT_DIR = os.path.join(REPO_ROOT, "docs", "images")
WWW_DIR = os.path.join(REPO_ROOT, "custom_components", "meraki_ha", "www")

# Mock Data designed to produce a nice looking screenshot
MOCK_DATA = {
    "enabled_networks": ["N_12345"],
    "networks": [
        {
            "id": "N_12345",
            "name": "Main Office",
            "productTypes": ["switch", "camera", "wireless"],
            "tags": [],
            "enrollmentString": None,
            "url": "https://dashboard.meraki.com",
            "timeZone": "America/Los_Angeles",
            "is_enabled": True,
            "ssids": [
                {
                    "number": 0,
                    "name": "Guest WiFi",
                    "enabled": True,
                    "networkId": "N_12345",
                    "entity_id": "switch.guest_wifi",
                    "psk_entity_id": None,
                    "visible": True,
                    "authMode": "open",
                }
            ],
        }
    ],
    "devices": [
        {
            "serial": "Q234-ABCD-SW1",
            "name": "Office Switch",
            "model": "MS220-8P",
            "networkId": "N_12345",
            "productType": "switch",
            "status": "online",
            "firmware": "switch-14-31",
            "lanIp": "192.168.1.2",
            "mac": "00:11:22:33:44:55",
            "ports_statuses": [
                {
                    "portId": "1",
                    "status": "Connected",
                    "enabled": True,
                    "speed": "1 Gbps",
                    "duplex": "full",
                    "usageInKb": {"total": 123456},
                    "poe": {"enabled": True},
                    "powerUsageInWh": 10.5,
                },
                {
                    "portId": "2",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"enabled": True},
                },
                {
                    "portId": "3",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"enabled": True},
                },
                {
                    "portId": "4",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"enabled": True},
                },
                {
                    "portId": "5",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"enabled": True},
                },
                {
                    "portId": "6",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"enabled": True},
                },
                {
                    "portId": "7",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"enabled": True},
                },
                {
                    "portId": "8",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"enabled": True},
                },
            ],
            "entity_id": "switch.office_switch",
        },
        {
            "serial": "Q234-ABCD-CAM1",
            "name": "Front Door Camera",
            "model": "MV12N",
            "networkId": "N_12345",
            "productType": "camera",
            "status": "online",
            "firmware": "camera-4-15",
            "lanIp": "192.168.1.50",
            "mac": "00:11:22:33:44:56",
            "entity_id": "camera.front_door_camera",
            "rtsp_url": "rtsp://192.168.1.50:9000/live",
        },
        {
            "serial": "Q234-ABCD-AP1",
            "name": "Lobby AP",
            "model": "MR33",
            "networkId": "N_12345",
            "productType": "wireless",
            "status": "online",
            "firmware": "wireless-28-5",
            "lanIp": "192.168.1.10",
            "mac": "00:11:22:33:44:57",
            "entity_id": "update.lobby_ap_firmware",
        },
    ],
    "options": MOCK_SETTINGS,
}


class ReuseAddrTCPServer(socketserver.TCPServer):
    """TCPServer that allows address reuse."""

    allow_reuse_address = True


def run_server() -> None:
    """Run a simple HTTP server to serve the frontend."""
    # Create index.html for testing in the WWW_DIR
    with open(os.path.join(WWW_DIR, "screenshot_index.html"), "w") as f:
        f.write("""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Meraki Panel</title>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        background-color: var(--primary-background-color, #fafafa);
                    }
                </style>
                <script>
                    window.Hass = {
                        callWS: () => Promise.resolve({}),
                    };
                </script>
            </head>
            <body>
                <script type="module" src="/meraki-panel.js"></script>
            </body>
            </html>
        """)

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=WWW_DIR)
    httpd = ReuseAddrTCPServer(("", TEST_PORT), handler)
    try:
        httpd.serve_forever()
    except OSError:
        pass  # Handle case where port is already in use or server shuts down


def generate_screenshots() -> None:
    """Generate screenshots using Playwright."""
    # Start Server in thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Give server a moment to start
    time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 800})

        # Define Custom Elements and Mock HASS similar to test
        init_script = f"""
            const MOCK_DATA = {json.dumps(MOCK_DATA)};

            class HACard extends HTMLElement {{
                constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                connectedCallback() {{
                    this.shadowRoot.innerHTML = `
                        <style>
                            :host {{
                                display: block;
                                background: white;
                                border-radius: 4px;
                                box-shadow: 0 2px 2px 0 rgba(0,0,0,0.14),
                                            0 3px 1px -2px rgba(0,0,0,0.12),
                                            0 1px 5px 0 rgba(0,0,0,0.2);
                                color: var(--primary-text-color);
                                margin-bottom: 16px;
                            }}
                            .card-header {{
                                padding: 16px 16px 0;
                                font-size: 24px;
                                line-height: 32px;
                                color: var(--primary-text-color);
                            }}
                            .card-content {{ padding: 16px; }}
                        </style>
                        <div class="card-header"><slot name="header"></slot></div>
                        <div class="card-content"><slot></slot></div>
                    `;
                }}
            }}
            class HAIcon extends HTMLElement {{
                constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                connectedCallback() {{
                    const icon = this.getAttribute('icon');
                    // Simple mock representation of icons
                    let symbol = '📱';
                    if (icon && icon.includes('switch')) symbol = '🔌';
                    if (icon && icon.includes('camera')) symbol = '📹';
                    if (icon && icon.includes('wifi')) symbol = '📶';
                    if (icon && icon.includes('chevron-down')) symbol = '▼';
                    if (icon && icon.includes('chevron-up')) symbol = '▲';

                    this.shadowRoot.innerHTML = `
                        <span style="font-family: sans-serif; font-size: 24px;">
                            ${{symbol}}
                        </span>
                    `;
                }}
                static get observedAttributes() {{ return ['icon']; }}
                attributeChangedCallback(name, oldValue, newValue) {{
                    this.connectedCallback();
                }}
            }}
            class HASwitch extends HTMLElement {{
                constructor() {{ super(); this.attachShadow({{mode: 'open'}}); }}
                connectedCallback() {{
                    this.shadowRoot.innerHTML = `
                        <input type="checkbox"
                               style="transform: scale(1.5); margin: 10px;" />
                    `;
                    const input = this.shadowRoot.querySelector('input');
                    input.checked = this.hasAttribute('checked');
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
                panel.panel = {{ config: {{ config_entry_id: 'test' }} }};
                panel.hass = {{
                    states: {{
                        "switch.office_switch": {{
                            state: "on",
                            attributes: {{}}
                        }},
                        "camera.front_door_camera": {{
                            state: "idle",
                            attributes: {{}}
                        }},
                        "switch.guest_wifi": {{
                            state: "on",
                            attributes: {{}}
                        }},
                        "update.lobby_ap_firmware": {{
                            state: "off",
                            attributes: {{}}
                        }}
                    }},
                    callWS: async (msg) => {{
                        if (msg.type === 'meraki_ha/get_config') return MOCK_DATA;
                        return {{}};
                    }},
                    callService: async () => {{}},
                    themes: {{ darkMode: false }}
                }};
            }});
        """
        page.add_init_script(init_script)

        page.goto(f"http://127.0.0.1:{TEST_PORT}/screenshot_index.html")

        # Wait for content - the React component uses .network-card class
        page.wait_for_selector(".network-card", timeout=30000)
        page.wait_for_timeout(3000)  # Wait for animations/rendering

        # Take Network View Screenshot
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "network_view.png"))
        print(f"Saved {os.path.join(SCREENSHOT_DIR, 'network_view.png')}")

        # Try to expand network details if expand button exists
        expand_button = page.locator(".network-card .expand-button").first
        if expand_button.is_visible():
            expand_button.click()
            page.wait_for_timeout(1000)

        # Try to navigate to device detail view
        # Look for device rows or device cards
        device_element = page.locator(".device-row, .device-card", has_text="Office Switch")
        if device_element.count() > 0:
            device_element.first.click()
            page.wait_for_timeout(2000)
            # Take Device Detail Screenshot
            page.screenshot(path=os.path.join(SCREENSHOT_DIR, "device_detail_view.png"))
            print(f"Saved {os.path.join(SCREENSHOT_DIR, 'device_detail_view.png')}")
        else:
            # If no device detail navigation, just take another screenshot
            print("No device detail navigation found, skipping device_detail_view.png")

        browser.close()


if __name__ == "__main__":
    try:
        generate_screenshots()
    finally:
        index_path = os.path.join(WWW_DIR, "screenshot_index.html")
        if os.path.exists(index_path):
            os.remove(index_path)
