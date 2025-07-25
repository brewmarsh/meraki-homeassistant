# TODO List for Meraki Home Assistant Integration

## High Priority / Core Functionality

- [ ] **Improve Error Handling and Logging:** Enhance error catching, provide more user-friendly error messages, and ensure consistent logging across the integration.
- [ ] **Optimize Data Retrieval:** Review API call patterns to optimize for performance and minimize API rate limit impact, especially for large organizations.
- [ ] **Refactor and Reorganize Sensor Files:** Consolidate sensor entity creation and potentially use a more centralized approach for defining sensor types to improve maintainability. _(From existing TODO)_

## New Features / Entities

- [ ] **Implement Switches for Internet Ports:** Allow control over WAN/Internet ports on MX appliances if API supports. _(From existing TODO)_
- [ ] **Signal Strength and Data Usage Sensors for Connected Clients:** Create sensors to monitor signal strength (RSSI, SNR) and data usage (upload/download) for individual clients connected to Meraki APs. _(From README TODO & existing TODO)_
- [ ] **More Sensor Types for SSIDs:** Add sensors for additional SSID properties, e.g., security settings (WPA type), traffic statistics (data usage per SSID), active bands. _(From README TODO & existing TODO)_
- [x] **Device Tracker for Connected Clients:** Implemented for tracking individual client devices.
- [ ] **Service Calls to Enable/Disable SSIDs (Directly):** Add service calls to directly control the administrative status of SSIDs via their API endpoints (if different from the current tag-based approach for `MerakiSSIDSwitch`). _(From README TODO & existing TODO)_
- [ ] **Support for Additional Meraki Product Types/Features:**
  - [ ] More detailed MV camera features (e.g., motion events, specific stream controls beyond snapshot URLs if available). _(Enhancement from existing TODO: "Implement support for other Meraki product types")_
  - [ ] SM (Systems Manager) endpoint monitoring/management if relevant for HA. _(Enhancement from existing TODO)_
  - [ ] Deeper sensor data for MT series (e.g., historical data, more specific readings if available).
  - [ ] More detailed switch port statistics (e.g., per-port traffic, PoE details beyond basic count).
- [ ] **Clarify and document/implement Camera Snapshot URL generation (is it a sensor attribute, service, or needs full implementation?).**
- [ ] **Firmware Update Sensors/Notifications:** Entities to indicate available firmware updates for devices or networks.
- [ ] **Network Health/Event Sensors:** Monitor overall network health or specific Meraki events/alerts.

## Enhancements / Bug Fixes

- [ ] **Configuration Option for SSID Sensor Selection:** Allow users to choose which specific sensors (availability, channel, client count, etc.) they want to enable per SSID to reduce entity clutter. _(From existing TODO)_
- [ ] **Customize Device and Entity Names:** Provide more advanced configuration options for customizing how Meraki device and entity names are generated in Home Assistant. _(From existing TODO)_
- [x] **Convert to using the Meraki Python Library:** Integration uses `meraki.aio.AsyncDashboardAPI`. The `meraki_api/_api_client.py` is a wrapper for this.
- [ ] **Full Home Assistant Branding Support:** Ensure the integration meets all requirements for Home Assistant branding, including logos and documentation links. _(From existing TODO)_
- [ ] **Address Specific Bugs:** (Add specific bug descriptions here as they are identified). _(From existing TODO)_
  - [ ] Review "Radio profiles are not returned for all MR devices" (from README known issues) and investigate if it's an API limitation or an integration issue.
- [ ] **Review API Client (`_api_client.py`):**
  - - [x] Consider implementing a shared `aiohttp.ClientSession`... (Handled by the `meraki` library itself).
  - - [ ] Refine error handling in `_async_api_request`... (Obsolete, `_api_client.py` wraps the SDK, does not have this method).
- [ ] **Fix SSID entity `device_info` to correctly link to parent AP via `via_device` attribute in `MerakiEntity` for SSID-specific entities.**
- [ ] **Tag-based SSID Control Review:** The current `MerakiSSIDSwitch` uses device tags to control SSID state. Evaluate if a more direct API method for enabling/disabling SSIDs per AP (if available and appropriate) would be better, or if the tag strategy is the most robust.
- [ ] **VLAN Entity Clarification:** Determine if "Meraki VLANs" should be actual HA entities/devices or if VLAN information is purely contextual data for other entities. Adjust documentation and entity creation accordingly.

## Documentation

- [ ] **Troubleshooting Section:** Add a comprehensive troubleshooting section to `README.md` covering common issues (API key errors, rate limits, device discovery problems). _(From existing TODO)_
- [ ] **Configuration Guide:** Create a more detailed guide on configuring the integration, including explanations of all options in the config flow and options flow. _(From existing TODO)_
- [ ] **Update Documentation for SSID Device Creation:** Ensure documentation clearly explains how SSIDs are represented as devices and how their entities are structured. _(From existing TODO)_
- [ ] **MkDocs for Documentation Generation:** Set up MkDocs (or similar like Sphinx) for generating more structured and navigable documentation, potentially hosted on GitHub Pages. _(From README TODO & existing TODO)_
- [ ] **Developer Documentation:** Add notes or a separate document for developers looking to contribute, explaining the coordinator structure, API client usage, and entity creation patterns.

## Code Quality & Refactoring

- [ ] **Review Placeholder Functions:** Identify and implement any placeholder functions (like `get_network_ids_and_names` in `sensor/__init__.py` or API methods in `meraki_api/` that were marked as placeholders) with actual API calls.
- [ ] **Consolidate Redundant Code:** Review for any redundant classes or functions (e.g., duplicate `MerakiNetworkClientCountSensor` in `network_clients.py` and `network_status.py`).
- [ ] **Unit and Integration Tests:** Expand test coverage significantly.
