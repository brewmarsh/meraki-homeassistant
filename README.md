#   Meraki Home Assistant Integration

This Home Assistant integration allows you to monitor and manage your Cisco Meraki network, including devices, networks, and SSIDs. It leverages the Meraki API to bring data from your Meraki dashboard into Home Assistant, enabling you to gain insights into your network and automate actions based on its status.

##   Features

* **Device Discovery:** Automatically discovers Meraki hardware devices within your organization and networks.
* **Supported Devices:**
    * Wireless (MR/GR)
    * Switch (MX, MS)
    * Appliance
    * Camera
    * Sensor [cite: 3, 4, 5]
* **Entity Creation:** Creates Home Assistant entities for:
    * Meraki devices [cite: 14]
    * Meraki networks [cite: 15]
    * Meraki SSIDs (wireless networks) [cite: 16]
    * Meraki VLANs [cite: 17]
* **Data Monitoring:**
    * Device status
    * Connected clients (wireless, switches) [cite: 8]
    * Appliance data usage [cite: 17]
    * Appliance connected client count [cite: 18]
    * Switch PoE usage (if supported) [cite: 20, 21, 22]
    * Switch port usage (total, available)
    * Camera stream URL [cite: 23]
    * Sensor values (model-dependent) [cite: 25]
    * Radio settings (for Meraki MR devices)
    * Network client count
    * SSID Availability (Enabled/Disabled)
    * SSID Channel
    * SSID Client Count
* **Device Control:**
    * Camera RTSP streaming (enable/disable) [cite: 24]
* **Configuration:**
    * API key and Organization ID via Home Assistant configuration flow [cite: 30, 31]
    * Configurable scan interval [cite: 9, 12]
    * Device name formatting (prefixes, suffixes, omission of device type) [cite: 6]
    * Relaxed tag matching for SSIDs [cite: 13]
* **Authentication:**
    * Handles API key re-authentication [cite: 13]

##   Installation

###   Prerequisites

* Home Assistant installation
* Cisco Meraki API key [cite: 1, 2]
* Cisco Meraki Organization ID [cite: 2]

###   Installation

1.  ... (Instructions for installing the custom integration)
2.  Restart Home Assistant.

##   Configuration

1.  Go to "Settings" -> "Devices & Services" -> "Add Integration".
2.  Search for "Meraki HA" and follow the configuration prompts.
3.  The scan interval setting is used to define how often (in seconds) that the sensors and devices are updated. The default is 60, but should be adjusted based on the number of devices and networks that you have in order to ensure that you do not exceed a rate limit for your Meraki API calls.
4.  Optionally, you can set the device name format. [cite: 11, 12]

##   Obtaining a Meraki API Key

1.  ... (Instructions for obtaining an API key)

##   Entities Provided

* **Sensors:**
    * Device status
    * Connected clients
    * Radio settings
    * Network client count
    * SSID Availability (Enabled/Disabled)
    * SSID Channel
    * SSID Client Count
    * Appliance data usage [cite: 17]
    * Appliance connected client count [cite: 18]
    * Switch PoE usage (if supported) [cite: 20, 21, 22]
    * Switch port usage (total, available)
    * Sensor values (model-dependent) [cite: 25]
* **Devices:**
    * Meraki Devices (MR, MX, etc.) [cite: 14]
    * Meraki Networks [cite: 15]
    * Meraki SSIDs [cite: 16]
    * Meraki VLANs [cite: 19]

##   Dependencies

* `meraki` [cite: 32]
* `aiohttp` [cite: 32]

##   Known issues

* Radio profiles are not returned for all MR devices.

##   Disclaimer

This is a custom integration and has not been tested by Home Assistant. Use it at your own risk.

##   TODO

* Add signal strength and data usage sensors for connected clients.
* Add more sensor types for SSIDs.
* Add device tracker functionality. [cite: 9]
* Improve error handling and logging. [cite: 27, 28]
* Add service calls to enable/disable SSIDs.
* Set up MkDocs for documentation generation.
