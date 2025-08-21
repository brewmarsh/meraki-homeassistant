# Meraki Home Assistant Integration 🤖

This Home Assistant integration allows you to monitor and manage your Cisco Meraki network, including devices, networks, and SSIDs. It leverages the Meraki API to bring data from your Meraki dashboard into Home Assistant, enabling you to gain insights into your network and automate actions based on its status.

## Features ✨

- **Device Discovery:** Automatically discovers Meraki hardware devices within your organization and networks.
- **Supported Devices:**
  - Wireless Access Points (MR series, GR series)
  - Switches (MS series, GS series)
  - Security Appliances (MX series)
  - Cameras (MV series) - Snapshot generation.
  - Environmental Sensors (MT series)
- **Entity Creation:** Creates Home Assistant entities for:
  - Meraki physical devices (APs, switches, appliances, cameras, sensors)
  - Meraki networks (represented as devices in HA for grouping)
  - Meraki SSIDs (wireless networks)
- **Data Monitoring:**
  - Device status (online/offline, product type)
  - Connected client counts (for APs, networks)
  - Appliance uplink status and potentially other data points (if specific sensors are developed).
  - Basic camera device status; snapshot URL generation to be explicitly integrated (e.g., as sensor attribute or service).
  - Sensor values for MT series sensors (Future).
  - Wireless radio settings for MR/GR access points (e.g., channel).
  - SSID Availability (Enabled/Disabled administrative status).
  - SSID Channel (current operational channel).
  - SSID Client Count.
- **Switch Entities:**
  - Control SSID enabled/disabled state (via a tagging strategy).
- **Configuration:**
  - API key and Organization ID via Home Assistant configuration flow.
  - Configurable scan interval for data refresh.
  - Device name formatting options (prefix, suffix, or omit device type in HA entity names).
- **Authentication:**
  - Handles initial API key validation.
  - Supports re-authentication flow if credentials become invalid.

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
    *   Navigate to **Organization** > **Settings**.
    *   Under the **Dashboard API access** section, ensure API access is enabled.
3.  **Generate API Key:**
    *   Go to your **Profile** (click your name/email in the top right) > **My profile**.
    *   Scroll down to the **API access** section.
    *   Click **Generate new API key**.
    *   **Important:** Copy the generated API key and store it securely. You will not be able to see it again after navigating away from this page.
4.  **Find Organization ID:**
    *   **Easiest Method:** The Organization ID is displayed at the bottom of every page in the Meraki dashboard. Simply scroll down to find it.
    *   **Alternative Method (URL):** The Organization ID can sometimes be found in the URL when you are viewing your organization dashboard.
    *   **Alternative Method (API):** You can find it by making a simple API call to the `/organizations` endpoint with your API key. The response will list your accessible organizations and their IDs.

    ```bash
    curl -L -H 'X-Cisco-Meraki-API-Key: <your_api_key>' -H 'Content-Type: application/json' 'https://api.meraki.com/api/v1/organizations'
    ```

### Setting up the Integration

1.  Navigate to **Settings** > **Devices & Services** in your Home Assistant UI.
2.  Click the **+ ADD INTEGRATION** button in the bottom right.
3.  Search for "Meraki" and select it.
4.  Follow the on-screen prompts to enter your API Key and Organization ID.

### Configuration Options

The following options can be configured when you first set up the integration, or at any time by navigating to the integration's card in **Settings -> Devices & Services** and clicking **Configure**.

*   **How many seconds between Meraki API refreshes:** How often (in seconds) to poll the Meraki API for updates. Default: 300. A shorter interval means more responsive sensors but significantly increases API calls to Meraki Cloud and may lead to rate limiting.
*   **Where would you like the Meraki device type in the name?:** Choose how device names are presented. 'Prefix' adds the Meraki device name before the entity name, 'Suffix' adds it after, 'Omitted' uses only the entity name.
*   **Auto-enable RTSP camera streams:** If checked, the integration will automatically enable the RTSP stream for all cameras that support it. This is useful for getting camera streams working without manual configuration in the Meraki dashboard.
*   **Use LAN IP for RTSP stream:** If checked, the integration will use the camera's LAN IP address for the RTSP stream. This is more efficient, but requires that Home Assistant is on the same network as the camera. If unchecked, the public IP address will be used.
*   **Webhook URL (optional):** A custom URL for Meraki webhooks. If left blank, the integration will use the default Home Assistant webhook URL.

## Entities 🧩

This integration provides various entities (devices, sensors, switches, etc.).

### Meraki Device Types in Home Assistant

The integration automatically categorizes your physical Meraki hardware into `productType` groups based on the device model. This allows for `productType`-specific sensors and controls. The following table details the mapping from model prefixes to the assigned `productType`:

| `productType` | Model Prefix(es) | Description               |
| :------------ | :--------------- | :------------------------ |
| `appliance`   | `MX`, `GX`       | Security Appliances       |
| `wireless`    | `MR`, `GR`       | Wireless Access Points    |
| `switch`      | `MS`, `GS`       | Network Switches          |
| `camera`      | `MV`             | Smart Cameras             |
| `sensor`      | `MT`             | Environmental Sensors     |
| `cellular`    | `MG`             | Cellular Gateways         |

The integration represents different aspects of your Meraki setup as devices within Home Assistant:

- **Physical Meraki Devices:** Your actual hardware (APs, switches, security appliances, cameras, environmental sensors) are registered as devices. Entities related to a specific piece of hardware (e.g., its status, IP address, connected clients for an AP) are linked to these devices.
- **Meraki Networks:** Each Meraki network defined in your dashboard is also registered as a "device" in Home Assistant. This allows for grouping; physical devices belonging to a network are often parented by their respective Meraki Network device in Home Assistant. Some network-wide sensors may also be linked here.
- **Meraki SSIDs:** Wireless SSIDs are registered as "devices," typically parented by their Meraki Network device. Entities specific to an SSID (e.g., its availability, client count, control switches) are linked to these SSID devices.
- **Meraki VLANs:** Each VLAN is registered as a "device" to group its associated sensors.
- **Meraki Organization:** A single device entry is created to represent the Meraki Organization itself. This device acts as a parent for organization-wide sensors.

### Organization Device

A conceptual device representing your entire Meraki Organization is created.

- **Naming:** The name of this device is based on the Organization Name fetched from the Meraki Dashboard.
- **Purpose:** This device serves as a central point for organization-wide information and sensors.

### Organization-Wide Client Sensors

These sensors provide aggregate client counts across your entire Meraki organization and are linked to the Organization device described above. The client data for these sensors is based on activity within the **last day** (the default timespan for the Meraki API).

- **`Organization SSID Clients`** (`sensor.<org_name>_ssid_clients`):
- **Description:** Total clients connected to all SSIDs across all networks in the organization.
- **Unit of Measurement:** `clients`
- **Icon:** `mdi:wifi`

- **`Organization Wireless Clients`** (`sensor.<org_name>_wireless_clients`):
- **Description:** Total clients connected to wireless Access Points (MR series devices) across the organization.
- **Unit of Measurement:** `clients`
- **Icon:** `mdi:access-point-network`

- **`Organization Appliance Clients`** (`sensor.<org_name>_appliance_clients`):
- **Description:** Total clients that have routed traffic through Meraki security appliances (MX series devices) across the organization.
- **Unit of Measurement:** `clients`
- **Icon:** `mdi:server-network`

- **`Organization Client Types`** (`sensor.<org_name>_client_types`):
- **Description:** A sensor that provides a breakdown of client counts by type (SSID, Appliance, Wireless) for the entire organization. The state of the sensor is the total number of clients, and the individual counts are available as attributes.
- **Unit of Measurement:** `clients`
- **Icon:** `mdi:account-group`

### Camera Entities

For each Meraki camera (MV series) in your organization, a `camera` entity is created in Home Assistant.

| Entity Type | Name           | Description                                                                                                                                                                                             | Availability      |
| :---------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------- |
| `camera`    | `[Camera Name]`| Provides a live video stream from the camera. This entity can be used in picture-in-picture cards, dashboards, and other parts of Home Assistant to view the camera's feed. The stream is provided via RTSP. | Meraki MV Cameras |

To view the camera stream, you must enable the RTSP (Real-Time Streaming Protocol) feature for the camera. You can do this in two ways:

1.  **Individually per Camera:** Each camera device in Home Assistant has a switch entity to toggle the RTSP stream on or off. When you enable the switch, the integration will make an API call to Meraki to enable the RTSP server for that camera. The RTSP stream URL will then become available in the `RTSP Stream URL` sensor.
2.  **Globally via Configuration:** In the integration's configuration options, you can enable the "Auto-enable RTSP streams" setting. This will automatically enable the RTSP stream for all of your cameras.

### Camera Sensors

| Entity Type | Name              | Description                                                                                                                                                                                           | Availability      |
| :---------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------- |
| `sensor`    | `RTSP Stream URL` | Displays the RTSP URL for the camera's video stream. The URL is only available when the RTSP stream is enabled for the camera. This sensor's state will be empty if RTSP is disabled. | Meraki MV Cameras |

### Physical Device Sensors

These sensors are linked to specific physical Meraki hardware devices.

| Entity Type | Name | Description | Availability |
| :--- | :--- | :--- | :--- |
| `sensor` | `[Device Name] Status` | Shows the current status of the device (e.g., "online", "offline"). | All |
| `sensor` | `[Device Name] Connected Clients` | The number of clients currently connected to the device. | Wireless APs, Switches, Appliances |
| `sensor` | `[Device Name] Data Usage` | The total data usage for the device in the last day. | Appliances |
| `sensor` | `[Device Name] Firmware Status` | Indicates if a firmware update is available. | All |
| `sensor` | `[Device Name] PoE Usage` | The total PoE power being consumed by the device. | Switches |
| `sensor` | `[Device Name] WAN 1 Connectivity` | The connectivity status of the WAN 1 port. | Appliances |
| `sensor` | `[Device Name] WAN 2 Connectivity` | The connectivity status of the WAN 2 port. | Appliances |

### Network Sensors

These sensors are linked to Meraki Network "devices" in Home Assistant.

- **`[Network Name] Clients`** (`sensor.<network_name>_clients`):
- **Description:** Shows the number of clients active on a specific Meraki network.
- **Note:** This sensor is designed for per-network client counts. For accurate organization-level total client counts, please use the `Organization SSID Clients`, `Organization Wireless Clients`, or `Organization Appliance Clients` sensors.

- **`[Network Name] Network Information`** (`sensor.<network_name>_network_information`):
- **Description:** A sensor that provides detailed information about the network. The state of the sensor is the network name, and additional details such as notes, tags, and time zone are available as attributes.

- **`[Network Name] Network Identity`** (`sensor.<network_name>_network_identity`):
- **Description:** A sensor that provides basic identity information about the network. The state of the sensor is the network name, and the network ID and type are available as attributes.

### VLAN Devices

Each VLAN configured in a network is represented as a device in Home Assistant. This device groups the sensors related to that VLAN.

| Entity Type | Name | Description | Availability |
| :--- | :--- | :--- | :--- |
| `sensor` | `[VLAN Name] Subnet` | Shows the subnet of the VLAN. | Networks with VLANs |
| `sensor` | `[VLAN Name] Appliance IP` | Shows the appliance IP address for the VLAN. | Networks with VLANs |

### Appliance Port Sensors

For each port on a Meraki MX security appliance, a sensor is created to monitor its status.

| Entity Type | Name | Description | Availability |
| :--- | :--- | :--- | :--- |
| `sensor` | `[Appliance Name] Port [Port Number]` | Shows the status of a specific port on a Meraki appliance. The state can be "connected", "disconnected", or "disabled". Additional attributes include link speed, VLAN, type, and access policy. | Meraki MX Appliances |

### SSID Sensors

These sensors are linked to Meraki SSID "devices" in Home Assistant.

| Entity Type | Name              | Description                                                                                                                                                                                           | Availability      |
| :---------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------- |
| `sensor`    | `[SSID Name] Splash Page` | The type of splash page for the SSID. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Auth Mode` | The association control method for the SSID. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Encryption Mode` | The psk encryption mode for the SSID. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] WPA Encryption Mode` | The types of WPA encryption. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] IP Assignment Mode` | The client IP assignment mode. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Band Selection` | The client-serving radio frequencies of this SSID. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Per-Client Bandwidth Limit Up` | The upload bandwidth limit in Kbps. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Per-Client Bandwidth Limit Down` | The download bandwidth limit in Kbps. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Per-SSID Bandwidth Limit Up` | The total upload bandwidth limit in Kbps. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Per-SSID Bandwidth Limit Down` | The total download bandwidth limit in Kbps. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Visible` | Whether the SSID is advertised or hidden. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Availability` | Whether the SSID is enabled or disabled. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Channel` | The current operational channel of the SSID. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Client Count` | The number of clients connected to the SSID. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Walled Garden` | Whether the walled garden is enabled or disabled. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Mandatory DHCP` | Whether mandatory DHCP is enabled or disabled. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Minimum Bitrate 2.4GHz` | The minimum bitrate for the 2.4GHz band. | Meraki Wireless SSIDs |
| `sensor`    | `[SSID Name] Minimum Bitrate 5GHz` | The minimum bitrate for the 5GHz band. | Meraki Wireless SSIDs |

## Automation Examples 🚀

Here are a few examples of how you can use the entities from this integration in your Home Assistant automations.

### Notify when a device goes offline

This automation sends a notification to your phone when a Meraki device goes offline.

```yaml
automation:
  - alias: "Notify when Meraki device goes offline"
    trigger:
      - platform: state
        entity_id:
          - sensor.my_access_point_status
          - sensor.my_switch_status
        to: "offline"
    action:
      - service: notify.mobile_app_my_phone
        data:
          message: "{{ trigger.to_state.name }} has gone offline."
```

### Turn on a light when a client connects to a specific SSID

This automation turns on a light when a new client connects to your guest SSID.

```yaml
automation:
  - alias: "Turn on light when guest connects"
    trigger:
      - platform: numeric_state
        entity_id: sensor.my_guest_ssid_client_count
        above: 0
    action:
      - service: light.turn_on
        target:
          entity_id: light.guest_room_lamp
```

## Troubleshooting 🆘

### Common Issues

#### Invalid Authentication

If you receive an "Invalid authentication" error, it means that your API key or Organization ID is incorrect. Please double-check your credentials and try again.

#### Cannot Connect

If you receive a "Cannot connect" error, it means that Home Assistant is unable to connect to the Meraki API. Please check your internet connection and ensure that there are no firewalls blocking access to the Meraki API.

#### API Rate Limits

The Meraki API has rate limits that restrict the number of API calls that can be made in a given time period. If you have a large number of devices or a short scan interval, you may exceed these rate limits. If this happens, you will see errors in the Home Assistant logs. To resolve this, you can increase the scan interval in the integration's options.

#### Feature Disabled Errors

Some sensors, such as VLAN and traffic analysis sensors, require specific features to be enabled in your Meraki dashboard. If a required feature is not enabled, you may see errors in the Home Assistant logs, and the corresponding sensors will show a "Disabled" state.

To resolve this, you need to enable the required feature in your Meraki dashboard. For example, to use the traffic analysis sensors, you need to enable "Traffic Analysis with Hostname Visibility" for the network. To use the VLAN sensors, you need to have VLANs enabled for the network.

### Getting Help

If you are still having issues, you can get help in the following ways:

*   **Home Assistant Community Forums:** Post a question in the [Meraki integration thread](https://community.home-assistant.io/t/meraki-integration/12345) (link is a placeholder).
*   **GitHub Issues:** If you believe you have found a bug, please open an issue on the [GitHub repository](https://github.com/your-repo/meraki-ha).

## Versioning and Releases

This project uses an automated versioning and release process triggered by merging Pull Requests (PRs) into the `main` branch.

- **Automatic Version Increment:** When a PR is merged, the version number in `custom_components/meraki_ha/manifest.json` and `package.json` is automatically incremented.
- **Determining Increment Type:** The type of version increment (major, minor, or patch) is determined by the PR title:
- `[major]` in the PR title (e.g., `[major] Implement new dashboard feature`) will trigger a major version update (e.g., `1.2.3` -> `2.0.0`).
- `[minor]` in the PR title (e.g., `[minor] Add support for new sensor type`) will trigger a minor version update (e.g., `1.2.3` -> `1.3.0`).
- `[patch]` in the PR title (e.g., `[patch] Fix API error handling`) or if no specific prefix is found, will trigger a patch version update (e.g., `1.2.3` -> `1.2.4`).
- **Changelog Generation:** A `CHANGELOG.md` file is automatically updated with commit messages from the PR.
- **GitHub Release:** A new GitHub Release is automatically created, tagged with the new version number (e.g., `v1.2.4`), and includes the changelog entries.

Please ensure your PR titles are descriptive and include the appropriate prefix if you intend to trigger a specific type of version bump.

## Dependencies 📦

- `meraki`: The official Meraki SDK for Python, used for all API interactions.
- `aiohttp`: Used by the Meraki SDK for asynchronous HTTP requests.

## Known Issues ⚠️

- **API Rate Limits:** Frequent polling with a short scan interval on large networks can lead to exceeding Meraki API rate limits. Adjust the scan interval appropriately.
- **SSID Control:** Enabling/disabling SSIDs is managed by adding/removing specific tags on access points, not by direct administrative status change of the SSID. This is an indirect control method and relies on consistent tag management.
- **Radio profiles might not be available or fully detailed for all wireless device models through the currently used API endpoints.**

## Disclaimer 📜

This is a custom Home Assistant integration. It is not officially endorsed or supported by Cisco Meraki or Home Assistant. Use at your own risk.
