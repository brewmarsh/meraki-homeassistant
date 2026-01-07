"""
Script to generate screenshots from the actual React UI.

This script builds the React frontend, serves it locally, injects mock data,
and uses Playwright to capture screenshots of different views.
"""

# ruff: noqa: E501

import http.server
import json
import socketserver
import subprocess
import sys
import threading
from functools import partial
from pathlib import Path

from playwright.sync_api import sync_playwright

# Configuration
TEST_PORT = 9988
REPO_ROOT = Path(__file__).parent.parent
SCREENSHOT_DIR = REPO_ROOT / "docs" / "images"
WWW_DIR = REPO_ROOT / "custom_components" / "meraki_ha" / "www"


# Mock data matching the TypeScript interfaces
MOCK_DATA = {
    "enabled_networks": ["N_12345"],
    "config_entry_id": "mock_config_entry",
    "version": "2.2.0",
    "scan_interval": 300,
    "last_updated": "2025-01-07T12:00:00Z",
    "dashboard_view_mode": "network",
    "dashboard_device_type_filter": "all",
    "dashboard_status_filter": "all",
    "temperature_unit": "celsius",
    "networks": [
        {
            "id": "N_12345",
            "name": "Main Office",
            "productTypes": ["switch", "camera", "wireless", "sensor"],
            "tags": ["production"],
            "is_enabled": True,
            "ssids": [
                {
                    "number": 0,
                    "name": "Corporate WiFi",
                    "enabled": True,
                    "networkId": "N_12345",
                    "entity_id": "switch.corporate_wifi",
                    "visible": True,
                    "authMode": "psk",
                },
                {
                    "number": 1,
                    "name": "Guest Network",
                    "enabled": True,
                    "networkId": "N_12345",
                    "entity_id": "switch.guest_network",
                    "visible": True,
                    "authMode": "open",
                },
            ],
        }
    ],
    "ssids": [
        {
            "number": 0,
            "name": "Corporate WiFi",
            "enabled": True,
            "networkId": "N_12345",
            "entity_id": "switch.corporate_wifi",
        },
        {
            "number": 1,
            "name": "Guest Network",
            "enabled": True,
            "networkId": "N_12345",
            "entity_id": "switch.guest_network",
        },
    ],
    "devices": [
        {
            "serial": "Q234-ABCD-SW1",
            "name": "Office Switch 1",
            "model": "MS225-24P",
            "networkId": "N_12345",
            "productType": "switch",
            "status": "online",
            "firmware": "switch-15-21",
            "lanIp": "192.168.1.2",
            "mac": "00:11:22:33:44:55",
            "entity_id": "switch.office_switch_1",
            "ports_statuses": [
                {
                    "portId": "1",
                    "status": "Connected",
                    "enabled": True,
                    "speed": "1 Gbps",
                    "duplex": "full",
                    "usageInKb": {"total": 2456000, "sent": 1200000, "recv": 1256000},
                    "trafficInKbps": {"total": 45000, "sent": 22000, "recv": 23000},
                    "poe": {"isAllocated": True, "enabled": True},
                    "powerUsageInWh": 12.5,
                    "clientName": "John's MacBook Pro",
                    "clientMac": "a4:83:e7:12:34:56",
                    "clientCount": 1,
                    "vlan": 100,
                    "lldp": {
                        "systemName": "Johns-MacBook-Pro",
                        "portId": "en0",
                        "managementAddress": "192.168.1.101",
                    },
                },
                {
                    "portId": "2",
                    "status": "Connected",
                    "enabled": True,
                    "speed": "1 Gbps",
                    "duplex": "full",
                    "usageInKb": {"total": 890000},
                    "trafficInKbps": {"total": 12000},
                    "poe": {"isAllocated": True, "enabled": True},
                    "powerUsageInWh": 8.2,
                    "clientName": "Conference Room Phone",
                    "clientMac": "00:50:56:ab:cd:ef",
                    "clientCount": 1,
                    "vlan": 200,
                },
                {
                    "portId": "3",
                    "status": "Connected",
                    "enabled": True,
                    "speed": "100 Mbps",
                    "duplex": "full",
                    "usageInKb": {"total": 45000},
                    "poe": {"isAllocated": False},
                    "powerUsageInWh": 0,
                    "clientName": "Printer-HP",
                    "clientMac": "b8:27:eb:12:34:56",
                    "clientCount": 1,
                    "vlan": 100,
                },
                {
                    "portId": "4",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"isAllocated": False},
                },
                {
                    "portId": "5",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"isAllocated": False},
                },
                {
                    "portId": "6",
                    "status": "Connected",
                    "enabled": True,
                    "speed": "1 Gbps",
                    "duplex": "full",
                    "usageInKb": {"total": 1200000},
                    "poe": {"isAllocated": True, "enabled": True},
                    "powerUsageInWh": 15.3,
                    "clientName": "Lobby AP",
                    "clientMac": "00:11:22:33:44:57",
                    "clientCount": 1,
                    "vlan": 1,
                    "cdp": {
                        "deviceId": "MR46-Lobby",
                        "platform": "Meraki MR46",
                        "portId": "Port 0",
                        "managementAddress": "192.168.1.10",
                    },
                },
                {
                    "portId": "7",
                    "status": "Disconnected",
                    "enabled": True,
                    "poe": {"isAllocated": False},
                },
                {
                    "portId": "8",
                    "status": "Connected",
                    "enabled": True,
                    "speed": "1 Gbps",
                    "duplex": "full",
                    "usageInKb": {"total": 3400000},
                    "poe": {"isAllocated": False},
                    "clientName": "NAS Storage",
                    "clientMac": "d8:3b:bf:aa:bb:cc",
                    "clientCount": 1,
                    "vlan": 100,
                },
            ],
        },
        {
            "serial": "Q234-ABCD-CAM1",
            "name": "Front Door Camera",
            "model": "MV12WE",
            "networkId": "N_12345",
            "productType": "camera",
            "status": "online",
            "firmware": "camera-4-18",
            "lanIp": "192.168.1.50",
            "mac": "00:11:22:33:44:56",
            "entity_id": "camera.front_door_camera",
        },
        {
            "serial": "Q234-ABCD-AP1",
            "name": "Lobby AP",
            "model": "MR46",
            "networkId": "N_12345",
            "productType": "wireless",
            "status": "online",
            "firmware": "wireless-29-5",
            "lanIp": "192.168.1.10",
            "mac": "00:11:22:33:44:57",
            "entity_id": "update.lobby_ap_firmware",
            "basicServiceSets": [
                {
                    "ssidName": "Corporate WiFi",
                    "ssidNumber": 0,
                    "enabled": True,
                    "band": "2.4 GHz",
                    "bssid": "00:11:22:33:44:58",
                    "channel": 6,
                    "channelWidth": "20 MHz",
                    "power": "17 dBm",
                    "visible": True,
                    "broadcasting": True,
                },
                {
                    "ssidName": "Corporate WiFi",
                    "ssidNumber": 0,
                    "enabled": True,
                    "band": "5 GHz",
                    "bssid": "00:11:22:33:44:59",
                    "channel": 36,
                    "channelWidth": "80 MHz",
                    "power": "19 dBm",
                    "visible": True,
                    "broadcasting": True,
                },
                {
                    "ssidName": "Guest Network",
                    "ssidNumber": 1,
                    "enabled": True,
                    "band": "2.4 GHz",
                    "bssid": "00:11:22:33:44:5a",
                    "channel": 6,
                    "channelWidth": "20 MHz",
                    "power": "14 dBm",
                    "visible": True,
                    "broadcasting": True,
                },
            ],
        },
        {
            "serial": "Q234-ABCD-MT1",
            "name": "Server Room Sensor",
            "model": "MT10",
            "networkId": "N_12345",
            "productType": "sensor",
            "status": "online",
            "firmware": "sensor-1-12",
            "lanIp": None,
            "mac": "00:11:22:33:44:58",
            "entity_id": "sensor.server_room_temperature",
            "readings": {
                "temperature": 21.5,
                "humidity": 45,
                "battery": 98,
            },
        },
    ],
    "clients": [
        {
            "id": "k12345",
            "mac": "a4:83:e7:12:34:56",
            "description": "John's MacBook Pro",
            "ip": "192.168.1.101",
            "manufacturer": "Apple",
            "os": "macOS",
            "status": "Online",
            "recentDeviceSerial": "Q234-ABCD-SW1",
            "recentDeviceName": "Office Switch 1",
            "switchport": "1",
            "vlan": 100,
            "usage": {"sent": 1256000000, "recv": 2456000000},
            "firstSeen": "2024-12-01T08:00:00Z",
            "lastSeen": "2025-01-07T12:00:00Z",
        },
        {
            "id": "k12346",
            "mac": "00:50:56:ab:cd:ef",
            "description": "Conference Room Phone",
            "ip": "192.168.1.102",
            "manufacturer": "Cisco",
            "os": None,
            "status": "Online",
            "recentDeviceSerial": "Q234-ABCD-SW1",
            "recentDeviceName": "Office Switch 1",
            "switchport": "2",
            "vlan": 200,
            "usage": {"sent": 45000000, "recv": 89000000},
        },
        {
            "id": "k12347",
            "mac": "b8:27:eb:12:34:56",
            "description": "Printer-HP",
            "ip": "192.168.1.103",
            "manufacturer": "HP Inc",
            "status": "Online",
            "recentDeviceSerial": "Q234-ABCD-SW1",
            "recentDeviceName": "Office Switch 1",
            "switchport": "3",
            "vlan": 100,
            "usage": {"sent": 12000000, "recv": 45000000},
        },
        {
            "id": "k12348",
            "mac": "f0:18:98:aa:bb:cc",
            "description": "Sarah's iPhone",
            "ip": "192.168.1.150",
            "manufacturer": "Apple",
            "os": "iOS",
            "status": "Online",
            "recentDeviceSerial": "Q234-ABCD-AP1",
            "recentDeviceName": "Lobby AP",
            "ssid": "Corporate WiFi",
            "vlan": 100,
            "usage": {"sent": 234000000, "recv": 567000000},
        },
        {
            "id": "k12349",
            "mac": "dc:a6:32:11:22:33",
            "description": "Guest Laptop",
            "ip": "192.168.10.5",
            "manufacturer": "Dell",
            "os": "Windows",
            "status": "Online",
            "recentDeviceSerial": "Q234-ABCD-AP1",
            "recentDeviceName": "Lobby AP",
            "ssid": "Guest Network",
            "vlan": 10,
            "usage": {"sent": 78000000, "recv": 123000000},
        },
    ],
}


class ReuseAddrTCPServer(socketserver.TCPServer):
    """TCPServer that allows address reuse."""

    allow_reuse_address = True


def create_screenshot_html() -> str:
    """Create an HTML wrapper that loads the panel with mock data."""
    mock_data_json = json.dumps(MOCK_DATA)

    return f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Meraki Panel Screenshot</title>
                <style>
        :root {{
            --primary-color: #03a9f4;
            --primary-text-color: #212121;
            --secondary-text-color: #727272;
            --primary-background-color: #fafafa;
            --secondary-background-color: #e0e0e0;
            --divider-color: #e0e0e0;
            --accent-color: #ff9800;
            --error-color: #f44336;
            --success-color: #4caf50;
            --warning-color: #ff9800;
            --card-background-color: #ffffff;
            --ha-card-border-radius: 8px;
        }}
        body {{
            font-family: Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 16px;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            min-height: 100vh;
        }}
        meraki-panel {{
            display: block;
        }}
                </style>
            </head>
            <body>
    <meraki-panel id="panel"></meraki-panel>
    <script type="module" src="/meraki-panel.js"></script>
    <script>
        // Wait for the custom element to be defined
        customElements.whenDefined('meraki-panel').then(() => {{
            const panel = document.getElementById('panel');

            // Create a mock hass object
            const mockHass = {{
                callWS: async (params) => {{
                    console.log('Mock callWS called with:', params);
                    if (params.type === 'meraki_ha/get_config') {{
                        return {mock_data_json};
                    }}
                    return {{}};
                }},
                states: {{}},
                services: {{}},
                user: {{ name: 'Demo User' }},
                themes: {{ darkMode: true }},
                language: 'en',
            }};

            // Create mock panel config
            const mockPanel = {{
                config: {{
                    config_entry_id: 'mock_config_entry',
                }},
            }};

            // Set properties on the panel
            panel.hass = mockHass;
            panel.panel = mockPanel;
            panel.narrow = false;
            panel.route = {{ path: '/', prefix: '/meraki' }};

            // Signal that panel is ready
            window.__PANEL_READY__ = true;
            console.log('Panel initialized with mock data');
        }});
    </script>
            </body>
            </html>
"""


def build_frontend() -> bool:
    """Build the React frontend if needed."""
    panel_js = WWW_DIR / "meraki-panel.js"

    # Check if we need to build
    if panel_js.exists():
        # Check if source is newer than build
        src_dir = WWW_DIR / "src"
        if src_dir.exists():
            src_mtime = max(
                f.stat().st_mtime for f in src_dir.rglob("*") if f.is_file()
            )
            if panel_js.stat().st_mtime >= src_mtime:
                print("Frontend is up to date, skipping build")
                return True

    print("Building frontend...")
    try:
        # Check if node_modules exists
        node_modules = WWW_DIR / "node_modules"
        if not node_modules.exists():
            print("Installing npm dependencies...")
            subprocess.run(
                ["npm", "ci"],
                cwd=WWW_DIR,
                check=True,
                capture_output=True,
            )

        # Build the frontend
        subprocess.run(
            ["npm", "run", "build"],
            cwd=WWW_DIR,
            check=True,
            capture_output=True,
            text=True,
        )
        print("Frontend build complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Frontend build failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("npm not found. Please install Node.js")
        return False


def run_server(port: int, directory: Path) -> socketserver.TCPServer:
    """Start a simple HTTP server."""
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    httpd = ReuseAddrTCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def generate_screenshots() -> None:
    """Generate screenshots using Playwright."""
    # Ensure screenshot directory exists
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # Build frontend
    if not build_frontend():
        print("Failed to build frontend, exiting")
        sys.exit(1)

    # Create the screenshot HTML wrapper
    html_path = WWW_DIR / "screenshot.html"
    html_path.write_text(create_screenshot_html())

    # Start the server
    print(f"Starting server on port {TEST_PORT}...")
    server = run_server(TEST_PORT, WWW_DIR)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()

            # Screenshot 1: Dashboard View
            print("Capturing Dashboard view...")
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto(f"http://localhost:{TEST_PORT}/screenshot.html")

            # Wait for panel to be ready
            page.wait_for_function("window.__PANEL_READY__ === true", timeout=30000)
            page.wait_for_timeout(2000)  # Allow rendering

            page.screenshot(path=str(SCREENSHOT_DIR / "dashboard_view.png"))
            print(f"  Saved: {SCREENSHOT_DIR / 'dashboard_view.png'}")

            # Screenshot 2: Switch Detail View
            print("Capturing Switch detail view...")
            # Click on the switch device to open detail view
            page.click("text=Office Switch 1")
            page.wait_for_timeout(1500)
            page.set_viewport_size({"width": 1280, "height": 1100})
            page.screenshot(path=str(SCREENSHOT_DIR / "switch_detail_view.png"))
            print(f"  Saved: {SCREENSHOT_DIR / 'switch_detail_view.png'}")

            # Click on first port to show port details
            page.click(".port.connected >> nth=0")
            page.wait_for_timeout(500)
            page.screenshot(path=str(SCREENSHOT_DIR / "switch_detail_view.png"))
            print(
                f"  Updated: {SCREENSHOT_DIR / 'switch_detail_view.png'} (with port details)"
            )

            # Screenshot 3: Sensor Detail View
            print("Capturing Sensor detail view...")
            # Go back to dashboard
            page.click("text=Back to Dashboard")
            page.wait_for_timeout(1000)
            # Click on the sensor device
            page.click("text=Server Room Sensor")
            page.wait_for_timeout(1500)
            page.set_viewport_size({"width": 1100, "height": 900})
            page.screenshot(path=str(SCREENSHOT_DIR / "sensor_detail_view.png"))
            print(f"  Saved: {SCREENSHOT_DIR / 'sensor_detail_view.png'}")

            # Screenshot 4: Clients View
            print("Capturing Clients view...")
            # Go back to dashboard
            page.click("text=Back to Dashboard")
            page.wait_for_timeout(1000)
            # Click on "Connected Clients" stat card
            page.click("text=Connected Clients")
            page.wait_for_timeout(1500)
            page.set_viewport_size({"width": 1280, "height": 900})
            page.screenshot(path=str(SCREENSHOT_DIR / "clients_view.png"))
            print(f"  Saved: {SCREENSHOT_DIR / 'clients_view.png'}")

            browser.close()

            print("\nAll screenshots generated successfully!")
            print(f"Screenshots saved to: {SCREENSHOT_DIR}")

    finally:
        # Cleanup
        server.shutdown()
        if html_path.exists():
            html_path.unlink()


if __name__ == "__main__":
    generate_screenshots()
