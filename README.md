#   Meraki Home Assistant Integration

This Home Assistant integration allows you to monitor and manage your Cisco Meraki network, including devices, networks, and SSIDs. It leverages the Meraki API to bring data from your Meraki dashboard into Home Assistant, enabling you to gain insights into your network and automate actions based on its status.

##   Features

* **Device Discovery:** Automatically discovers Meraki hardware devices within your organization and networks.
* **Supported Devices:**
    * Wireless Access Points (MR series, GR series)
    * Switches (MS series, GS series)
    * Security Appliances (MX series)
    * Cameras (MV series) - Snapshot generation.
    * Environmental Sensors (MT series)
* **Entity Creation:** Creates Home Assistant entities for:
    * Meraki physical devices (APs, switches, appliances, cameras, sensors)
    * Meraki networks (represented as devices in HA for grouping)
    * Meraki SSIDs (wireless networks)
* **Data Monitoring:**
    * Device status (online/offline, product type)
    * Connected client counts (for APs, networks)
    * Appliance uplink status and potentially other data points (if specific sensors are developed).
    * Camera snapshot URL generation.
    * Sensor values for MT series sensors (model-dependent, requires specific sensor entity implementation).
    * Wireless radio settings for MR/GR access points (e.g., channel).
    * SSID Availability (Enabled/Disabled administrative status).
    * SSID Channel (current operational channel).
    * SSID Client Count.
* **Switch Entities:**
    * Control SSID enabled/disabled state (via a tagging strategy).
* **Configuration:**
    * API key and Organization ID via Home Assistant configuration flow.
    * Configurable scan interval for data refresh.
    * Device name formatting options (prefix, suffix, or omit device type in HA entity names).
    * Relaxed tag matching option for SSID-to-device association.
* **Authentication:**
    * Handles initial API key validation.
    * Supports re-authentication flow if credentials become invalid.

##   Installation

###   Prerequisites

* Home Assistant installation (ensure you are on a compatible version).
* A Cisco Meraki account with API access enabled.
* Your Meraki API key.
* Your Meraki Organization ID.

###   Installation Steps

1.  **Ensure HACS is installed:** If you haven't already, install the [Home Assistant Community Store (HACS)](https://hacs.xyz/).
2.  **Add Custom Repository:**
    *   In HACS, go to "Integrations".
    *   Click the three dots in the top right and select "Custom repositories".
    *   In the "Repository" field, enter the URL of this custom integration's GitHub repository.
    *   For "Category", select "Integration".
    *   Click "Add".
3.  **Install Integration:**
    *   Search for "Meraki" or the name of this integration in HACS.
    *   Click "Install" and follow the prompts.
4.  **Restart Home Assistant:** After installation, restart your Home Assistant instance to load the integration.

##   Configuration

1.  Navigate to **Settings** > **Devices & Services** in your Home Assistant UI.
2.  Click the **+ ADD INTEGRATION** button in the bottom right.
3.  Search for "Meraki" (or the specific name given to this integration) and select it.
4.  Follow the on-screen prompts:
    *   **API Key:** Enter your Cisco Meraki API key.
    *   **Organization ID:** Enter the ID of the Meraki organization you want to integrate.
    *   **Scan Interval (seconds):** Define how often (in seconds) Home Assistant should fetch data from the Meraki API. The default is 60 seconds. Adjust this based on the size of your network and the number of devices to avoid exceeding Meraki API rate limits. Shorter intervals provide more real-time data but increase API load.
    *   **Device Name Format:** (Optional) Choose how device names from Meraki should be formatted in Home Assistant (e.g., with a type prefix like "[Wireless] AP Name", a suffix, or omitted).
    *   **Relaxed Tag Matching:** (Optional) Enable if you want SSIDs to be associated with access points if *any* of the SSID's tags match any of the AP's tags. If disabled (strict mode), *all* of an SSID's tags must be present on an AP for association.

Once configured, the integration will start discovering your Meraki devices and creating corresponding entities in Home Assistant.

##   Obtaining a Meraki API Key and Organization ID

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
    *   The Organization ID is not directly visible in an obvious "Org ID" field.
    *   One way to find it is to look at the URL when you are viewing your organization dashboard. It might be part of the URL structure (e.g., `nXX...`).
    *   Alternatively, you can often find it by making a simple API call (e.g., using `curl` or Postman) to the `/organizations` endpoint with your API key. The response will list your accessible organizations and their IDs.
    ```bash
    curl -L -H 'X-Cisco-Meraki-API-Key: <your_api_key>' -H 'Content-Type: application/json' 'https://api.meraki.com/api/v1/organizations'
    ```

##   Entities Provided

Entities are dynamically created based on your Meraki setup.

*   **Sensor Entities:**
    *   **Device Status:** Shows the product type of Meraki devices (e.g., "Wireless", "Switch").
    *   **Connected Clients (per AP):** Number of clients connected to specific MR/GR access points.
    *   **Radio Settings (per AP):** Displays information like the current channel for AP radios.
    *   **Uplink Status (per MX):** Status of the primary uplink for MX security appliances.
    *   **Network Client Count (per Network):** Total clients active on a network within a timespan.
    *   **SSID Availability:** Administrative status (Enabled/Disabled) of an SSID.
    *   **SSID Channel:** Current operational channel for an SSID (derived from APs broadcasting it).
    *   **SSID Client Count:** Number of clients connected to a specific SSID.
    *   *(Future)* Sensor values for MT series environmental sensors.
    *   *(Future)* More detailed appliance/switch port statistics if API data is available and processed.

*   **Switch Entities:**
    *   **SSID Control:** Allows enabling/disabling SSIDs (achieved by managing device tags on associated APs).

*   **Device Trackers (Conceptual):**
    *   Represents Meraki hardware (like APs) and their "active" state based on client connectivity. Does not track individual client devices as HA device trackers.

*   **Home Assistant Devices:**
    *   Physical Meraki Devices (APs, switches, appliances, cameras, sensors) are registered.
    *   Meraki Networks are registered as "devices" to act as parents for physical devices and network-wide entities.
    *   Meraki SSIDs are registered as "devices", typically parented by the network or the APs broadcasting them, to group SSID-specific entities.

## Versioning and Releases

This project uses an automated versioning and release process triggered by merging Pull Requests (PRs) into the `main` branch.

*   **Automatic Version Increment:** When a PR is merged, the version number in `custom_components/meraki_ha/manifest.json` and `package.json` is automatically incremented.
*   **Determining Increment Type:** The type of version increment (major, minor, or patch) is determined by the PR title:
    *   `[major]` in the PR title (e.g., `[major] Implement new dashboard feature`) will trigger a major version update (e.g., `1.2.3` -> `2.0.0`).
    *   `[minor]` in the PR title (e.g., `[minor] Add support for new sensor type`) will trigger a minor version update (e.g., `1.2.3` -> `1.3.0`).
    *   `[patch]` in the PR title (e.g., `[patch] Fix API error handling`) or if no specific prefix is found, will trigger a patch version update (e.g., `1.2.3` -> `1.2.4`).
*   **Changelog Generation:** A `CHANGELOG.md` file is automatically updated with commit messages from the PR.
*   **GitHub Release:** A new GitHub Release is automatically created, tagged with the new version number (e.g., `v1.2.4`), and includes the changelog entries.

Please ensure your PR titles are descriptive and include the appropriate prefix if you intend to trigger a specific type of version bump.

##   Dependencies

*   `aiohttp`: For asynchronous HTTP requests to the Meraki API.

##   Known Issues

*   **API Rate Limits:** Frequent polling with a short scan interval on large networks can lead to exceeding Meraki API rate limits. Adjust the scan interval appropriately.
*   **Tag-based SSID Control:** Enabling/disabling SSIDs is managed by adding/removing specific tags on access points. This is an indirect control method and relies on consistent tag management.
*   Radio profile information might not be available or fully detailed for all wireless device models through the currently used API endpoints.

##   Disclaimer

This is a custom Home Assistant integration. It is not officially endorsed or supported by Cisco Meraki or Home Assistant. Use at your own risk.
