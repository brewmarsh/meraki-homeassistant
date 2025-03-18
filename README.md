# Meraki Integration for Home Assistant

This Home Assistant integration provides sensors and devices for your
Meraki network, including devices, networks, and SSIDs.

## Features

- **Device Status:** Monitor the status of your Meraki devices (MR, MX, etc.).
- **Connected Clients:** Track the number of clients connected to your
  Meraki access points.
- **Radio Settings:** View wireless radio settings for your Meraki MR
  devices.
- **Network Client Count:** Monitor the number of clients connected to each
  Meraki network.
- **SSID Status:** Track the availability, channel, and client count of your
  Meraki SSIDs as individual Home Assistant devices.

## Installation

1. ... (Instructions for installing the custom integration)
2. Restart Home Assistant.

## Configuration

1. Go to "Settings" -> "Devices & Services" -> "Add Integration".
2. Search for "Meraki HA" and follow the configuration prompts.
3. The scan interval setting is used to define how often (in seconds) that
   the sensors and devices are updated. The default is 60, but should be adjusted
   based on the number of devices and networks that you have in order to ensure
   that you do not exceed a rate limit for your Meraki API calls.
4. Optionally, you can set the device name format.

## Obtaining a Meraki API Key

1. ... (Instructions for obtaining an API key)

## Entities Provided

- **Sensors:**
- Device status
- Connected clients
- Radio settings
- Network client count
- SSID Availability (Enabled/Disabled)
- SSID Channel
- SSID Client Count
- **Devices:**
- Meraki Devices (MR, MX, etc.)
- Meraki Networks
- Meraki SSIDs

## Dependencies

- `meraki`
- `aiohttp`

## Known issues

- Radio profiles are not returned for all MR devices.

## Disclaimer

This is a custom integration and has not been tested by Home Assistant.
Use it at your own risk.

## TODO

- Add signal strength and data usage sensors for connected clients.
- Add more sensor types for SSIDs.
- Add device tracker functionality.
- Improve error handling and logging.
- Add service calls to enable/disable SSIDs.
