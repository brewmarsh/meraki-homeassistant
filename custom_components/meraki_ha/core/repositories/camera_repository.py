"""
Repository for camera-related data.

This module defines the CameraRepository class, which is responsible for
fetching and processing camera-related data from the Meraki API.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from aiohttp import ClientError
from meraki.exceptions import AsyncAPIError

from ...helpers.logging_helper import MerakiLoggers
from ..errors import MerakiError, MerakiInformationalError

if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient


_LOGGER = MerakiLoggers.CAMERA


class CameraRepository:
    """Repository for camera-related data."""

    def __init__(self, api_client: MerakiAPIClient, organization_id: str) -> None:
        """Initialize the camera repository."""
        self._api_client = api_client
        self._organization_id = organization_id

    async def get_camera_features(self, serial: str) -> list[str]:
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
        if (
            model.startswith("MV12")
            or model.startswith("MV22")
            or model.startswith("MV72")
        ):
            features.extend(["person_detection", "vehicle_detection"])

        return features

    async def get_analytics_data(
        self, serial: str, object_type: str
    ) -> list[dict[str, Any]] | None:
        """Fetch object detection and motion data."""
        try:
            recent = await self._api_client.camera.get_device_camera_analytics_recent(
                serial, object_type
            )
            return recent
        except (AsyncAPIError, MerakiError, ClientError) as e:
            _LOGGER.error("Error fetching analytics data for %s: %s", serial, e)
            return None

    async def async_get_cloud_video_url(self, serial: str) -> str | None:
        """
        Get the cloud video URL for a camera.

        This returns a Meraki Dashboard video link URL (HTTPS) that can be
        used to view the camera stream in a browser or compatible player.
        """
        try:
            video_link_data = (
                await self._api_client.camera.get_device_camera_video_link(serial)
            )
            url = video_link_data.get("url")

            # Return any valid HTTPS URL (cloud video links)
            if url and isinstance(url, str) and url.startswith("https://"):
                return cast(str, url)

            # Also accept HTTP URLs (less common but possible)
            if url and isinstance(url, str) and url.startswith("http://"):
                return cast(str, url)

            return None
        except MerakiInformationalError as e:
            _LOGGER.debug(
                "Could not retrieve cloud video URL for camera %s: %s",
                serial,
                e,
            )
            return None
        except (AsyncAPIError, MerakiError, ClientError) as e:
            _LOGGER.debug("Error fetching cloud video link for %s: %s", serial, e)
            return None

    async def async_get_rtsp_stream_url(self, serial: str) -> str | None:
        """
        Get the RTSP video stream URL for a camera.

        This method validates that the URL is a valid RTSP stream URL.
        """
        # MV2 cameras do not support historical viewing without cloud archive,
        # so we should not attempt to fetch a video link for them.
        try:
            device = await self._api_client.devices.get_device(serial)
            if device and device.get("model", "").startswith("MV2"):
                _LOGGER.debug(
                    "Skipping video link fetch for unsupported MV2 model: %s", serial
                )
                return None
        except (AsyncAPIError, MerakiError, ClientError) as e:
            _LOGGER.warning(
                "Could not check camera model for %s due to an error "
                "fetching device details: %s",
                serial,
                e,
            )
            # Do not proceed if the device check fails.
            return None

        try:
            video_link_data = (
                await self._api_client.camera.get_device_camera_video_link(serial)
            )
            url = video_link_data.get("url")

            # Validate that we received a valid RTSP URL
            if url and isinstance(url, str) and url.startswith("rtsp://"):
                return cast(str, url)

            # If we get a non-RTSP URL, log it and return None
            if url:
                _LOGGER.debug(
                    "API returned non-RTSP URL, no RTSP stream available: %s",
                    url,
                )
            return None
        except MerakiInformationalError as e:
            # This can happen if the camera model doesn't support RTSP (e.g., MV2).
            # Log it as a debug, not an error that will spam the user.
            _LOGGER.debug(
                "Could not retrieve RTSP URL for camera %s "
                "(this may be normal if the model does not support it): %s",
                serial,
                e,
            )
            return None
        except (AsyncAPIError, MerakiError, ClientError) as e:
            _LOGGER.debug("Error fetching video link for %s: %s", serial, e)
            return None

    async def get_analytics_history(
        self, network_id: str, object_type: str
    ) -> list[dict[str, Any]]:
        """Get analytics history for a network."""
        try:
            return await self._api_client.network.get_network_camera_analytics_history(
                network_id, object_type
            )
        except (AsyncAPIError, MerakiError, ClientError) as e:
            _LOGGER.error("Error fetching analytics history: %s", e)
            return []

    async def generate_snapshot(self, serial: str) -> str | None:
        """Generate a snapshot and return the URL."""
        try:
            snapshot_data = (
                await self._api_client.camera.generate_device_camera_snapshot(serial)
            )
            return snapshot_data.get("url")
        except (AsyncAPIError, MerakiError, ClientError) as e:
            _LOGGER.error("Error generating snapshot for %s: %s", serial, e)
            return None

    async def set_rtsp_stream_enabled(self, serial: str, enabled: bool) -> None:
        """Enable or disable RTSP stream for a camera."""
        try:
            await self._api_client.camera.update_camera_video_settings(
                serial, externalRtspEnabled=enabled
            )
        except (AsyncAPIError, MerakiError, ClientError) as e:
            _LOGGER.error("Error setting RTSP stream for %s: %s", serial, e)
