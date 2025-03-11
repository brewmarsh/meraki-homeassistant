"""Constants for the meraki_ha integration."""

DOMAIN = "meraki_ha"
"""Domain for the component."""

CONF_MERAKI_API_KEY = "meraki_api_key"
"""Configuration key for the Meraki API key."""

CONF_MERAKI_ORG_ID = "meraki_org_id"
"""Configuration key for the Meraki organization ID."""

DATA_CLIENT = "client"
"""Key for storing the Meraki API client in Home Assistant's data."""

DATA_COORDINATOR = "coordinator"
"""Key for storing the Meraki data coordinator in Home Assistant's data."""

PLATFORMS = ["sensor"]
"""List of platforms supported by the integration."""

DEFAULT_SCAN_INTERVAL = 60
"""Default scan interval for the Meraki API data."""