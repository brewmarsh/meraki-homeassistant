# Entities

This page describes the various entities (devices, sensors, switches, etc.) provided by the Meraki Home Assistant Integration.

## Meraki Device Types in Home Assistant

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

### Camera Switches

These switches are available for Meraki MV series cameras and provide control over specific camera features. They are linked to the physical camera device in Home Assistant.

| Entity Type | Name                            | Description                                                                | Availability      |
| :---------- | :------------------------------ | :------------------------------------------------------------------------- | :---------------- |
| Switch      | `[Camera Name] MV Sense`        | Controls the MV Sense (computer vision) feature on the camera.             | Meraki MV Cameras |
| Switch      | `[Camera Name] Audio Detection` | Controls the audio detection feature on the camera.                        | Meraki MV Cameras |
| Switch      | `[Camera Name] RTSP Server`     | Controls the RTSP (Real Time Streaming Protocol) server on Meraki cameras. | Meraki MV Cameras |

### Camera Sensors

These sensors provide additional information or status related to Meraki MV series cameras. They are linked to the physical camera device in Home Assistant.

| Entity Type | Name                            | Description                                                                                                                             | Availability      | Icon                                          |
| :---------- | :------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------- | :---------------- | :-------------------------------------------- |
| Sensor      | `[Camera Name] Sense Enabled`   | Displays if MV Sense (computer vision) is "enabled" or "disabled".                                                                      | Meraki MV Cameras | `mdi:camera-iris` or `mdi:camera-off-outline` |
| Sensor      | `[Camera Name] Audio Detection` | Displays if audio detection is "enabled" or "disabled".                                                                                 | Meraki MV Cameras | `mdi:microphone` or `mdi:microphone-off`      |
| Sensor      | `[Camera Name] RTSP Stream URL` | Displays the RTSP URL for the camera feed when the RTSP server is enabled. The state will be the URL string if active, otherwise empty. | Meraki MV Cameras | `mdi:video-stream`                            |

#### RTSP Functionality

The **`[Camera Name] RTSP Server`** switch allows you to enable or disable the RTSP stream for your Meraki camera. When this switch is turned ON, the **`[Camera Name] RTSP Stream URL`** sensor associated with the same camera will display the full RTSP stream address. This URL can be used in media players like VLC or streaming components in Home Assistant (e.g., the generic camera platform or WebRTC). If the RTSP Server switch is OFF, the sensor's state will be empty or unavailable.

---

_Contributions to expand this section with details on all existing entities are welcome._
