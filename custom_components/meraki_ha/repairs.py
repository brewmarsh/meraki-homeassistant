"""Repairs support for Meraki."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.issue_registry import IssueSeverity, async_create_issue

from .const import DOMAIN


async def async_create_api_key_issue(hass: HomeAssistant, entry_id: str) -> None:
    """
    Create an issue for an invalid API key.

    Args:
    ----
        hass: The Home Assistant instance.
        entry_id: The ID of the config entry.

    """
    async_create_issue(
        hass,
        DOMAIN,
        "invalid_api_key",
        is_fixable=True,
        is_persistent=True,
        severity=IssueSeverity.ERROR,
        translation_key="invalid_api_key",
        data={"entry_id": entry_id},
    )
