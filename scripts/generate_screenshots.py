"""Script to generate screenshots for the README."""
# ruff: noqa: E501

import http.server
import os
import socketserver
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
            "productTypes": ["switch", "camera", "wireless", "sensor"],
            "tags": ["production"],
            "enrollmentString": None,
            "url": "https://dashboard.meraki.com",
            "timeZone": "America/Los_Angeles",
            "is_enabled": True,
            "ssids": [
                {
                    "number": 0,
                    "name": "Corporate WiFi",
                    "enabled": True,
                    "networkId": "N_12345",
                    "entity_id": "switch.corporate_wifi",
                    "psk_entity_id": None,
                    "visible": True,
                    "authMode": "psk",
                },
                {
                    "number": 1,
                    "name": "Guest Network",
                    "enabled": True,
                    "networkId": "N_12345",
                    "entity_id": "switch.guest_network",
                    "psk_entity_id": None,
                    "visible": True,
                    "authMode": "open",
                },
            ],
        }
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
            "ports_statuses": [
                {
                    "portId": "1",
                    "status": "Connected",
                    "enabled": True,
                    "speed": "1 Gbps",
                    "duplex": "full",
                    "usageInKb": {"total": 2456000},
                    "poe": {"isAllocated": True},
                    "powerUsageInWh": 12.5,
                    "clientName": "John's MacBook Pro",
                    "clientMac": "a4:83:e7:12:34:56",
                },
                {
                    "portId": "2",
                    "status": "Connected",
                    "enabled": True,
                    "speed": "1 Gbps",
                    "duplex": "full",
                    "usageInKb": {"total": 890000},
                    "poe": {"isAllocated": True},
                    "powerUsageInWh": 8.2,
                    "clientName": "Conference Room Phone",
                    "clientMac": "00:50:56:ab:cd:ef",
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
                    "poe": {"isAllocated": True},
                    "powerUsageInWh": 15.3,
                    "clientName": "Lobby AP",
                    "clientMac": "00:11:22:33:44:57",
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
                },
            ],
            "entity_id": "switch.office_switch_1",
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
            "rtsp_url": "rtsp://192.168.1.50:9000/live",
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
            "clients": 23,
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
            },
        },
    ],
    "options": MOCK_SETTINGS,
}


class ReuseAddrTCPServer(socketserver.TCPServer):
    """TCPServer that allows address reuse."""

    allow_reuse_address = True


def create_network_view_html() -> str:
    """Create a beautiful network view mockup HTML."""
    return """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
    <title>Meraki Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
                <style>
        :root {
            --primary: #00b4d8;
            --primary-dark: #0096c7;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --card-border: #334155;
            --text: #f1f5f9;
            --text-muted: #94a3b8;
            --radius: 16px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
                    body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            min-height: 100vh;
            color: var(--text);
            padding: 32px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 32px;
        }
        .header .logo {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .header .logo .material-icons-round { font-size: 28px; }
        .header h1 {
            font-size: 28px;
            font-weight: 600;
            background: linear-gradient(90deg, #fff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stats-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius);
            padding: 20px;
        }
        .stat-card .label {
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        .stat-card .value {
            font-size: 32px;
            font-weight: 700;
        }
        .stat-card .value.success { color: var(--success); }
        .stat-card .value.primary { color: var(--primary); }
        .network-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius);
            overflow: hidden;
            margin-bottom: 24px;
        }
        .network-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 24px;
            border-bottom: 1px solid var(--card-border);
            background: linear-gradient(90deg, rgba(0,180,216,0.1) 0%, transparent 100%);
        }
        .network-header .title {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .network-header h2 {
            font-size: 20px;
            font-weight: 600;
        }
        .network-header .badge {
            background: var(--success);
            color: #fff;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        .devices-table {
            width: 100%;
            border-collapse: collapse;
        }
        .devices-table th {
            text-align: left;
            padding: 16px 24px;
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--card-border);
        }
        .devices-table td {
            padding: 16px 24px;
            border-bottom: 1px solid var(--card-border);
            vertical-align: middle;
        }
        .devices-table tr:last-child td { border-bottom: none; }
        .devices-table tr:hover { background: rgba(255,255,255,0.02); }
        .device-name {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .device-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .device-icon.switch { background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%); }
        .device-icon.camera { background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%); }
        .device-icon.wireless { background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); }
        .device-icon.sensor { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
        .device-name span { font-weight: 500; }
        .model { color: var(--text-muted); font-size: 14px; }
        .status {
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 500;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 8px var(--success);
        }
        .status-text { color: var(--success); }
        .clients-badge {
            background: rgba(0,180,216,0.15);
            color: var(--primary);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
        }
        .ssid-section {
            padding: 20px 24px;
            border-top: 1px solid var(--card-border);
        }
        .ssid-section h3 {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .ssid-list {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        .ssid-item {
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .ssid-item .material-icons-round {
            color: var(--primary);
            font-size: 20px;
        }
        .ssid-item .name { font-weight: 500; }
        .ssid-item .clients {
            color: var(--text-muted);
            font-size: 13px;
        }
        .toggle {
            width: 44px;
            height: 24px;
            background: var(--success);
            border-radius: 12px;
            position: relative;
        }
        .toggle::after {
            content: '';
            position: absolute;
            width: 20px;
            height: 20px;
            background: #fff;
            border-radius: 50%;
            top: 2px;
            right: 2px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    }
                </style>
            </head>
            <body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <span class="material-icons-round">router</span>
            </div>
            <h1>Meraki Dashboard</h1>
        </div>

        <div class="stats-row">
            <div class="stat-card">
                <div class="label">Total Devices</div>
                <div class="value primary">4</div>
            </div>
            <div class="stat-card">
                <div class="label">Online</div>
                <div class="value success">4</div>
            </div>
            <div class="stat-card">
                <div class="label">Connected Clients</div>
                <div class="value primary">47</div>
            </div>
            <div class="stat-card">
                <div class="label">Active SSIDs</div>
                <div class="value primary">2</div>
            </div>
        </div>

        <div class="network-card">
            <div class="network-header">
                <div class="title">
                    <span class="material-icons-round" style="color: var(--primary)">lan</span>
                    <h2>Main Office</h2>
                    <span class="badge">4 devices online</span>
                </div>
            </div>

            <table class="devices-table">
                <thead>
                    <tr>
                        <th>Device</th>
                        <th>Model</th>
                        <th>Status</th>
                        <th>IP Address</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <div class="device-name">
                                <div class="device-icon switch">
                                    <span class="material-icons-round">power</span>
                                </div>
                                <span>Office Switch 1</span>
                            </div>
                        </td>
                        <td class="model">MS225-24P</td>
                        <td>
                            <div class="status">
                                <div class="status-dot"></div>
                                <span class="status-text">Online</span>
                            </div>
                        </td>
                        <td class="model">192.168.1.2</td>
                        <td><span class="clients-badge">5 ports active</span></td>
                    </tr>
                    <tr>
                        <td>
                            <div class="device-name">
                                <div class="device-icon camera">
                                    <span class="material-icons-round">videocam</span>
                                </div>
                                <span>Front Door Camera</span>
                            </div>
                        </td>
                        <td class="model">MV12WE</td>
                        <td>
                            <div class="status">
                                <div class="status-dot"></div>
                                <span class="status-text">Online</span>
                            </div>
                        </td>
                        <td class="model">192.168.1.50</td>
                        <td><span class="clients-badge">Recording</span></td>
                    </tr>
                    <tr>
                        <td>
                            <div class="device-name">
                                <div class="device-icon wireless">
                                    <span class="material-icons-round">wifi</span>
                                </div>
                                <span>Lobby AP</span>
                            </div>
                        </td>
                        <td class="model">MR46</td>
                        <td>
                            <div class="status">
                                <div class="status-dot"></div>
                                <span class="status-text">Online</span>
                            </div>
                        </td>
                        <td class="model">192.168.1.10</td>
                        <td><span class="clients-badge">23 clients</span></td>
                    </tr>
                    <tr>
                        <td>
                            <div class="device-name">
                                <div class="device-icon sensor">
                                    <span class="material-icons-round">thermostat</span>
                                </div>
                                <span>Server Room Sensor</span>
                            </div>
                        </td>
                        <td class="model">MT10</td>
                        <td>
                            <div class="status">
                                <div class="status-dot"></div>
                                <span class="status-text">Online</span>
                            </div>
                        </td>
                        <td class="model">—</td>
                        <td><span class="clients-badge">21.5°C / 45%</span></td>
                    </tr>
                </tbody>
            </table>

            <div class="ssid-section">
                <h3>
                    <span class="material-icons-round">wifi</span>
                    Wireless Networks
                </h3>
                <div class="ssid-list">
                    <div class="ssid-item">
                        <span class="material-icons-round">lock</span>
                        <span class="name">Corporate WiFi</span>
                        <span class="clients">32 clients</span>
                        <div class="toggle"></div>
                    </div>
                    <div class="ssid-item">
                        <span class="material-icons-round">public</span>
                        <span class="name">Guest Network</span>
                        <span class="clients">15 clients</span>
                        <div class="toggle"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
            </body>
            </html>
"""


def create_switch_detail_html() -> str:
    """Create a beautiful switch detail view with port visualization."""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Switch Detail</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <style>
        :root {
            --primary: #00b4d8;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --card-border: #334155;
            --text: #f1f5f9;
            --text-muted: #94a3b8;
            --radius: 16px;
            --poe: #f59e0b;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            min-height: 100vh;
            color: var(--text);
            padding: 32px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .back-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--primary);
            font-weight: 500;
            margin-bottom: 24px;
            cursor: pointer;
        }
        .device-header {
            display: flex;
            align-items: flex-start;
            gap: 24px;
            margin-bottom: 32px;
        }
        .device-icon {
            width: 72px;
            height: 72px;
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .device-icon .material-icons-round { font-size: 36px; }
        .device-info h1 { font-size: 28px; font-weight: 600; margin-bottom: 8px; }
        .device-info .meta {
            display: flex;
            gap: 24px;
            color: var(--text-muted);
            font-size: 14px;
        }
        .device-info .meta span {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16,185,129,0.15);
            color: var(--success);
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 500;
            font-size: 14px;
        }
        .status-badge .dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
        }
        .cards-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius);
            padding: 24px;
        }
        .card h3 {
            font-size: 14px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        .info-item .label {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }
        .info-item .value {
            font-size: 16px;
            font-weight: 500;
        }
        .switch-visual {
            background: #0f172a;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .switch-chassis {
            background: linear-gradient(180deg, #374151 0%, #1f2937 100%);
            border-radius: 8px;
            padding: 16px 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            border: 2px solid #4b5563;
        }
        .switch-label {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: #9ca3af;
        }
        .ports-row {
            display: flex;
            gap: 6px;
        }
        .port {
            width: 40px;
            height: 32px;
            background: #111827;
            border-radius: 4px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            position: relative;
            border: 2px solid #374151;
            transition: all 0.2s;
        }
        .port:hover {
            transform: translateY(-2px);
            border-color: var(--primary);
        }
        .port.connected {
            background: rgba(16,185,129,0.2);
            border-color: var(--success);
        }
        .port.connected::before {
            content: '';
            width: 6px;
            height: 6px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 6px var(--success);
        }
        .port .num {
            font-size: 9px;
            color: #6b7280;
            position: absolute;
            bottom: 2px;
        }
        .port .poe {
            position: absolute;
            top: -8px;
            right: -4px;
            font-size: 12px;
            color: var(--poe);
            text-shadow: 0 0 4px var(--poe);
        }
        .port-details {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius);
            padding: 20px;
        }
        .port-details h4 {
            font-size: 16px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .port-details .client-info {
            background: rgba(0,180,216,0.1);
            border-radius: 8px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .client-avatar {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .client-details .name { font-weight: 600; margin-bottom: 4px; }
        .client-details .mac { font-size: 13px; color: var(--text-muted); font-family: monospace; }
        .port-stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 16px;
        }
        .port-stat .label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; }
        .port-stat .value { font-size: 18px; font-weight: 600; color: var(--primary); }
        .legend {
            display: flex;
            gap: 24px;
            margin-top: 16px;
            font-size: 13px;
            color: var(--text-muted);
        }
        .legend span {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .legend .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }
        .legend .dot.connected { background: var(--success); }
        .legend .dot.disconnected { background: #374151; }
    </style>
</head>
<body>
    <div class="container">
        <div class="back-btn">
            <span class="material-icons-round">arrow_back</span>
            Back to Dashboard
        </div>

        <div class="device-header">
            <div class="device-icon">
                <span class="material-icons-round">power</span>
            </div>
            <div class="device-info">
                <h1>Office Switch 1</h1>
                <div class="meta">
                    <span><strong>Model:</strong> MS225-24P</span>
                    <span><strong>Serial:</strong> Q234-ABCD-SW1</span>
                    <span><strong>Firmware:</strong> switch-15-21</span>
                </div>
            </div>
            <div class="status-badge">
                <div class="dot"></div>
                Online
            </div>
        </div>

        <div class="cards-grid">
            <div class="card">
                <h3><span class="material-icons-round">info</span> Device Information</h3>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="label">LAN IP</div>
                        <div class="value">192.168.1.2</div>
                    </div>
                    <div class="info-item">
                        <div class="label">MAC Address</div>
                        <div class="value" style="font-family: monospace;">00:11:22:33:44:55</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Uptime</div>
                        <div class="value">14 days, 6 hours</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Last Seen</div>
                        <div class="value">Just now</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <h3><span class="material-icons-round">bolt</span> Power Summary</h3>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="label">Total PoE Power</div>
                        <div class="value" style="color: var(--poe);">36.0 W</div>
                    </div>
                    <div class="info-item">
                        <div class="label">PoE Budget</div>
                        <div class="value">370 W</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Active PoE Ports</div>
                        <div class="value">3 of 24</div>
                    </div>
                    <div class="info-item">
                        <div class="label">Utilization</div>
                        <div class="value" style="color: var(--success);">9.7%</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <h3><span class="material-icons-round">settings_ethernet</span> Port Status</h3>
            <div class="switch-visual">
                <div class="switch-chassis">
                    <div class="switch-label">
                        <span>Cisco Meraki MS225-24P</span>
                        <span>Ports 1-8</span>
                    </div>
                    <div class="ports-row">
                        <div class="port connected"><span class="num">1</span><span class="poe">⚡</span></div>
                        <div class="port connected"><span class="num">2</span><span class="poe">⚡</span></div>
                        <div class="port connected"><span class="num">3</span></div>
                        <div class="port"><span class="num">4</span></div>
                        <div class="port"><span class="num">5</span></div>
                        <div class="port connected"><span class="num">6</span><span class="poe">⚡</span></div>
                        <div class="port"><span class="num">7</span></div>
                        <div class="port connected"><span class="num">8</span></div>
                    </div>
                </div>
                <div class="legend">
                    <span><div class="dot connected"></div> Connected</span>
                    <span><div class="dot disconnected"></div> Disconnected</span>
                    <span>⚡ PoE Active</span>
                </div>
            </div>

            <div class="port-details">
                <h4>
                    <span class="material-icons-round" style="color: var(--success);">cable</span>
                    Port 1 - Connected
                </h4>
                <div class="client-info">
                    <div class="client-avatar">
                        <span class="material-icons-round">laptop_mac</span>
                    </div>
                    <div class="client-details">
                        <div class="name">John's MacBook Pro</div>
                        <div class="mac">a4:83:e7:12:34:56</div>
                    </div>
                </div>
                <div class="port-stats">
                    <div class="port-stat">
                        <div class="label">Speed</div>
                        <div class="value">1 Gbps</div>
                    </div>
                    <div class="port-stat">
                        <div class="label">Traffic</div>
                        <div class="value">2.4 GB</div>
                    </div>
                    <div class="port-stat">
                        <div class="label">PoE Power</div>
                        <div class="value" style="color: var(--poe);">12.5 W</div>
                    </div>
                    <div class="port-stat">
                        <div class="label">VLAN</div>
                        <div class="value">100</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""


def create_sensor_detail_html() -> str:
    """Create a beautiful sensor detail view with readings."""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Sensor Detail</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
                        <style>
        :root {
            --primary: #00b4d8;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --card-border: #334155;
            --text: #f1f5f9;
            --text-muted: #94a3b8;
            --radius: 16px;
            --temp: #f97316;
            --humidity: #06b6d4;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            min-height: 100vh;
            color: var(--text);
            padding: 32px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .back-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--primary);
            font-weight: 500;
            margin-bottom: 24px;
            cursor: pointer;
        }
        .device-header {
            display: flex;
            align-items: flex-start;
            gap: 24px;
            margin-bottom: 32px;
        }
        .device-icon {
            width: 72px;
            height: 72px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .device-icon .material-icons-round { font-size: 36px; }
        .device-info h1 { font-size: 28px; font-weight: 600; margin-bottom: 8px; }
        .device-info .meta {
            display: flex;
            gap: 24px;
            color: var(--text-muted);
            font-size: 14px;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16,185,129,0.15);
            color: var(--success);
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 500;
            font-size: 14px;
        }
        .status-badge .dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
        }
        .readings-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }
        .reading-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius);
            padding: 32px;
            text-align: center;
        }
        .reading-card .icon-wrapper {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
        }
        .reading-card.temp .icon-wrapper {
            background: rgba(249, 115, 22, 0.15);
        }
        .reading-card.humidity .icon-wrapper {
            background: rgba(6, 182, 212, 0.15);
        }
        .reading-card .icon-wrapper .material-icons-round {
            font-size: 40px;
        }
        .reading-card.temp .icon-wrapper .material-icons-round { color: var(--temp); }
        .reading-card.humidity .icon-wrapper .material-icons-round { color: var(--humidity); }
        .reading-card .label {
            font-size: 14px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        .reading-card .value {
            font-size: 56px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 8px;
        }
        .reading-card.temp .value { color: var(--temp); }
        .reading-card.humidity .value { color: var(--humidity); }
        .reading-card .unit {
                                font-size: 24px;
            font-weight: 400;
            opacity: 0.7;
        }
        .reading-card .status {
            font-size: 14px;
            color: var(--success);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            margin-top: 16px;
        }
        .gauge-wrapper {
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            margin-top: 20px;
            overflow: hidden;
        }
        .gauge-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .reading-card.temp .gauge-fill {
            background: linear-gradient(90deg, #22c55e 0%, #eab308 50%, #ef4444 100%);
            width: 43%;
        }
        .reading-card.humidity .gauge-fill {
            background: var(--humidity);
            width: 45%;
        }
        .gauge-labels {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 6px;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: var(--radius);
            padding: 24px;
        }
        .card h3 {
            font-size: 14px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 24px;
        }
        .info-item .label {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }
        .info-item .value {
            font-size: 16px;
            font-weight: 500;
        }
        .history-note {
            margin-top: 24px;
            padding: 16px;
            background: rgba(0,180,216,0.1);
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
            color: var(--text-muted);
        }
        .history-note .material-icons-round { color: var(--primary); }
                        </style>
</head>
<body>
    <div class="container">
        <div class="back-btn">
            <span class="material-icons-round">arrow_back</span>
            Back to Dashboard
        </div>

        <div class="device-header">
            <div class="device-icon">
                <span class="material-icons-round">thermostat</span>
            </div>
            <div class="device-info">
                <h1>Server Room Sensor</h1>
                <div class="meta">
                    <span><strong>Model:</strong> MT10</span>
                    <span><strong>Serial:</strong> Q234-ABCD-MT1</span>
                    <span><strong>Firmware:</strong> sensor-1-12</span>
                </div>
            </div>
            <div class="status-badge">
                <div class="dot"></div>
                Online
            </div>
        </div>

        <div class="readings-grid">
            <div class="reading-card temp">
                <div class="icon-wrapper">
                    <span class="material-icons-round">thermostat</span>
                </div>
                <div class="label">Temperature</div>
                <div class="value">21.5<span class="unit">°C</span></div>
                <div class="status">
                    <span class="material-icons-round" style="font-size: 16px;">check_circle</span>
                    Within normal range
                </div>
                <div class="gauge-wrapper">
                    <div class="gauge-fill"></div>
                </div>
                <div class="gauge-labels">
                    <span>0°C</span>
                    <span>25°C</span>
                    <span>50°C</span>
                </div>
            </div>

            <div class="reading-card humidity">
                <div class="icon-wrapper">
                    <span class="material-icons-round">water_drop</span>
                </div>
                <div class="label">Humidity</div>
                <div class="value">45<span class="unit">%</span></div>
                <div class="status">
                    <span class="material-icons-round" style="font-size: 16px;">check_circle</span>
                    Optimal humidity
                </div>
                <div class="gauge-wrapper">
                    <div class="gauge-fill"></div>
                </div>
                <div class="gauge-labels">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                </div>
            </div>
        </div>

        <div class="card">
            <h3><span class="material-icons-round">info</span> Device Information</h3>
            <div class="info-grid">
                <div class="info-item">
                    <div class="label">Battery</div>
                    <div class="value" style="color: var(--success);">98%</div>
                </div>
                <div class="info-item">
                    <div class="label">Last Update</div>
                    <div class="value">2 min ago</div>
                </div>
                <div class="info-item">
                    <div class="label">Network</div>
                    <div class="value">Main Office</div>
                </div>
                <div class="info-item">
                    <div class="label">Uptime</div>
                    <div class="value">45 days</div>
                </div>
            </div>
            <div class="history-note">
                <span class="material-icons-round">show_chart</span>
                Historical data available in Home Assistant's history panel
            </div>
        </div>
    </div>
</body>
</html>
"""


def run_server() -> None:
    """Run a simple HTTP server to serve the frontend."""
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=WWW_DIR)
    httpd = ReuseAddrTCPServer(("", TEST_PORT), handler)
    try:
        httpd.serve_forever()
    except OSError:
        pass  # Handle case where port is already in use or server shuts down

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=WWW_DIR)
    httpd = ReuseAddrTCPServer(("", TEST_PORT), handler)
    try:
        httpd.serve_forever()
    except OSError:
        pass  # Handle case where port is already in use or server shuts down


def generate_screenshots() -> None:
    """Generate beautiful mockup screenshots using Playwright."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # Generate Network View Screenshot
        network_html_path = os.path.join(WWW_DIR, "screenshot_network.html")
        with open(network_html_path, "w") as f:
            f.write(create_network_view_html())

        page.goto(f"file://{network_html_path}")
        page.wait_for_timeout(1500)  # Wait for fonts to load

        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "network_view.png"))
        print(f"Saved {os.path.join(SCREENSHOT_DIR, 'network_view.png')}")
        os.remove(network_html_path)

        # Generate Switch Detail View Screenshot
        switch_html_path = os.path.join(WWW_DIR, "screenshot_switch.html")
        with open(switch_html_path, "w") as f:
            f.write(create_switch_detail_html())

        page.set_viewport_size({"width": 1280, "height": 1100})
        page.goto(f"file://{switch_html_path}")
        page.wait_for_timeout(1500)

        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "switch_detail_view.png"))
        print(f"Saved {os.path.join(SCREENSHOT_DIR, 'switch_detail_view.png')}")
        os.remove(switch_html_path)

        # Generate Sensor Detail View Screenshot
        sensor_html_path = os.path.join(WWW_DIR, "screenshot_sensor.html")
        with open(sensor_html_path, "w") as f:
            f.write(create_sensor_detail_html())

        page.set_viewport_size({"width": 1100, "height": 900})
        page.goto(f"file://{sensor_html_path}")
        page.wait_for_timeout(1500)

        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "sensor_detail_view.png"))
        print(f"Saved {os.path.join(SCREENSHOT_DIR, 'sensor_detail_view.png')}")
        os.remove(sensor_html_path)

        browser.close()


if __name__ == "__main__":
    try:
        generate_screenshots()
    finally:
        index_path = os.path.join(WWW_DIR, "screenshot_index.html")
        if os.path.exists(index_path):
            os.remove(index_path)
