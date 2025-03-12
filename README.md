# Meraki Integration for Home Assistant

This Home Assistant integration provides sensors for your Meraki devices.

## Installation

1. ... (Instructions for installing the custom integration)
2. Restart Home Assistant.

## Configuration

1. Go to "Settings" -> "Devices & Services" -> "Add Integration".
2. Search for "Meraki HA" and follow the configuration prompts.
3. The scan interval setting is used to define how often (in seconds) that the
   sensors are updated. The default is 60, but should be adjusted based on the
   number of devices that you have in order to ensure that you do not exceed a
   rate limit for your Meraki API calls.

## Obtaining a Meraki API Key

1. ... (Instructions for obtaining an API key)

## Dependencies

- `meraki`
- `aiohttp`

## Known issues

- radio profiles are not returned for all MR devices

## Disclaimer

This is a custom integration and has not been tested by Home Assistant.
Use it at your own risk.
