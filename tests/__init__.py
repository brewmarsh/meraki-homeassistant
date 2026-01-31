"""Tests for the Meraki integration."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

# Mock meraki if not installed to avoid ModuleNotFoundError during collection
try:
    import meraki  # noqa: F401
except ImportError:
    sys.modules["meraki"] = MagicMock()
    sys.modules["meraki.exceptions"] = MagicMock()

from typing import Any

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN

from .const import MERAKI_TEST_API_KEY, MERAKI_TEST_ORG_ID


async def async_get_config_entry(
    hass: HomeAssistant, data: dict[str, Any] | None = None
) -> MockConfigEntry:
    """Create a mock config entry for testing."""
    if data is None:
        data = {
            "meraki_api_key": MERAKI_TEST_API_KEY,
            "meraki_org_id": MERAKI_TEST_ORG_ID,
        }

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=data,
        entry_id="test",
    )
    config_entry.add_to_hass(hass)
    return config_entry
