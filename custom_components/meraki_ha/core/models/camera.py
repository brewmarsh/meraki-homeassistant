"""Camera models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(kw_only=True)
class MerakiCameraMixin:
    """Mixin for Meraki Camera specific fields."""

    video_settings: dict[str, Any] | None = None
    rtsp_url: str | None = None
    sense_settings: dict[str, Any] | None = None
    analytics: list[dict[str, Any]] = field(default_factory=list)
