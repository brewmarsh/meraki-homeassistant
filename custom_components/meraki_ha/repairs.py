"""Repairs support for Meraki."""

from __future__ import annotations

from homeassistant.components.repairs import RepairsFlow
from homeassistant.core import HomeAssistant
from homeassistant.helpers.issue_registry import IssueSeverity, async_create_issue

from .const import DOMAIN


# --- KEEP YOUR EXISTING LOGIC ---
async def async_create_api_key_issue(hass: HomeAssistant, entry_id: str) -> None:
    """Create an issue for an invalid API key."""
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


async def async_create_fix_flow(
    hass: HomeAssistant,
    issue_id: str,
    data: dict[str, str | int | float | None] | None,
) -> RepairsFlow | None:
    """Create a repairs flow for a specific issue.

    This function is required by Home Assistant to prevent
    the 'Invalid repairs platform' error.
    """
    # If the user clicks "FIX" on the invalid_api_key issue,
    # we currently don't have a custom wizard, so we return None.
    return None
