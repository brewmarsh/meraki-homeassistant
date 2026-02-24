"""Wireless models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True)
class MerakiWirelessMixin:
    """Mixin for Meraki Wireless specific fields."""

    wireless_radio_settings: dict[str, Any] | None = None
