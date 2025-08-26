"""
Repository for camera-related data.

This module defines the CameraRepository class, which is responsible for
fetching and processing camera-related data from the Meraki API.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional


if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class CameraRepository:
    """Repository for camera-related data."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """Initialize the camera repository."""
        self._api_client = api_client

    async def get_camera_features(self, serial: str) -> List[str]:
        """
        Retrieve a camera's model-specific capabilities.

        This method should determine the features of a camera based on its model
        and other properties. For now, we'll assume all cameras support basic
        features, but this can be expanded later.
        """
        # In the future, this could involve a call to get device details
        # and then a lookup based on the model.
        # For now, we'll hardcode some features for demonstration.
        device = await self._api_client.organization.get_organization_device(serial)
        model = device.get("model", "")

        features = ["video_stream"]
        if model.startswith("MV12") or model.startswith("MV22") or model.startswith("MV72"):
            features.extend(["person_detection", "vehicle_detection"])

        return features

    async def get_analytics_data(self, serial: str) -> Optional[Dict[str, Any]]:
        """Fetch object detection and motion data."""
        try:
            overview = (
                await self._api_client.camera.get_device_camera_analytics_overview(
                    serial
                )
            )
            return overview
        except Exception as e:
            _LOGGER.error("Error fetching analytics data for %s: %s", serial, e)
            return None

    async def get_video_url(self, serial: str) -> Optional[str]:
        """Get the video stream URL for a camera."""
        try:
            video_link_data = (
                await self._api_client.camera.get_device_camera_video_link(serial)
            )
            return video_link_data.get("url")
        except Exception as e:
            _LOGGER.error("Error fetching video link for %s: %s", serial, e)
            return None

    async def get_analytics_history(
        self, network_id: str, object_type: str
    ) -> List[Dict[str, Any]]:
        """Get analytics history for a network."""
        try:
            return await self._api_client.network.get_network_camera_analytics_history(
                network_id, object_type
            )
        except Exception as e:
            _LOGGER.error("Error fetching analytics history: %s", e)
            return []
