"""Switch models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
