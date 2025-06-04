# Entities

This page describes the various entities (devices, sensors, switches, etc.) provided by the Meraki Home Assistant Integration.

## Meraki Device Types in Home Assistant

The integration represents different aspects of your Meraki setup as devices within Home Assistant:

*   **Physical Meraki Devices:** Your actual hardware (APs, switches, security appliances, cameras, environmental sensors) are registered as devices. Entities related to a specific piece of hardware (e.g., its status, IP address, connected clients for an AP) are linked to these devices.
*   **Meraki Networks:** Each Meraki network defined in your dashboard is also registered as a "device" in Home Assistant. This allows for grouping; physical devices belonging to a network are often parented by their respective Meraki Network device in Home Assistant. Some network-wide sensors may also be linked here.
*   **Meraki SSIDs:** Wireless SSIDs are registered as "devices," typically parented by their Meraki Network device. Entities specific to an SSID (e.g., its availability, client count, control switches) are linked to these SSID devices.
*   **Meraki Organization (New):** A single device entry is created to represent the Meraki Organization itself. This device acts as a parent for organization-wide sensors.

## Organization Device

A new conceptual device representing your entire Meraki Organization is now created.

*   **Naming:** The name of this device is based on the Organization Name fetched from the Meraki Dashboard.
    *   It can be prefixed (e.g., `[Org] Your Org Name`) or suffixed (e.g., `Your Org Name [Org]`) based on the "Device Name Format" option chosen during integration setup or in the options flow. If the format is "omitted", the raw organization name is used.
*   **Purpose:** This device serves as a central point for organization-wide information and sensors.

### Organization-Wide Client Sensors

These sensors provide aggregate client counts across your entire Meraki organization and are linked to the Organization device described above. The client data for these sensors is typically based on activity within the **last hour** (timespan increased from 5 minutes for more stable counts).

*   **`Organization SSID Clients`** (`sensor.<org_name>_ssid_clients`):
    *   **Description:** Total clients connected to all SSIDs across all networks in the organization.
    *   **Unit of Measurement:** `clients`
    *   **Icon:** `mdi:wifi`

*   **`Organization Wireless Clients`** (`sensor.<org_name>_wireless_clients`):
    *   **Description:** Total clients connected to wireless Access Points (MR series devices) across the organization.
    *   **Unit of Measurement:** `clients`
    *   **Icon:** `mdi:access-point-network`

*   **`Organization Appliance Clients`** (`sensor.<org_name>_appliance_clients`):
    *   **Description:** Total clients that have routed traffic through Meraki security appliances (MX series devices) across the organization.
    *   **Unit of Measurement:** `clients`
    *   **Icon:** `mdi:server-network`

## Physical Device Sensors

These sensors are linked to specific physical Meraki hardware devices.

*   *(Details of existing physical device sensors like status, uplink, firmware, etc., would go here. This section can be expanded as other sensors are documented.)*

## Network Sensors

These sensors are linked to Meraki Network "devices" in Home Assistant.

*   **`Network Client Count`** (`sensor.<network_name>_client_count`):
    *   **Description:** Shows the number of clients active on a *specific* Meraki network within a defined timespan.
    *   **Note:** This sensor is designed for per-network client counts. For accurate organization-level total client counts, please use the new `Organization SSID Clients`, `Organization Wireless Clients`, or `Organization Appliance Clients` sensors. This sensor relies on the data coordinator providing a specific `network_client_counts` data structure.

*   *(Details of other network-specific sensors like Network Information for MX would go here.)*

## SSID Sensors

These sensors are linked to Meraki SSID "devices" in Home Assistant.

*   *(Details of existing SSID-specific sensors like SSID Availability, SSID Client Count (per SSID), SSID Channel would go here.)*

## Switches and Other Entities

*   *(Details of switch entities for SSID control, text entities for SSID renaming, etc., would go here.)*

---
*Contributions to expand this section with details on all existing entities are welcome.*
