"""Switch models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(kw_only=True)
class MerakiSwitchMixin:
    """Mixin for Meraki Switch specific fields."""

    ports_statuses: list[dict[str, Any]] = field(default_factory=list)
