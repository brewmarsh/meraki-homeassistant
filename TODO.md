# TODO List for Meraki Home Assistant Integration

## High Priority / Core Functionality

- [ ] **Refactor to use `core` components:** The highest priority is to refactor the codebase to use the new `core` components and remove the old, redundant code. This will involve updating the platforms to use the new `core` entities and coordinators, and removing the old API client, coordinators, and entities.
- [ ] **Improve Error Handling and Logging:** Enhance error catching, provide more user-friendly error messages, and ensure consistent logging across the integration.
- [ ] **Optimize Data Retrieval:** Review API call patterns to optimize for performance and minimize API rate limit impact, especially for large organizations.

## New Features / Entities

- [ ] **Implement Switches for Internet Ports:** Allow control over WAN/Internet ports on MX appliances if API supports.
- [ ] **Signal Strength and Data Usage Sensors for Connected Clients:** Create sensors to monitor signal strength (RSSI, SNR) and data usage (upload/download) for individual clients connected to Meraki APs.
- [ ] **More Sensor Types for SSIDs:** Add sensors for additional SSID properties, e.g., security settings (WPA type), traffic statistics (data usage per SSID), active bands.
- [ ] **Support for Additional Meraki Product Types/Features:**
  - [ ] More detailed MV camera features (e.g., motion events, specific stream controls beyond snapshot URLs if available).
  - [ ] SM (Systems Manager) endpoint monitoring/management if relevant for HA.
  - [ ] Deeper sensor data for MT series (e.g., historical data, more specific readings if available).
  - [ ] More detailed switch port statistics (e.g., per-port traffic, PoE details beyond basic count).
- [ ] **Firmware Update Sensors/Notifications:** Entities to indicate available firmware updates for devices or networks.
- [ ] **Network Health/Event Sensors:** Monitor overall network health or specific Meraki events/alerts.

## Enhancements / Bug Fixes

- [ ] **Configuration Option for SSID Sensor Selection:** Allow users to choose which specific sensors (availability, channel, client count, etc.) they want to enable per SSID to reduce entity clutter.
- [ ] **Customize Device and Entity Names:** Provide more advanced configuration options for customizing how Meraki device and entity names are generated in Home Assistant.
- [ ] **Full Home Assistant Branding Support:** Ensure the integration meets all requirements for Home Assistant branding, including logos and documentation links.
- [ ] **Address Specific Bugs:**
  - [ ] Review "Radio profiles are not returned for all MR devices" (from README known issues) and investigate if it's an API limitation or an integration issue.
- [ ] **Fix SSID entity `device_info`:** Correctly link to parent AP via `via_device` attribute in `MerakiEntity` for SSID-specific entities.
- [ ] **Tag-based SSID Control Review:** The current `MerakiSSIDSwitch` uses device tags to control SSID state. Evaluate if a more direct API method for enabling/disabling SSIDs per AP (if available and appropriate) would be better, or if the tag strategy is the most robust.
- [ ] **VLAN Entity Clarification:** Determine if "Meraki VLANs" should be actual HA entities/devices or if VLAN information is purely contextual data for other entities. Adjust documentation and entity creation accordingly.

## Documentation

- [ ] **Troubleshooting Section:** Add a comprehensive troubleshooting section to `README.md` covering common issues (API key errors, rate limits, device discovery problems).
- [ ] **Configuration Guide:** Create a more detailed guide on configuring the integration, including explanations of all options in the config flow and options flow.
- [ ] **Update Documentation for SSID Device Creation:** Ensure documentation clearly explains how SSIDs are represented as devices and how their entities are structured.
- [ ] **MkDocs for Documentation Generation:** Set up MkDocs (or similar like Sphinx) for generating more structured and navigable documentation, potentially hosted on GitHub Pages.
- [ ] **Developer Documentation:** Add notes or a separate document for developers looking to contribute, explaining the coordinator structure, API client usage, and entity creation patterns.

## Code Quality & Refactoring

- [ ] **Unit and Integration Tests:** Expand test coverage significantly.
