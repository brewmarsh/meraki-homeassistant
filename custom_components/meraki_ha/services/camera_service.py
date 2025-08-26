"""
Service for camera-related logic.

This module defines the CameraService class, which encapsulates the business
logic for handling Meraki cameras. It uses the CameraRepository to interact
with the API and provides a clean interface for other parts of the integration.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from ..core.repositories.camera_repository import CameraRepository


_LOGGER = logging.getLogger(__name__)


class CameraService:
    """Service for camera-related business logic."""

    def __init__(self, repository: CameraRepository) -> None:
        """Initialize the camera service."""
        self._repository = repository

    async def get_supported_analytics(self, serial: str) -> List[str]:
        """
        Get the list of supported analytics features for a camera.
        """
        features = await self._repository.get_camera_features(serial)
        analytics = [
            feature
            for feature in features
            if feature in ["person_detection", "vehicle_detection"]
        ]
        return analytics

    async def get_analytics_data(self, serial: str) -> Optional[Dict[str, Any]]:
        """Get the latest analytics data for a camera."""
        return await self._repository.get_analytics_data(serial)

    async def get_video_stream_url(self, serial: str) -> Optional[str]:
        """Get the video stream URL for a camera."""
        return await self._repository.get_video_url(serial)

    async def get_motion_history(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Get the motion history for a network."""
        # The API provides 'person' or 'vehicle' object types.
        # We might need a more generic way to detect motion.
        # For now, we'll fetch person detection history as a proxy for motion.
        return await self._repository.get_analytics_history(
            network_id, object_type="person"
        )
