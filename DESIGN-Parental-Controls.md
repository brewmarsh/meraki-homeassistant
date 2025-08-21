# Design Document: Parental Controls & Content Filtering

This document outlines the design for the Parental Controls & Content Filtering feature for the Meraki Home Assistant integration.

## 1. Feature Overview

The goal of this feature is to provide users with simple, powerful tools to manage internet access and content filtering for their home network directly from Home Assistant. This will be achieved by creating new entities that control the features of Meraki MX Security Appliances.

The feature will consist of two main components:

1.  **Content Filtering Policy Switch:** A `select` entity in Home Assistant that allows the user to change the active content filtering policy for a network.
2.  **"Internet Time-Out" Switch per Device:** A `switch` entity for each client device on the network, allowing the user to block or allow internet access for that device on demand.

## 2. User Interface (UI) Design

The primary user interface for this feature will be a new "Parental Controls" page within the existing Meraki web UI.

### Proposed UI Layout:

```
------------------------------------------------------
| Parental Controls                                  |
------------------------------------------------------
|                                                    |
|  **Content Filtering**                             |
|                                                    |
|  Network Policy: [ Homework ▼ ]  (Save Button)     |
|                                                    |
|  --------------------------------------------------  |
|                                                    |
|  **Client Devices**                                |
|                                                    |
|  - John's iPad        (Connected)   [ Internet On |o ] |
|  - Living Room TV     (Connected)   [ Internet On |o ] |
|  - Guest Phone        (Connected)   [ Internet On |o ] |
|                                                    |
------------------------------------------------------
```

### UI Components:

*   **Content Filtering Dropdown:** A `<select>` dropdown menu that will be populated with the list of available content filtering policies from the Meraki network.
*   **Save Button:** A button to apply the selected content filtering policy.
*   **Client List:** A list of all client devices on the network.
*   **Internet Access Toggle:** A toggle switch for each client device to enable or disable their internet access.

## 3. Technical Implementation

### Home Assistant Entities:

*   **`select.meraki_content_filtering_policy`:** A `select` entity to control the network's content filtering policy.
*   **`switch.meraki_client_internet_access_<client_mac>`:** A `switch` entity for each client device to control its internet access.

### Meraki API Endpoints:

*   **Content Filtering:**
    *   `GET /networks/{networkId}/appliance/contentFiltering` - To get the current content filtering settings.
    *   `GET /networks/{networkId}/appliance/contentFiltering/categories` - To get the list of available content filtering categories, which can be used to populate the `select` entity.
    *   `PUT /networks/{networkId}/appliance/contentFiltering` - To update the content filtering settings.
*   **Client Firewall Rules:**
    *   `GET /networks/{networkId}/appliance/firewall/l7FirewallRules` - To get the current layer 7 firewall rules for the network.
    *   `PUT /networks/{networkId}/appliance/firewall/l7FirewallRules` - To update the layer 7 firewall rules. This will be used to block or allow internet access for specific clients. We will need to manage the rules carefully to avoid overwriting existing user-configured rules.

### Backend Logic:

*   The integration will need to fetch the list of content filtering policies and populate the `select` entity.
*   When the `select` entity's state is changed, the integration will make a `PUT` request to the Meraki API to update the content filtering policy.
*   The integration will need to fetch the list of clients on the network.
*   For each client, a `switch` entity will be created.
*   When a `switch` entity is toggled, the integration will add or remove a firewall rule to block or allow traffic for that client's IP address. The rule will need to be carefully constructed to block all traffic.
*   The integration will need to periodically refresh the list of clients and the state of the firewall rules.
*   **Important:** To avoid interfering with user-defined firewall rules, the integration will add a comment to the rules it creates (e.g., `"comment": "Managed by Home Assistant Meraki Integration"`). When updating the rules, it will only modify the rules with this comment, leaving other rules untouched.
