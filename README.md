#   Meraki Home Assistant Integration

This Home Assistant integration allows you to monitor and manage your Cisco Meraki network, including devices, networks, and SSIDs. It leverages the Meraki API to bring data from your Meraki dashboard into Home Assistant, enabling you to gain insights into your network and automate actions based on its status.

##   Features

* **Device Discovery:** Automatically discovers Meraki hardware devices within your organization and networks.
* **Supported Devices:**
    * Wireless (MR/GR)
    * Switch (MX, MS)
    * Appliance
    * Camera
    * Sensor
* **Entity Creation:** Creates Home Assistant entities for:
    * Meraki devices
    * Meraki networks
    * Meraki SSIDs (wireless networks)
    * Meraki VLANs
* **Data Monitoring:**
    * Device status
    * Connected clients (wireless, switches)
    * Appliance data usage
    * Appliance connected client count
    * Switch PoE usage (if supported)
    * Switch port usage (total, available)
    * Camera stream URL
    * Sensor values (model-dependent)
    * Radio settings (for Meraki MR devices)
    * Network client count
    * SSID Availability (Enabled/Disabled)
    * SSID Channel
    * SSID Client Count
* **Device Control:**
    * Camera RTSP streaming (enable/disable)
* **Configuration:**
    * API key and Organization ID via Home Assistant configuration flow
    * Configurable scan interval
    * Device name formatting (prefixes, suffixes, omission of device type)
    * Relaxed tag matching for SSIDs
* **Authentication:**
    * Handles API key re-authentication

##   Installation

###   Prerequisites

* Home Assistant installation
* Cisco Meraki API key
* Cisco Meraki Organization ID

###   Installation

1.  ... (Instructions for installing the custom integration)
2.  Restart Home Assistant.

##   Configuration

1.  Go to "Settings" -> "Devices & Services" -> "Add Integration".
2.  Search for "Meraki HA" and follow the configuration prompts.
3.  The scan interval setting is used to define how often (in seconds) that the sensors and devices are updated. The default is 60, but should be adjusted based on the number of devices and networks that you have in order to ensure that you do not exceed a rate limit for your Meraki API calls.
4.  Optionally, you can set the device name format.

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
    * Appliance data usage
    * Appliance connected client count
    * Switch PoE usage (if supported)
    * Switch port usage (total, available)
    * Sensor values (model-dependent)
* **Devices:**
    * Meraki Devices (MR, MX, etc.)
    * Meraki Networks
    * Meraki SSIDs
    * Meraki VLANs

##   Dependencies

* `meraki`
* `aiohttp`

##   Known issues

* Radio profiles are not returned for all MR devices.

##   Disclaimer

This is a custom integration and has not been tested by Home Assistant. Use it at your own risk.

##   TODO

* Add signal strength and data usage sensors for connected clients.
* Add more sensor types for SSIDs.
* Add device tracker functionality.
* Improve error handling and logging.
* Add service calls to enable/disable SSIDs.
* Set up MkDocs for documentation generation.
