"""Switch models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import MerakiBaseDevice


@dataclass(kw_only=True)
class SwitchMixin:
    """Mixin for Meraki Switch specific fields."""

    switch_ports: list[dict[str, Any]] = field(default_factory=list)

    def switch_to_dict(self) -> dict[str, Any]:
        """Convert switch fields to dictionary."""
        return {"portsStatuses": self.switch_ports}

    @staticmethod
    def switch_from_dict(data: dict[str, Any]) -> dict[str, Any]:
        """Parse switch fields from dictionary."""
        return {"switch_ports": data.get("portsStatuses", [])}


@dataclass(kw_only=True)
class MerakiSwitchDevice(MerakiBaseDevice, SwitchMixin):
    """Dataclass for a Meraki Switch."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = self.base_to_dict()
        data.update(self.switch_to_dict())
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiSwitchDevice:
        """Create a MerakiSwitchDevice from a dictionary."""
        kwargs = cls.base_from_dict(data)
        kwargs.update(cls.switch_from_dict(data))
        return cls(**kwargs)
