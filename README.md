# Meraki Home Assistant Integration

This Home Assistant integration allows you to monitor and manage your Cisco Meraki network devices and services. By leveraging the Meraki Dashboard API, it brings data from your Meraki organization into Home Assistant, enabling enhanced network visibility, automation, and control within your smart home environment.

## Documentation

**For detailed setup instructions, configuration options, entity descriptions, troubleshooting, and more, please visit our [full documentation site](https://YOUR_USER_OR_ORG.github.io/YOUR_REPO_NAME/).** (Replace placeholders with your actual GitHub Pages URL).

The documentation site includes:
*   Comprehensive installation and configuration guides.
*   Detailed explanations of all entities provided by the integration.
*   Troubleshooting tips for common issues.
*   Technical overview for developers.

## Key Features

*   **Device Discovery:** Automatically discovers Meraki hardware (APs, switches, security appliances, cameras, sensors) within your organization.
*   **Rich Entity Creation:** Creates a variety of Home Assistant entities for:
    *   Meraki hardware devices
    *   Logical Meraki networks
    *   Wireless SSIDs
    *   (Potentially VLANs, depending on implementation details)
*   **Extensive Data Monitoring:** Provides sensors for:
    *   Device status (online/offline, product type)
    *   Connected client counts (per AP, per network, per SSID)
    *   Network uplink status and appliance data usage (for MX series)
    *   Switch PoE and port usage (for MS series)
    *   Camera stream URLs (for MV series)
    *   Environmental sensor values (for MT series)
    *   Wireless AP radio settings and SSID operational status (channel, availability).
*   **Control Capabilities:** (Examples, actual controls may vary)
    *   Enable/disable SSIDs on access points (typically via device tag manipulation).
    *   Control camera RTSP streaming.
*   **User-Friendly Configuration:**
    *   Simple setup via Home Assistant UI (API Key, Organization ID).
    *   Configurable options: API polling interval, device name formatting, relaxed tag matching for SSID control.
*   **Authentication Handling:** Manages API key authentication and supports re-authentication flows.

## Installation

### Prerequisites

*   A running Home Assistant instance.
*   A Cisco Meraki Dashboard API key with appropriate permissions.
*   Your Cisco Meraki Organization ID.

### Recommended Method: HACS (Home Assistant Community Store)

1.  Ensure HACS is installed in your Home Assistant.
2.  In HACS, go to "Integrations", click "Explore & Add Repositories".
3.  Search for "Meraki HA Integration" (or its registered name) and install it.
4.  Restart Home Assistant.

For manual installation steps and detailed instructions on obtaining your Meraki API key and Organization ID, please refer to the [Installation and Configuration page on our documentation site](https://YOUR_USER_OR_ORG.github.io/YOUR_REPO_NAME/configuration/).

## Configuration

After installation and restarting Home Assistant:

1.  Navigate to **Settings** > **Devices & Services**.
2.  Click **+ ADD INTEGRATION** and search for "Meraki HA".
3.  Follow the on-screen prompts to enter your API Key, Organization ID, and initial options.

For a complete guide to all configuration options, see the [documentation site](https://YOUR_USER_OR_ORG.github.io/YOUR_REPO_NAME/configuration/).

## Entities Provided

This integration creates various entities. For a comprehensive list and descriptions, please see the [Entities page on our documentation site](https://YOUR_USER_OR_ORG.github.io/YOUR_REPO_NAME/entities/).

Summary:
*   **Sensors:** Device status, connected client counts (per device, network, SSID), radio settings, network uplink/usage, SSID availability & channel, etc.
*   **Switches:** SSID enable/disable controls, camera RTSP stream toggle.
*   **Device Trackers:** Represents Meraki hardware devices, showing connectivity based on client presence on the device itself.
*   **Home Assistant Devices:** Registers Meraki hardware, networks, and SSIDs as "devices" in the HA device registry for better organization.

## Dependencies

*   `meraki` (Official Cisco Meraki Dashboard API Python library)
*   `aiohttp` (For asynchronous HTTP requests)

These are typically installed automatically by Home Assistant.

## Known Issues

Please refer to the [Troubleshooting page on our documentation site](https://YOUR_USER_OR_ORG.github.io/YOUR_REPO_NAME/troubleshooting/) for known issues and common solutions.
*(Example: Radio profiles may not be available for all MR device models.)*

## Disclaimer

This is a community-developed custom integration. It is not officially endorsed by Cisco Meraki or Home Assistant. Use at your own risk.

## TODO / Future Enhancements

The following are planned or potential areas for improvement. Contributions are welcome!

*   **Client-Specific Sensors:** Add sensors for individual connected clients (e.g., signal strength, data usage per client).
*   **Expanded SSID Sensors:** Introduce more detailed sensors for SSIDs (e.g., specific authentication modes, encryption types).
*   **Advanced Device Tracker:** Enhance device tracker functionality, potentially to track specific client devices rather than just Meraki hardware presence.
*   **Error Handling & Logging:** Continuously refine error handling for API interactions and improve the clarity and utility of diagnostic logging. (Note: Recent documentation efforts have improved clarity on existing error handling).
*   **Service Calls:** Implement more Home Assistant services for advanced control (e.g., more granular SSID settings, port controls for switches, rebooting devices).
*   **Support for More Device Features:** Extend support for other Meraki device capabilities as exposed by the API (e.g., more sensor types for MT, advanced switch configurations).

Please check the project's issue tracker on GitHub for more detailed tasks and ongoing discussions.
