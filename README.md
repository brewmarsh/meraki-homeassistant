[![Beta Python Linting](https://github.com/brewmarsh/meraki-homeassistant/actions/workflows/beta-validation.yaml/badge.svg)](https://github.com/brewmarsh/meraki-homeassistant/actions/workflows/beta-validation.yaml)
[![codecov](https://codecov.io/gh/brewmarsh/meraki-homeassistant/branch/main/graph/badge.svg)](https://codecov.io/gh/brewmarsh/meraki-homeassistant)
[![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)]()
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

## Key Features ✨

- **Comprehensive Monitoring:** Keep tabs on all your Meraki hardware, including Wireless Access Points (MR/GR), Switches (MS/GS), Security Appliances (MX), Cameras (MV), and Environmental Sensors (MT).
- **Powerful Controls:** Enable/disable SSIDs, block specific clients (Parental Controls), and manage content filtering categories directly from Home Assistant.
- **Web Interface:** A dedicated web UI for advanced features like guest Wi-Fi management and viewing event logs.
- **Rich Sensor Data:** Creates a wide array of sensors for device status, client counts, data usage, firmware updates, PoE consumption, and much more.
- **Camera Integration:** View live RTSP streams from your Meraki cameras within Home Assistant.

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

* **How many seconds between Meraki API refreshes:** How often (in seconds) to poll the Meraki API for updates. Default: 300.
* **Where would you like the Meraki device type in the name?:** Choose how device names are presented. 'Prefix' adds the Meraki device name before the entity name, 'Suffix' adds it after, 'Omitted' uses only the entity name.
* **Auto-enable RTSP camera streams:** If checked, the integration will automatically enable the RTSP stream for all cameras that support it.
* **Use LAN IP for RTSP stream:** Controls how the RTSP stream URL is determined for cameras.
    * **When checked:** The integration will prioritize using a local IP address for the stream. It will first check if the URL from the Meraki API is already a local address. If not, it will try to construct a URL using the camera's detected LAN IP. This is the most efficient option if your Home Assistant instance is on the same local network as your cameras.
    * **When unchecked (default):** The integration will prioritize the URL provided by the Meraki API. If that URL is unavailable or invalid, it will fall back to using the camera's LAN IP as a last resort.
* **Webhook URL (optional):** A custom URL for Meraki webhooks. If left blank, the integration will use the default Home Assistant webhook URL.

## Lovelace Dashboard Card 🖼️

This integration provides a custom Lovelace card to display a dashboard of your Meraki network.

### How to Add the Card

**Step 1: Add the Javascript as a Lovelace Resource**

You must first add the `meraki-panel.js` file as a frontend resource in Home Assistant.

1.  Navigate to any of your dashboards.
2.  Click the **"..."** menu in the top right and select **"Edit Dashboard"**.
3.  Click the **"..."** menu again and select **"Manage resources"**.
4.  Click **"ADD RESOURCE"**.
5.  For the **URL**, enter `/hacsfiles/meraki-homeassistant/meraki-panel.js`.
    * *Note: This path assumes you installed the integration via HACS. If you installed it manually, the path will be `/local/meraki-panel.js` (if you placed the file in your `<config>/www` directory).*
6.  For **Resource type**, select **"JavaScript Module"**.
7.  Click **"CREATE"**.

**Step 2: Find your Meraki Config Entry ID**

The card needs to know which Meraki integration to display data from.

1.  Go to **Settings > Devices & Services**.
2.  Find the Meraki integration and click **"CONFIGURE"**.
3.  The **Config Entry ID** will be shown in the description text at the top of the dialog (e.g., "Your Config Entry ID is: ..."). Copy this ID.

**Step 3: Add the Card to your Dashboard**

1.  Go back to your dashboard and click **"ADD CARD"**.
2.  At the bottom of the list, choose the **"Manual"** card type.
3.  In the YAML editor, paste the following code:

    ```yaml
    type: custom:meraki-lovelace-card
    config_entry_id: YOUR_CONFIG_ENTRY_ID_HERE
    ```

4.  Replace `YOUR_CONFIG_ENTRY_ID_HERE` with the ID you copied in Step 2.
5.  Click **"SAVE"**.

## Services & Controls 🎛️

This integration provides several ways to control your Meraki network directly from Home Assistant.

### Parental Controls (Client Blocking)

For each client device that connects to your network, a `switch` entity is created. This switch allows you to block or unblock that specific client from accessing the network.

- **Entity ID:** `switch.<client_name>_blocked`
- **How it Works:** When you turn the switch `on`, the integration adds an L7 firewall rule to the SSID the client is connected to, effectively blocking its traffic. Turning it `off` removes the rule.
- **Use Case:** Easily implement parental controls, such as turning off a child's internet access at bedtime through an automation.

### Content Filtering

For each SSID, a `select` entity is created to manage Meraki's content filtering policies.

- **Entity ID:** `select.<ssid_name>_content_filtering`
- **How it Works:** This dropdown allows you to select the content filtering policy for the SSID from a list of available options (e.g., "Whitelisted," "Blocked," "Family-safe"). The integration fetches the available policies from your Meraki dashboard.

### SSID Control

You can enable or disable an entire SSID using a `switch` entity.

- **Entity ID:** `switch.<ssid_name>_enabled`
- **How it Works:** This is an indirect control method that works by adding or removing a specific tag (e.g., `ha-disabled`) on the access points within the network. This method is used due to Meraki API limitations but provides a reliable way to control SSID availability.

## Entities 🧩

### Device & Entity Model

The integration represents different aspects of your Meraki setup as devices within Home Assistant to create a logical hierarchy:

- **Meraki Organization:** A single device entry representing your entire Meraki Organization. This acts as a parent for organization-wide sensors.
- **Meraki Networks:** Each Meraki network is registered as a "device". Physical devices and SSIDs belonging to that network are parented by this device.
- **Physical Meraki Devices:** Your actual hardware (APs, switches, cameras, etc.) are registered as devices.
- **Meraki SSIDs:** Wireless SSIDs are registered as "devices," parented by their network.
- **Meraki VLANs:** Each VLAN is registered as a "device" to group its associated sensors.

### Organization-Wide Sensors

These sensors provide aggregate client counts across your entire Meraki organization and are linked to the Organization device. The client data for these sensors is based on activity within the **last day**.

| Entity Type | Name | Description |
| :--- | :--- | :--- |
| `sensor` | `Organization SSID Clients` | Total clients connected to all SSIDs across the organization. |
| `sensor` | `Organization Wireless Clients` | Total clients connected to wireless Access Points (MR series). |
| `sensor` | `Organization Appliance Clients` | Total clients that have routed traffic through security appliances (MX series). |
| `sensor` | `Organization Client Types` | A breakdown of client counts by type (SSID, Appliance, Wireless). |

### Camera Entities & Sensors

For each Meraki camera (MV series), a `camera` entity is created.

| Entity Type | Name | Description |
| :--- | :--- | :--- |
| `camera` | `[Camera Name]` | Provides a live video stream from the camera via RTSP. |
| `sensor` | `RTSP Stream URL` | The RTSP URL for the camera's video stream. The URL is only available when RTSP is enabled. |

**Note:** To view the camera stream, you must enable RTSP. You can do this via the "Auto-enable RTSP streams" global configuration option, or by using the individual `switch` entity created for each camera to toggle its RTSP stream.

### Physical Device Sensors

These sensors are linked to specific physical Meraki hardware devices.

| Entity Type | Name | Description | Availability |
| :--- | :--- | :--- | :--- |
| `sensor` | `[Device Name] Status` | The current operational status of the device (e.g., "online", "offline"). | All |
| `sensor` | `[Device Name] Connected Clients` | The number of clients currently connected to the device. | Wireless APs, Switches, Appliances |
| `sensor` | `[Device Name] Data Usage` | Total data usage for the device in the last day. | Appliances |
| `sensor` | `[Device Name] Firmware Status` | Indicates if a firmware update is available. | All |
| `sensor` | `[Device Name] PoE Usage` | The total PoE power being consumed by the device. | Switches |
| `sensor` | `[Device Name] WAN 1 Connectivity` | The connectivity status of the WAN 1 port. | Appliances |
| `sensor` | `[Device Name] WAN 2 Connectivity` | The connectivity status of the WAN 2 port. | Appliances |

### Network Sensors

These sensors are linked to Meraki Network "devices" in Home Assistant.

- **`[Network Name] Clients`**: Shows the number of clients active on a specific Meraki network.
- **Note:** For accurate organization-level total client counts, please use the `Organization ... Clients` sensors.
- **`[Network Name] Network Information`**: Provides detailed information about the network as attributes (notes, tags, time zone).
- **`[Network Name] Network Identity`**: Provides basic identity information about the network as attributes (ID, type).

### VLAN Sensors

For each VLAN configured in a network, the following sensors are created.

| Entity Type | Name | Description |
| :--- | :--- | :--- |
| `sensor` | `[VLAN Name] Subnet` | The subnet of the VLAN. |
| `sensor` | `[VLAN Name] Appliance IP` | The appliance IP address for the VLAN. |

### Appliance Port Sensors

For each port on a Meraki MX security appliance, a sensor is created to monitor its status.

| Entity Type | Name | Description |
| :--- | :--- | :--- |
| `sensor` | `[Appliance Name] Port [Port Number]` | The status of a specific port on a Meraki appliance (e.g., "connected"). |

### SSID Sensors

| Entity Type | Name | Description |
| :--- | :--- | :--- |
| `sensor` | `[SSID Name] Splash Page` | The type of splash page for the SSID. |
| `sensor` | `[SSID Name] Auth Mode` | The association control method for the SSID. |
| `sensor` | `[SSID Name] Encryption Mode` | The psk encryption mode for the SSID. |
| `sensor` | `[SSID Name] WPA Encryption Mode` | The types of WPA encryption. |
| `sensor` | `[SSID Name] IP Assignment Mode` | The client IP assignment mode. |
| `sensor` | `[SSID Name] Band Selection` | The client-serving radio frequencies of this SSID. |
| `sensor` | `[SSID Name] Per-Client Bandwidth Limit Up` | The upload bandwidth limit in Kbps. |
| `sensor` | `[SSID Name] Per-Client Bandwidth Limit Down` | The download bandwidth limit in Kbps. |
| `sensor` | `[SSID Name] Per-SSID Bandwidth Limit Up` | The total upload bandwidth limit in Kbps. |
| `sensor` | `[SSID Name] Per-SSID Bandwidth Limit Down` | The total download bandwidth limit in Kbps. |
| `sensor` | `[SSID Name] Visible` | Whether the SSID is advertised or hidden. |
| `sensor` | `[SSID Name] Availability` | Whether the SSID is enabled or disabled. |
| `sensor` | `[SSID Name] Channel` | The current operational channel of the SSID. |
| `sensor` | `[SSID Name] Client Count` | The number of clients connected to the SSID. |
| `sensor` | `[SSID Name] Walled Garden` | Whether the walled garden is enabled or disabled. |
| `sensor` | `[SSID Name] Mandatory DHCP` | Whether mandatory DHCP is enabled or disabled. |
| `sensor` | `[SSID Name] Minimum Bitrate 2.4GHz` | The minimum bitrate for the 2.4GHz band. |
| `sensor` | `[SSID Name] Minimum Bitrate 5GHz` | The minimum bitrate for the 5GHz band. |

### Environmental Sensors (MT Series)

For each Meraki environmental sensor (MT series), entities are created to monitor real-time conditions.

| Entity Type | Name | Description | Availability |
| :--- | :--- | :--- | :--- |
| `sensor` | `[Sensor Name] Temperature` | The ambient temperature. | MT10, MT12 |
| `sensor` | `[Sensor Name] Humidity` | The relative humidity. | MT10, MT12 |
| `sensor` | `[Sensor Name] Water Detection` | Whether water has been detected. | MT12 |
| `binary_sensor` | `[Sensor Name] Door` | The state of the door (open/closed). | MT20 |

## Automation Examples 🚀

### Notify when a device goes offline

```yaml
automation:
  - alias: "Notify when Meraki device goes offline"
    trigger:
      - platform: state
        entity_id: sensor.my_access_point_status
        to: "offline"
    action:
      - service: notify.mobile_app_my_phone
        data:
          message: "{{ trigger.to_state.name }} has gone offline."
