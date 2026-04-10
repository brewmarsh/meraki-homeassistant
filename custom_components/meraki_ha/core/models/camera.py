"""Camera models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import MerakiBaseDevice


@dataclass(kw_only=True)
class CameraMixin:
    """Mixin for Meraki Camera specific fields."""

    video_settings: dict[str, Any] | None = None
    rtsp_url: str | None = None
    sense_settings: dict[str, Any] | None = None
    camera_analytics: list[dict[str, Any]] = field(default_factory=list)

    def camera_to_dict(self) -> dict[str, Any]:
        """Convert camera fields to dictionary."""
        return {
            "videoSettings": self.video_settings,
            "rtspUrl": self.rtsp_url,
            "senseSettings": self.sense_settings,
            "analytics": self.camera_analytics,
        }

    @staticmethod
    def camera_from_dict(data: dict[str, Any]) -> dict[str, Any]:
        """Parse camera fields from dictionary."""
        return {
            "video_settings": data.get("videoSettings"),
            "rtsp_url": data.get("rtspUrl"),
            "sense_settings": data.get("senseSettings"),
            "camera_analytics": data.get("analytics", []),
        }


@dataclass(kw_only=True)
class MerakiCameraDevice(MerakiBaseDevice, CameraMixin):
    """Dataclass for a Meraki Camera."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = self.base_to_dict()
        data.update(self.camera_to_dict())
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiCameraDevice:
        """Create a MerakiCameraDevice from a dictionary."""
        kwargs = cls.base_from_dict(data)
        kwargs.update(cls.camera_from_dict(data))
        return cls(**kwargs)
