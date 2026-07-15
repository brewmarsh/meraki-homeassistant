"""Webhook related constants."""

from __future__ import annotations

from typing import Final

WEBHOOK_ID_FORMAT: Final = "meraki_ha_webhook_{entry_id}"
EVENT_MERAKI_WEBHOOK_ALERT: Final = "meraki_ha_webhook_alert"

# Alert Types
ALERT_TYPE_AP_DOWN: Final = "APs went down"
ALERT_TYPE_MOTION_DETECTED: Final = "Motion detected"
ALERT_TYPE_PERSON_DETECTED: Final = "Person detected"
ALERT_TYPE_CLIENT_CONNECTIVITY: Final = "Client connectivity changed"

# Event Types
EVENT_TYPE_DEVICES_SEEN: Final = "DevicesSeen"
