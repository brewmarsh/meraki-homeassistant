"""Wireless models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True)
class WirelessMixin:
    """Mixin for Meraki Wireless specific fields."""

    wireless_radio_settings: dict[str, Any] | None = None

    def wireless_to_dict(self) -> dict[str, Any]:
        """Convert wireless fields to dictionary."""
        return {"wirelessRadioSettings": self.wireless_radio_settings}

    @staticmethod
    def wireless_from_dict(data: dict[str, Any]) -> dict[str, Any]:
        """Parse wireless fields from dictionary."""
        return {"wireless_radio_settings": data.get("wirelessRadioSettings")}
