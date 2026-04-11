"""Organization models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(kw_only=True)
class MerakiOrganization:
    """Dataclass for a Meraki organization."""

    id: str | None = None
    name: str | None = None
    url: str | None = None
    api: dict[str, Any] = field(default_factory=dict)
    cloud: dict[str, Any] = field(default_factory=dict)
    management: dict[str, Any] = field(default_factory=dict)
    licensing: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiOrganization:
        """Create a MerakiOrganization instance from a dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            url=data.get("url"),
            api=data.get("api", {}),
            cloud=data.get("cloud", {}),
            management=data.get("management", {}),
            licensing=data.get("licensing", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "api": self.api,
            "cloud": self.cloud,
            "management": self.management,
            "licensing": self.licensing,
        }
