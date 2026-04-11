"""Wireless models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import MerakiBaseDevice


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


@dataclass(kw_only=True)
class MerakiWirelessDevice(MerakiBaseDevice, WirelessMixin):
    """Dataclass for a Meraki Wireless device."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = self.base_to_dict()
        data.update(self.wireless_to_dict())
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiWirelessDevice:
        """Create a MerakiWirelessDevice from a dictionary."""
        kwargs = cls.base_from_dict(data)
        kwargs.update(cls.wireless_from_dict(data))
        return cls(**kwargs)
