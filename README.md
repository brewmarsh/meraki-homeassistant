[![Beta CI](https://github.com/liptonj/meraki-homeassistant/actions/workflows/beta-ci.yaml/badge.svg)](https://github.com/liptonj/meraki-homeassistant/actions/workflows/beta-ci.yaml)
[![Main CI](https://github.com/liptonj/meraki-homeassistant/actions/workflows/main-ci.yaml/badge.svg)](https://github.com/liptonj/meraki-homeassistant/actions/workflows/main-ci.yaml)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)]()
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

# Meraki Home Assistant Integration 🤖

This Home Assistant integration allows you to monitor and manage your Cisco Meraki network, including devices, networks, and SSIDs. It leverages the Meraki API to bring data from your Meraki dashboard into Home Assistant, enabling you to gain insights into your network and automate actions based on its status.

## Table of Contents
- [Key Features](#key-features-)
- [Installation](#installation-️)
- [Configuration](#configuration-⚙️)
- [Web UI](#web-ui-)
- [Services & Controls](#services--controls-)
  - [Parental Controls (Client Blocking)](#parental-controls-client-blocking)
  - [Content Filtering](#content-filtering)
  - [SSID Control](#ssid-control)
- [Entities](#entities-)
  - [Device & Entity Model](#device--entity-model)
  - [Organization-Wide Sensors](#organization-wide-sensors)
  - [Camera Entities & Sensors](#camera-entities--sensors)
  - [Physical Device Sensors](#physical-device-sensors)
  - [Network Sensors](#network-sensors)
  - [VLAN Sensors](#vlan-sensors)
  - [Appliance Port Sensors](#appliance-port-sensors)
  - [SSID Sensors](#ssid-sensors)
  - [Environmental Sensors (MT Series)](#environmental-sensors-mt-series)
- [Automation Examples](#automation-examples-)
- [Troubleshooting](#troubleshooting-)
- [How to Contribute](#how-to-contribute-)
- [Known Issues & Limitations](#known-issues--limitations-️)
- [Disclaimer](#disclaimer-)

## Screenshots 📸

| Network View | Device Detail View |
| :---: | :---: |
| ![Network View](https://user-images.githubusercontent.com/1099616/279869151-24702f37-646d-4176-963d-2103f6f3630d.png) | ![Device Detail View](https://user-images.githubusercontent.com/1099616/279869158-2947a195-5c02-4580-b7a4-315111956f46.png) |

## Key Features ✨

- **Comprehensive Monitoring:** Keep tabs on all your Meraki hardware, including Wireless Access Points (MR/GR), Switches (MS/GS), Security Appliances (MX), Cameras (MV), and Environmental Sensors (MT).
- **Powerful Controls:** Enable/disable SSIDs, block specific clients (Parental Controls), and manage content filtering categories directly from Home Assistant.
- **Web Interface:** A dedicated web UI for advanced features like guest Wi-Fi management and viewing event logs.
- **Rich Sensor Data:** Creates a wide array of sensors for device status, client counts, data usage, firmware updates, PoE consumption, and much more.
- **Camera Integration:** View live RTSP streams from your Meraki cameras within Home Assistant.
- **Device & Entity Model:** The integration represents different aspects of your Meraki setup as devices within Home Assistant to create a logical hierarchy.
- **Organization-Wide Sensors:** These sensors provide aggregate client counts across your entire Meraki organization and are linked to the Organization device.
- **Physical Device Sensors:** These sensors are linked to specific physical Meraki hardware devices.
- **Network Sensors:** These sensors are linked to Meraki Network "devices" in Home Assistant.
- **VLAN Sensors:** For each VLAN configured in a network, sensors are created to monitor its status.
- **Appliance Port Sensors:** For each port on a Meraki MX security appliance, a sensor is created to monitor its status.
- **SSID Sensors:** A variety of sensors are created for each SSID, including client count, bandwidth limits, and more.
- **Environmental Sensors (MT Series):** For each Meraki environmental sensor (MT series), entities are created to monitor real-time conditions.

## Troubleshooting

If you encounter issues with the integration, please check the following:

- **API Key and Organization ID:** Ensure that your API key and organization ID are correct.
- **API Access:** Make sure that API access is enabled in your Meraki dashboard.
- **Home Assistant Logs:** Check the Home Assistant logs for any error messages related to the integration.
- **Restart Home Assistant:** If you've made any changes to the integration's configuration, restart Home Assistant to apply them.

If you're still having trouble, please open an issue on the GitHub repository.

## Installation 🛠️

### Prerequisites

- Home Assistant installation (ensure you are on a compatible version).
- A Cisco Meraki account with API access enabled.
- Your Meraki API key.
- Your Meraki Organization ID.

### Installation Steps

1. **Ensure HACS is installed:** If you haven't already, install the [Home Assistant Community Store (HACS)](https://hacs.xyz/).
2. **Add Custom Repository:**
    - In HACS, go to "Integrations".
    - Click the three dots in the top right and select "Custom repositories".
    - In the "Repository" field, enter the URL of this custom integration's GitHub repository.
    - For "Category", select "Integration".
    - Click "Add".
3. **Install Integration:**
    - Search for "Meraki" or the name of this integration in HACS.
    - Click "Install" and follow the prompts.
4. **Restart Home Assistant:** After installation, restart your Home Assistant instance to load the integration.

## Configuration ⚙️

### Obtaining Meraki API Credentials

To use this integration, you will need a Meraki API key and your Organization ID.

1.  **Log in to the Meraki Dashboard:** Go to [https://dashboard.meraki.com/](https://dashboard.meraki.com/).
2.  **Enable API Access:**
    * Navigate to **Organization** > **Settings**.
    * Under the **Dashboard API access** section, ensure API access is enabled.
3.  **Generate API Key:**
    * Go to your **Profile** (click your name/email in the top right) > **My profile**.
    * Scroll down to the **API access** section.
    * Click **Generate new API key**.
    * **Important:** Copy the generated API key and store it securely. You will not be able to see it again after navigating away from this page.
4.  **Find Organization ID:**
    * **Easiest Method:** The Organization ID is displayed at the bottom of every page in the Meraki dashboard.
    * **Alternative Method (API):** You can find it by making a simple API call to the `/organizations` endpoint with your API key.
    ```bash
    curl -L -H 'X-Cisco-Meraki-API-Key: <your_api_key>' -H 'Content-Type: application/json' '[https://api.meraki.com/api/v1/organizations](https://api.meraki.com/api/v1/organizations)'
    ```

### Setting up the Integration

1.  Navigate to **Settings** > **Devices & Services** in your Home Assistant UI.
2.  Click the **+ ADD INTEGRATION** button in the bottom right.
3.  Search for "Meraki" and select it.
4.  Follow the on-screen prompts to enter your API Key and Organization ID.

### Configuration Options

The following options can be configured when you first set up the integration, or at any time by navigating to the integration's card in **Settings -> Devices & Services** and clicking **Configure**.

* **Scan Interval:** How often (in seconds) to poll the Meraki API for updates. Default: 300.
* **Enable Device Tracker:** Whether to enable the device tracker entity for clients. Default: true.
* **Enable VLAN Management:** Whether to enable VLAN management entities. Default: false.
* **Ignored Networks:** A comma-separated list of network IDs to ignore.

## Web UI 🖼️

This integration provides a custom panel to display a dashboard of your Meraki network. The panel is automatically added to your Home Assistant sidebar when you install the integration.

The Web UI provides a comprehensive overview of your Meraki network, including:

- **Network Summary:** A list of all your networks, with a summary of the devices in each.
- **Device Details:** A detailed view of each device, including its status, configuration, and connected clients.
- **Client Details:** A list of all the clients on your network, with the ability to block or unblock them.
- **Event Log:** A log of all the events on your network, including device connectivity, client activity, and configuration changes.

## Services & Controls 🎛️

This integration provides several ways to control your Meraki network directly from Home Assistant.

### 📶 Wireless (MR)
Control your Wi-Fi experience.
*   **SSID Management:** Toggle SSIDs on or off dynamically.
*   **Client Counts:** See how many devices are connected to each network in real-time.

### 🛡️ Gateways (MX)
*   **Uplink Status:** Monitor your internet connection health and failover status.

## 🖥️ The Dashboard

We've built a custom **Meraki Panel** right into Home Assistant. It gives you a bird's-eye view of your organization without needing to clutter your standard Lovelace dashboard with hundreds of entities.

![Network View](docs/images/network_view.png)
*The Network View provides a quick summary of all your sites.*

![Device Detail](docs/images/device_detail_view.png)
*Drill down into specific devices for detailed controls and metrics.*

## 🚀 Getting Started

1.  **Install:** Use HACS (recommended) to install "Meraki Home Assistant". Alternatively, copy the `custom_components/meraki_ha` folder to your HA `custom_components` directory.
2.  **Configure:** Go to **Settings > Devices & Services > Add Integration** and search for "Meraki".
3.  **API Key:** Enter your Meraki Dashboard API Key. The integration will discover your organizations.
4.  **Enjoy:** Check out the new "Meraki" panel in your sidebar!

## 🤝 Contributing

We love contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) and [DEVELOPMENT.md](DEVELOPMENT.md) guides to get started.

---
*Built with ❤️ by the Open Source Community.*
