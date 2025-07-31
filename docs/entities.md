# Entities

This page describes the various entities (devices, sensors, switches, etc.) provided by the Meraki Home Assistant Integration.

## Meraki Device Types in Home Assistant

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
- **Meraki Organization:** A single device entry is created to represent the Meraki Organization itself. This device acts as a parent for organization-wide sensors.

## Organization Device

A conceptual device representing your entire Meraki Organization is created.

- **Naming:** The name of this device is based on the Organization Name fetched from the Meraki Dashboard.
- The name is based on the Organization Name fetched from the Meraki Dashboard.
- **Purpose:** This device serves as a central point for organization-wide information and sensors.

### Organization-Wide Client Sensors

These sensors provide aggregate client counts across your entire Meraki organization and are linked to the Organization device described above. The client data for these sensors is typically based on activity within the **last hour** (timespan increased from 5 minutes for more stable counts).

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

## Camera Entities

For each Meraki camera (MV series) in your organization, a `camera` entity is created in Home Assistant.

| Entity Type | Name           | Description                                                                                                                                                                                             | Availability      |
| :---------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------- |
| `camera`    | `[Camera Name]`| Provides a live video stream from the camera. This entity can be used in picture-in-picture cards, dashboards, and other parts of Home Assistant to view the camera's feed. The stream is provided via RTSP. | Meraki MV Cameras |

To view the camera stream, the RTSP (Real Time Streaming Protocol) server must be enabled for the camera in your Meraki dashboard. Alternatively, you can enable the "Auto-enable RTSP streams" option in the integration's configuration, and Home Assistant will automatically enable the RTSP stream for all of your cameras.

## Physical Device Sensors

These sensors are linked to specific physical Meraki hardware devices.

- _(Details of existing physical device sensors like status, uplink, firmware, etc., would go here. This section can be expanded as other sensors are documented.)_

## Network Sensors

These sensors are linked to Meraki Network "devices" in Home Assistant.

- **`Network Client Count`** (`sensor.<network_name>_client_count`):
- **Description:** Shows the number of clients active on a _specific_ Meraki network within a defined timespan.
- **Note:** This sensor is designed for per-network client counts. For accurate organization-level total client counts, please use the new `Organization SSID Clients`, `Organization Wireless Clients`, or `Organization Appliance Clients` sensors. This sensor relies on the data coordinator providing a specific `network_client_counts` data structure.

- _(Details of other network-specific sensors like Network Information for MX would go here.)_

### Appliance Port Sensors

These sensors are linked to Meraki MX security appliance "devices" in Home Assistant.

| Entity Type | Name | Description | Availability |
| :--- | :--- | :--- | :--- |
| Sensor | `[Appliance Name] Port [Port Number]` | Shows the status of a specific port on a Meraki appliance. The state will be "connected" or "disconnected". | Meraki MX Appliances |

## SSID Sensors

These sensors are linked to Meraki SSID "devices" in Home Assistant.

- _(Details of existing SSID-specific sensors like SSID Availability, SSID Client Count (per SSID), SSID Channel would go here.)_

## Switches and Other Entities

- _(Details of switch entities for SSID control, text entities for SSID renaming, etc., would go here.)_

---

_Contributions to expand this section with details on all existing entities are welcome._
