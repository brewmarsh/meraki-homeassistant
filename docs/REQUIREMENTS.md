# Meraki Home Assistant Integration Requirements

## Core Functionality

### Meraki API Integration

| Requirement                                                                   | Status   |
| :---------------------------------------------------------------------------- | :------- |
| The integration needs to communicate with the Cisco Meraki API to fetch data. | Included |
| It requires an API key and organization ID for authentication.                | Included |
| The API key must be stored securely.                                          | Included |

### Meraki Device Discovery and Setup

| Requirement                                                                                                 | Status   |
| :---------------------------------------------------------------------------------------------------------- | :------- |
| The integration must discover Meraki hardware devices within the specified organization and networks.       | Included |
| It should create or update device entities in Home Assistant based on these hardware devices.               | Included |
| Device types (Wireless, Switch, Appliance, Camera, Sensor) should be correctly identified.                  | Included |
| Device names should be formattable, with options for prefixes, suffixes, or omission of device type labels. | Included |
| Devices should include the model name, serial number, MAC address(es) and firmware version.                 | Included |

### Data Retrieval

| Requirement                                                                                             | Status   |
| :------------------------------------------------------------------------------------------------------ | :------- |
| The integration should retrieve device data, including connected clients for wireless devices (MR, GR)  | Included |
| The integration should retrieve device data, including connected clients for appliances (MX, GX).       | Included |
| The integration should retrieve device data, including connected clients for network switches (MS, GS). | Included |
| Data should be updated at a configurable scan interval.                                                 | Included |

### Home Assistant Integration

| Requirement                                                                                                                                                                                                                        | Status   |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| The integration should create sensor, device tracker, and switch entities in Home Assistant.                                                                                                                                       | Included |
| The integration must properly handle config entries, including setup, unloading, and reloading.                                                                                                                                    | Included |
| The integration needs to have a configuration flow to take the API key and org id.                                                                                                                                                 | Included |
| The integration must have a native, multi-step Home Assistant Options Flow to manage settings (e.g., enabling camera entities, device sensors) via a menu-driven interface, adhering to HA UX guidelines for complex integrations. | Included |
| The integration should handle re-authentication of the API key.                                                                                                                                                                    | Included |
| The integration must provide comprehensive localization for all configuration flows, including the multi-step Options Flow Menu, using `strings.json` and translation files.                                                       | Included |

### Mapping Meraki objects to Home Assistant objects

| Requirement                                                                                                           | Status   |
| :-------------------------------------------------------------------------------------------------------------------- | :------- |
| Physical Meraki devices (Wireless, Switch, Appliance, Camera, Sensor) will have corresponding Home Assistant devices. | Included |
| Meraki networks will be shown as Home Assistant devices.                                                              | Included |
| Meraki SSIDs (wireless networks) will be shown as Home Assistant devices.                                             | Included |
| Meraki VLANs will be shown as Home Assistant devices.                                                                 | Included |

### Meraki Appliances

| Requirement                                                                                              | Status   |
| :------------------------------------------------------------------------------------------------------- | :------- |
| Meraki appliances should have sensors that track data usage.                                             | Included |
| Meraki appliances should have a sensor that tracks the number of connected clients.                      | Included |
| Meraki appliances have VLANs; these VLANs should appear as Home Assistant devices.                       | Included |
| Meraki appliances have an external hostname; this should appear as details of the Home Assistant device. | Included |
| Meraki appliances should have a sensor that tracks the number of ports in use.                           | Included |
| Meraki appliances should have a sensor that tracks the number of ports available.                        | Included |
| Meraki appliances should show the status of the appliance uplinks                                        | Included |

### Meraki Wireless

| Requirement                                                                                                                                                                                                   | Status   |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------- |
| Meraki wireless devices should appear as Home Assistant devices                                                                                                                                               | Included |
| Meraki wireless devices should have a sensor that tracks the number of connected clients.                                                                                                                     | Included |
| Meraki SSID names should appear as Home Assistant devices                                                                                                                                                     | Included |
| Disabled SSIDs should not be shown in the list                                                                                                                                                                | Working  |
| SSID names should be updateable                                                                                                                                                                               | Included |
| SSIDs should be able to have the "Broadcast SSID" feature enabled / disabled                                                                                                                                  | Fixed    |
| Meraki SSIDs should have sensors for splash page, auth mode, encryption mode, WPA encryption mode, IP assignment mode, band selection, per-client bandwidth limits, per-SSID bandwidth limits, and visibility | Included |

### Meraki Switches

| Requirement                                                                                  | Status   |
| :------------------------------------------------------------------------------------------- | :------- |
| If the Meraki switch supports PoE, the switch should have sensors that aggregated PoE usage. | Included |
| Meraki switches should have a sensor that tracks the number of ports in use.                 | Included |
| Meraki switches should have a sensor that tracks the number of ports available.              | Included |

### Meraki Cameras

| Requirement                                                                           | Status   |
| :------------------------------------------------------------------------------------ | :------- |
| Meraki cameras should have a data element that reflects the URL of the camera stream. | Included |
| Meraki cameras should have a Home Assistant switch that enables RTSP streaming.       | Included |

### Meraki Sensors

| Requirement                                                                           | Status   |
| :------------------------------------------------------------------------------------ | :------- |
| Meraki sensors should have appropriate sensor and switch values based on their model. | Included |

## Technical Requirements

### Asynchronous Operations

| Requirement                                                         | Status   |
| :------------------------------------------------------------------ | :------- |
| All API calls and Home Assistant interactions must be asynchronous. | Included |

### Error Handling

| Requirement                                                                                 | Status   |
| :------------------------------------------------------------------------------------------ | :------- |
| The integration should handle API errors, network issues, and other exceptions gracefully.  | Included |
| Logging should be used for debugging and error reporting.                                   | Included |
| The integration must implement an adaptive back-off algorithm when 429 errors are detected. | Included |

### Data Coordination

| Requirement                                                                                    | Status   |
| :--------------------------------------------------------------------------------------------- | :------- |
| A DataUpdateCoordinator should be used to manage data updates and prevent excessive API calls. | Included |
| A separate coordinator should be created to manage the device creations.                       | Included |

### Configuration Flow

| Requirement                                                                                        | Status   |
| :------------------------------------------------------------------------------------------------- | :------- |
| The integration must provide a configuration flow for users to enter their Meraki API credentials. | Included |

### Home Assistant API

| Requirement                                                                       | Status   |
| :-------------------------------------------------------------------------------- | :------- |
| The integration must adhere to the Home Assistant API guidelines and conventions. | Included |

### Use of AIOHTTP

| Requirement                                     | Status   |
| :---------------------------------------------- | :------- |
| The Integration uses AIOHTTP for the API calls. | Included |

### Use of Voluptuous

| Requirement                                            | Status   |
| :----------------------------------------------------- | :------- |
| The Integration uses Voluptuous for schema validation. | Included |

### Testing & Hardening

| Requirement                                                                                                                                                                                          | Status   |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| The integration uses a non-blocking setup sequence where only Tier 1 data (basic device skeleton) is awaited during `async_setup_entry`. Heavy sensor data is fetched in the background.             | Included |
| Automated smoke tests must include a 90-second wait after integration initialization to allow the Meraki background coordinators to complete their initial data fetch before auditing logs or state. | Included |
| Staging smoke tests must audit entity states via the Home Assistant Template API to ensure no Meraki entities are in an 'unavailable' or 'unknown' state before passing.                             | Included |

\*\*Frontend Development (DEPRECATED - Removed in v2.3.0)

| Requirement                                                                                                                                     | Status  |
| :---------------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| Home Assistant Web Components must be explicitly registered in the global JSX namespace (e.g., `src/types/ha-frontend.d.ts`) for TypeScript.    | Removed |
| WebSocket commands used by the frontend must be centralized in a type-safe enum (e.g., `src/types/websocket.ts`).                               | Removed |
| Vite build must use a dedicated `dist` directory for `outDir` and explicitly define `src/main.tsx` as the entry point in `rollupOptions.input`. | Removed |
| The `index.html` file must point to the TypeScript source entry point to allow Vite to transform it during the build process.                   | Removed |

## Key Learnings from Debugging

| Requirement                                                                                | Status             |
| :----------------------------------------------------------------------------------------- | :----------------- |
| Import statements must be accurate and reflect the actual file structure and module names. | Included           |
| Caching can cause significant issues, requiring aggressive cache clearing.                 | Partially Included |
| Thorough logging is essential for debugging.                                               | Included           |
| The removal of a base class requires the functionality to be moved to the child class.     | N/A                |
| The **init**.py file is the central location for the integration's logic.                  | Included           |
| The use of the correct coordinator class is very important.                                | Included           |

## Future Work

### High Priority / Core Functionality

- [ ] **Refactor to use `core` components:** The highest priority is to refactor the codebase to use the new `core` components and remove the old, redundant code. This will involve updating the platforms to use the new `core` entities and coordinators, and removing the old API client, coordinators, and entities.
- [ ] **Improve Error Handling and Logging:** Enhance error catching, provide more user-friendly error messages, and ensure consistent logging across the integration.
- [ ] **Optimize Data Retrieval:** Review API call patterns to optimize for performance and minimize API rate limit impact, especially for large organizations.
- [ ] **Real-time Updates:** Investigate using webhooks or WebSockets for real-time data updates.

### New Features / Entities

- [ ] **Native HA Entity Integrations:**
  - [ ] **Native Firmware Management (`update` entity):** Allow users to view and trigger Meraki network upgrades natively from the HA UI.
  - [ ] **Edge Analytics & Presence (`binary_sensor` entity):** Feed MV camera object detection (e.g., person/vehicle) directly into HA for instant automation triggers.
  - [ ] **Network Device Tracking (`device_tracker` entity):** Use MR access point client associations for hyper-reliable, network-level presence tracking.
  - [ ] **PoE Port Control (`switch` entity):** Expose MS switch ports as native toggles to easily bounce PoE power for locked-up smart home devices.
  - [ ] **Dynamic Bandwidth Toggles (`select` or `switch` entity):** Allow users to toggle specific SSIDs or Traffic Shaping rules via standard HA dashboards.
- [ ] **Implement Switches for Internet Ports:** Allow control over WAN/Internet ports on MX appliances if API supports.
- [ ] **Device Services:** Add services to reboot a device and blink its LEDs.
- [ ] **Client List Sensor:** Add a sensor that provides a list of connected clients as an attribute.
- [ ] **Signal Strength and Data Usage Sensors for Connected Clients:** Create sensors to monitor signal strength (RSSI, SNR) and data usage (upload/download) for individual clients connected to Meraki APs.
- [ ] **More Sensor Types for SSIDs:** Add sensors for additional SSID properties, e.g., security settings (WPA type), traffic statistics (data usage per SSID), active bands.
- [ ] **Support for Additional Meraki Product Types/Features:**
  - [ ] More detailed MV camera features (e.g., motion events, specific stream controls beyond snapshot URLs if available).
  - [ ] SM (Systems Manager) endpoint monitoring/management if relevant for HA.
  - [ ] Deeper sensor data for MT series (e.g., historical data, more specific readings if available).
  - [ ] More detailed switch port statistics (e.g., per-port traffic, PoE details beyond basic count).
- [ ] **Firmware Update Sensors/Notifications:** Entities to indicate available firmware updates for devices or networks.
- [ ] **Network Health/Event Sensors:** Monitor overall network health or specific Meraki events/alerts.
- [ ] **Parental Controls & Content Filtering (MX Security Appliances):**
  - [ ] **Content Filtering Policy Switch:** Create a `select` entity to switch between content filtering policies.
  - [ ] **"Internet Time-Out" Switch per Device:** Create a `switch` entity to block internet access for specific clients.
- [ ] **Guest Wi-Fi Management (MR Access Points):**
  - [ ] **Guest Wi-Fi Password Control:** Create a `text` entity to manage the guest Wi-Fi password.
  - [x] **IPSK Lifecycle Management:** Implement a backend manager to track and reap temporary guest Identity PSKs (IPSKs) upon expiration, with persistent storage across reboots.
  - [x] **IPSK WebSocket API:** Implement a strict WebSocket API contract for IPSK management with camelCase payload keys and centralized command definitions.
  - [x] **IPSK Native Service Action:** Expose IPSK creation functionality as a standard Home Assistant Service Action, allowing users to create timed guest keys without the custom frontend panel.
  - [x] **Guest Wi-Fi Blueprint:** Provide a plug-and-play automation template for creating temporary guest keys via the `meraki_ha.create_guest_key` action.
  - [x] **Dual-WAN Failover Blueprint:** Provide an automation template for critical alerts when the primary internet connection fails on Meraki MX appliances.
  - [x] **IPSK Native UX Overhaul:** Rebuilt the TimedAccess.tsx component to provide a native Home Assistant experience using `ha-textfield`, `ha-select`, `ha-button`, and `ha-alert` web components.
  - [ ] **Enhanced Home Security & Awareness (MV Cameras & MT Sensors):**
  - [ ] **Camera Motion Events:** Create `binary_sensor` entities for camera motion events.
  - [ ] **Per-Client Presence Detection:** Enhance the device tracker to show which AP a client is connected to.
- [ ] **PoE Control for Smart Homes (MS Switches):**
  - [ ] **Per-Port PoE Control:** Create a `switch` entity for each PoE-capable port.
- [ ] **Blueprints (Automations):**
  - [ ] **EV Arrived Trigger:** Presence detection to trigger garage/lights.
  - [ ] **Dinner Time Policy Enforcer:** Scheduling Meraki Group Policies.
  - [ ] **Scheduled Guest Key:** Auto-generating and notifying service workers.
  - [ ] **Dead Node Auto-Heal:** Cycling PoE power if an HA entity goes unavailable.
  - [ ] **MT Sensor Threshold Alerts:** Critical notifications for temp/water.
- [ ] **Custom Lovelace Cards (Dashboards):**
  - [ ] **Event Host QR Generator:** Generating IPSK and rendering a QR code.
  - [ ] **Client Locator Glance Card:** Search for a client to see AP and RSSI.
  - [x] **Meraki Network Vitals Card:** Compact horizontal header for network health (Gateways, Switches, APs) and real-time WAN throughput.
  - [ ] **Smart PoE Port Toggle:** List ports, show power draw, toggle PoE state.

### Enhancements / Bug Fixes

- [ ] **Relaxed Tag Matching:** Add an option to allow for relaxed tag matching when associating SSIDs with wireless devices.
- [ ] **Configuration Option for SSID Sensor Selection:** Allow users to choose which specific sensors (availability, channel, client count, etc.) they want to enable per SSID to reduce entity clutter.
- [ ] **Customize Device and Entity Names:** Provide more advanced configuration options for customizing how Meraki device and entity names are generated in Home Assistant.
- [ ] **Full Home Assistant Branding Support:** Ensure the integration meets all requirements for Home Assistant branding, including logos and documentation links.
- [ ] **Address Specific Bugs:**
  - [ ] Review "Radio profiles are not returned for all MR devices" (from README known issues) and investigate if it's an API limitation or an integration issue.
- [ ] **Fix SSID entity `device_info`:** Correctly link to parent AP via `via_device` attribute in `MerakiEntity` for SSID-specific entities.
- [ ] **Tag-based SSID Control Review:** The current `MerakiSSIDSwitch` uses device tags to control SSID state. Evaluate if a more direct API method for enabling/disabling SSIDs per AP (if available and appropriate) would be better, or if the tag strategy is the most robust.

### Documentation

- [ ] **Troubleshooting Section:** Add a comprehensive troubleshooting section to `README.md` covering common issues (API key errors, rate limits, device discovery problems).
- [ ] **Configuration Guide:** Create a more detailed guide on configuring the integration, including explanations of all options in the config flow and options flow.
- [ ] **Update Documentation for SSID Device Creation:** Ensure documentation clearly explains how SSIDs are represented as devices and how their entities are structured.
- [ ] **MkDocs for Documentation Generation:** Set up MkDocs (or similar like Sphinx) for generating more structured and navigable documentation, potentially hosted on GitHub Pages.
- [ ] **Developer Documentation:** Add notes or a separate document for developers looking to contribute, explaining the coordinator structure, API client usage, and entity creation patterns.

### Code Quality & Refactoring

- [ ] **Unit and Integration Tests:** Expand test coverage significantly.

## Structural Improvements & Refactoring

| Improvement                                                                                                                                                           | Status   |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| **ACL Score Reduction:** Refactored complex sensor update functions in `device_status.py` and `base.py` to bring Agent Cognitive Load (ACL) scores below 10.          | Complete |
| **Logic Decomposition:** Extracted nested data parsing and status determination logic into single-responsibility helper functions (e.g., `_determine_device_status`). | Complete |
| **Strict Type Hinting:** Applied comprehensive Python type hints to all refactored functions to improve maintainability and catch potential errors early.             | Complete |
| **Helper Function Size Constraints:** Ensured all new helper functions remain strictly under 50 lines of code, promoting readability and ease of testing.             | Complete |
| **IPSK Manager Singleton:** Implemented a central `IPSKManager` singleton in `async_setup` to manage the lifecycle of guest PSKs across all config entries.           | Complete |
| **Custom Panel Removal:** Completely removed the custom React sidebar panel; all functionality (IPSK management) is now handled via native HA Service Actions and UI. | Complete |
