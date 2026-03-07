"""Constants for the Meraki integration core.

DEPRECATED: Use custom_components.meraki_ha.const_device instead.
"""

from __future__ import annotations

# Re-export from the new centralized location
from ..const_device import (  # noqa: F401
    DEFAULT_CAPS,
    DEVICE_CAPABILITIES,
    get_ssid_identifier,
)
