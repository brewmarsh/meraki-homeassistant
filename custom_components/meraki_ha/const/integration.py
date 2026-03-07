"""Constants for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "meraki_ha"
MANUFACTURER: Final = "Cisco Meraki"
VERSION: Final = "2.4.0"

# Merged Constants - Adopting beta's explicit naming style with fix's descriptive value
WEBHOOK_ID_FORMAT: Final = "meraki_ha_webhook_{entry_id}"
DATA_CLIENT: Final = "meraki_client"

EVENT_MERAKI_WEBHOOK_ALERT: Final = "meraki_ha_webhook_alert"

# WebSocket Commands
WS_CMD_GET_CONFIG: Final = "meraki_ha/get_config"
WS_CMD_SUBSCRIBE_MERAKI_DATA: Final = "meraki_ha/subscribe_meraki_data"
WS_CMD_GET_CAMERA_STREAM_URL: Final = "meraki_ha/get_camera_stream_url"
WS_CMD_GET_CAMERA_SNAPSHOT: Final = "meraki_ha/get_camera_snapshot"
WS_CMD_GET_VERSION: Final = "meraki_ha/get_version"
WS_CMD_GET_NETWORK_EVENTS: Final = "meraki_ha/get_network_events"
WS_CMD_UPDATE_OPTIONS: Final = "meraki_ha/update_options"
WS_CMD_UPDATE_ENABLED_NETWORKS: Final = "meraki_ha/update_enabled_networks"
WS_CMD_GET_GUEST_KEYS: Final = "meraki_ha/ipsk/get"
WS_CMD_CREATE_GUEST_KEY: Final = "meraki_ha/ipsk/create"
WS_CMD_REVOKE_GUEST_KEY: Final = "meraki_ha/ipsk/revoke"
WS_CMD_TIMED_ACCESS_GET_POLICIES: Final = "meraki_ha/timed_access/get_policies"
