# Meraki for Home Assistant

This is a custom component for integrating Cisco Meraki devices into Home Assistant.

## Features

This integration provides a wide range of entities for monitoring and controlling your Meraki networks and devices.

### Parental Controls

This integration includes parental control features that are automatically discovered based on the Meraki hardware in your network.

#### Category-Based Content Filtering (for Meraki MX Appliances)

If you have a Meraki MX security appliance on your network, this integration will create a series of switches, one for each available content filtering category (e.g., "Block Social Media", "Block Gambling", "Block Adult and Pornography").

*   **Hardware Requirement:** Meraki MX Series Security Appliance.
*   **Functionality:** Allows you to granularly block or allow specific categories of web content for your entire network.
*   **Entities:** These will appear as `switch` entities in Home Assistant.

#### Adult Content Filtering (for Meraki MR Access Points)

If you have Meraki MR wireless access points, the integration will create a switch for each SSID that is configured in "NAT mode". This switch controls Meraki's simple, one-click "Adult Content Filtering" feature.

*   **Hardware Requirement:** Meraki MR Series Wireless Access Point.
*   **Configuration Requirement:** The SSID must be in "NAT mode".
*   **Functionality:** A simple on/off toggle to block a predefined list of adult content.
*   **Entities:** These will appear as `switch` entities, one for each eligible SSID (e.g., "Adult Content Filtering on Guest WiFi").

### Note on Using Both MX and MR Filtering

If your network includes both an MX appliance and MR access points, it is recommended to use the more powerful and granular content filtering on the MX as your single source of truth for parental controls. You can manage all your desired categories on the MX and should leave the "Adult Content Filtering" feature disabled on your individual SSIDs to avoid confusion and conflicting policies. The most restrictive policy will always win.
