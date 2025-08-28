"""
Repository for camera-related data.

This module defines the CameraRepository class, which is responsible for
fetching and processing camera-related data from the Meraki API.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..errors import MerakiInformationalError


if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class CameraRepository:
    """Repository for camera-related data."""

    def __init__(self, api_client: MerakiAPIClient, organization_id: str) -> None:
        """Initialize the camera repository."""
        self._api_client = api_client
        self._organization_id = organization_id

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
        devices = await self._api_client.organization.get_organization_devices()
        device = next((d for d in devices if d.get("serial") == serial), None)
        if not device:
            return []

        model = device.get("model", "")

        features = ["video_stream"]
        if model.startswith("MV12") or model.startswith("MV22") or model.startswith("MV72"):
            features.extend(["person_detection", "vehicle_detection"])

        return features

    async def get_analytics_data(
        self, serial: str, object_type: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch object detection and motion data."""
        try:
            recent = (
                await self._api_client.camera.get_device_camera_analytics_recent(
                    serial, object_type
                )
            )
            return recent
        except Exception as e:
            _LOGGER.error("Error fetching analytics data for %s: %s", serial, e)
            return None

    async def async_get_rtsp_stream_url(self, serial: str) -> Optional[str]:
        """
        Get the RTSP video stream URL for a camera.

        This method validates that the URL is a valid RTSP stream URL.
        """
        try:
            video_link_data = (
                await self._api_client.camera.get_device_camera_video_link(serial)
            )
            url = video_link_data.get("url")

            # Validate that we received a valid RTSP URL
            if url and url.startswith("rtsp://"):
                return url

            # If we get a non-RTSP URL, log it and return None
            if url:
                _LOGGER.debug(
                    "API returned a non-RTSP URL, assuming no stream available: %s",
                    url,
                )
            return None
        except MerakiInformationalError:
            raise  # Re-raise to be handled by the service/entity
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

    async def generate_snapshot(self, serial: str) -> Optional[str]:
        """Generate a snapshot and return the URL."""
        try:
            snapshot_data = (
                await self._api_client.camera.generate_device_camera_snapshot(
                    serial
                )
            )
            return snapshot_data.get("url")
        except Exception as e:
            _LOGGER.error("Error generating snapshot for %s: %s", serial, e)
            return None

    async def set_rtsp_stream_enabled(self, serial: str, enabled: bool) -> None:
        """Enable or disable RTSP stream for a camera."""
        try:
            await self._api_client.camera.update_device_camera_video_settings(
                serial, rtsp_server_enabled=enabled
            )
        except Exception as e:
            _LOGGER.error("Error setting RTSP stream for %s: %s", serial, e)
