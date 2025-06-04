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
    *   Basic camera device status; snapshot URL generation to be explicitly integrated (e.g., as sensor attribute or service).
    *   Sensor values for MT series sensors (Future).
    * SSID Availability (Enabled/Disabled administrative status).
    * SSID Channel (current operational channel).
    * SSID Client Count.
* **Switch Entities:**
    * Control SSID enabled/disabled state.
    * Control SSID broadcast (visible/hidden) state.
* **Text Entities:**
    * Control SSID name (rename SSIDs).
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
    *   **Device Status:** Shows the operational status of Meraki devices (e.g., "online", "offline", "alerting"). Attributes include product type, model, serial, firmware, IPs, etc.
    *   **Connected Clients (per AP):** Number of clients connected to specific MR/GR access points.
    *   **Uplink Status (per MX):** Status of the uplinks for MX security appliances (e.g., "Online", "Offline"). Attributes include WAN IPs.
    *   **Network Client Count (per Network):** Total clients active on a network within a defined timespan.
    *   **Network Information (per MX/Appliance):** Provides various network parameters of an MX device as attributes (WAN IPs, DNS servers, LAN IP, Public IP, etc.). The sensor state is the device name.
    *   **Firmware Status (per Device):** Current firmware version and whether an update is available. Attributes include latest available version.
    *   **WAN1 Connectivity (per MX):** "Connected" or "Disconnected" status for the WAN1 interface of an MX device. Attribute includes WAN1 IP.
    *   **WAN2 Connectivity (per MX):** "Connected" or "Disconnected" status for the WAN2 interface of an MX device. Attribute includes WAN2 IP.
    *   **SSID Availability:** Administrative status (Enabled/Disabled) of an SSID, represented as ON/OFF.
    *   **SSID Channel:** Current operational channel for an SSID (derived data, may not be available for all SSIDs).
    *   **SSID Client Count:** Number of clients connected to a specific SSID.
    *   *(Future)* Sensor values for MT series environmental sensors.
    *   *(Future)* More detailed appliance/switch port statistics.

*   **Switch Entities:**
    *   **SSID Enabled Control:** Allows enabling or disabling an SSID.
    *   **SSID Broadcast Control:** Allows making an SSID visible (broadcasting) or hidden.

*   **Text Entities:**
    *   **SSID Name Control:** Allows viewing and changing the name of an SSID.

*   **Device Trackers:**
    *   Tracks connected client devices, showing if they are connected to the Meraki network.

*   **Home Assistant Devices:**
    *   Physical Meraki Devices (APs, switches, appliances, cameras, sensors) are registered.
    *   Meraki Networks are registered as "devices" to act as parents for physical devices and network-wide entities.
    *   Meraki SSIDs are registered as "devices", parented by their network, to group SSID-specific entities.

## Developer Guide

This section provides a brief overview for developers looking to extend the integration.

### Coordinators

The integration uses a coordinator pattern to manage data fetching and updates:
*   **`MerakiDataUpdateCoordinator` (`custom_components/meraki_ha/coordinators/base_coordinator.py`):** This is the main coordinator. It fetches general data for all physical devices (APs, switches, MX appliances) and networks within the organization. It uses `MerakiApiDataFetcher` for API calls and `DataAggregationCoordinator` to process and structure the data. Entities related to physical devices (like Device Status, Uplink Status, Connected Clients per AP) rely on this coordinator.
*   **`SSIDDeviceCoordinator` (`custom_components/meraki_ha/coordinators/ssid_device_coordinator.py`):** This coordinator is specifically responsible for managing SSIDs. It fetches detailed SSID information, registers each enabled SSID as a logical "device" in Home Assistant, and provides data for SSID-specific entities (like SSID Availability, SSID Client Count, SSID Channel, and SSID control switches/text entities). It gets the initial list of SSIDs from the `MerakiDataUpdateCoordinator` (via `api_data_fetcher` attribute) and then fetches further details itself.

### Adding Support for New Meraki Device Types

1.  **Data Fetching:** If the new device type requires fetching new API endpoints or processing existing data differently, modifications will be needed in `custom_components/meraki_ha/coordinators/api_data_fetcher.py`. Add new methods or update existing ones to retrieve the necessary information.
2.  **Entity Registration:**
    *   Define new sensor/switch/etc. classes in the respective directories (e.g., `custom_components/meraki_ha/sensor/`).
    *   Update `custom_components/meraki_ha/sensor_registry.py` (or a similar registry for other entity types) to map the new device's `productType` (as reported by the Meraki API) to the new entity classes.
    *   Ensure the `async_setup_entry` function in the relevant platform's `__init__.py` (e.g., `custom_components/meraki_ha/sensor/__init__.py`) correctly iterates through devices and uses the registry to create your new entities.
3.  **Coordinator Logic:** If the new device type has significantly different data patterns or requires unique handling not covered by the main coordinator, you might consider:
    *   Adding specific processing logic to `MerakiDataProcessor` and `DataAggregator`.
    *   For very distinct devices, potentially introducing a new dedicated `DataUpdateCoordinator` similar to `SSIDDeviceCoordinator`.
4.  **Device Typing:** Update `custom_components/meraki_ha/coordinators/meraki_device_types.py` if the new device model needs a specific type mapping for display name formatting or other logic.

### Adding New Sensors/Switches for Existing Device Types

1.  **Data Fetching:** Ensure the data required for your new entity is being fetched by `custom_components/meraki_ha/coordinators/api_data_fetcher.py` and is available in the data provided by the relevant coordinator (`MerakiDataUpdateCoordinator` for physical devices, `SSIDDeviceCoordinator` for SSIDs).
2.  **Entity Class:** Create your new sensor or switch class in the appropriate directory (e.g., `custom_components/meraki_ha/sensor/my_new_sensor.py`). This class will typically inherit from `MerakiEntity` (or a more specific base like `CoordinatorEntity`) and implement the necessary properties and methods.
3.  **Sensor Registry (for physical device sensors):** If it's a sensor for a physical device, add your new sensor class to `custom_components/meraki_ha/sensor_registry.py`, either to `COMMON_DEVICE_SENSORS` (if applicable to all devices) or to the list for the specific `productType` it applies to.
4.  **SSID Entities:** For SSID-specific entities, you'll likely add the instantiation of your new entity class within the `create_ssid_sensors` factory function in `custom_components/meraki_ha/sensor/ssid.py` (or a similar factory for switches/text entities if they are created that way).
5.  **Platform Setup:** Ensure the `async_setup_entry` in the platform's `__init__.py` correctly passes the coordinator and device/SSID data to your new entity's constructor.

Remember to test thoroughly, including API error handling and UI representation.

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
*   **SSID Control:** Enabling/disabling SSIDs and controlling broadcast status are direct API calls to modify SSID settings.
*   **Radio profiles might not be available or fully detailed for all wireless device models through the currently used API endpoints.**

##   Disclaimer

This is a custom Home Assistant integration. It is not officially endorsed or supported by Cisco Meraki or Home Assistant. Use at your own risk.
