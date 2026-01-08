"""
Service for camera-related logic.

This module defines the CameraService class, which encapsulates the business
logic for handling Meraki cameras. It uses the CameraRepository to interact
with the API and provides a clean interface for other parts of the integration.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..core.repositories.camera_repository import CameraRepository


_LOGGER = logging.getLogger(__name__)


class CameraService:
    """Service for camera-related business logic."""

    def __init__(self, repository: CameraRepository) -> None:
        """Initialize the camera service."""
        self._repository = repository

    async def get_supported_analytics(self, serial: str) -> list[str]:
        """Get the list of supported analytics features for a camera."""
        features = await self._repository.get_camera_features(serial)
        analytics = [
            feature
            for feature in features
            if feature in ["person_detection", "vehicle_detection"]
        ]
        return analytics

    async def get_analytics_data(
        self, serial: str, object_type: str
    ) -> list[dict[str, Any]] | None:
        """Get the latest analytics data for a camera."""
        return await self._repository.get_analytics_data(serial, object_type)

    async def get_video_stream_url(self, serial: str) -> str | None:
        """Get the video stream URL for a camera (RTSP or cloud)."""
        # First try to get cloud video link (works for more camera models)
        cloud_url = await self._repository.async_get_cloud_video_url(serial)
        if cloud_url:
            return cloud_url
        # Fall back to RTSP URL
        return await self._repository.async_get_rtsp_stream_url(serial)

    async def get_rtsp_stream_url(self, serial: str) -> str | None:
        """Get the RTSP stream URL for a camera."""
        return await self._repository.async_get_rtsp_stream_url(serial)

    async def get_cloud_video_url(self, serial: str) -> str | None:
        """Get the cloud video URL for a camera."""
        return await self._repository.async_get_cloud_video_url(serial)

    async def get_camera_snapshot(self, serial: str) -> str | None:
        """Get a camera snapshot URL."""
        return await self.generate_snapshot(serial)

    async def get_motion_history(self, serial: str) -> list[dict[str, Any]]:
        """
        Get the motion history for a camera.

        This method fetches both person and vehicle detection history and
        combines them to represent general motion.
        """
        person_history = await self.get_analytics_data(serial, "person")
        vehicle_history = await self.get_analytics_data(serial, "vehicle")

        motion_events = []
        if person_history:
            motion_events.extend(person_history)
        if vehicle_history:
            motion_events.extend(vehicle_history)

        return motion_events

    async def generate_snapshot(self, serial: str) -> str | None:
        """Generate a snapshot and return the URL."""
        return await self._repository.generate_snapshot(serial)

    async def async_set_rtsp_stream_enabled(self, serial: str, enabled: bool) -> None:
        """Enable or disable RTSP stream for a camera."""
        await self._repository.set_rtsp_stream_enabled(serial, enabled)
