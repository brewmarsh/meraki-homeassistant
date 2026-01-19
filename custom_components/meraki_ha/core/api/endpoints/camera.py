"""Meraki API endpoints for cameras."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class CameraEndpoints:
    """Camera-related endpoints."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """
        Initialize the endpoint.

        Args:
        ----
            api_client: The Meraki API client.

        """
        self._api_client = api_client
<<<<<<< HEAD
        self._dashboard = api_client.dashboard
=======
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

    @handle_meraki_errors
    @async_timed_cache()
    async def get_camera_sense_settings(self, serial: str) -> dict[str, Any]:
        """Get sense settings for a specific camera."""
<<<<<<< HEAD
        settings = await self._api_client.run_sync(
            self._dashboard.camera.getDeviceCameraSense, serial=serial
=======
        if self._api_client.dashboard is None:
            return {}
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.camera.getDeviceCameraSense, serial=serial
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_camera_sense_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_camera_video_settings(self, serial: str) -> dict[str, Any]:
        """Get video settings for a specific camera."""
<<<<<<< HEAD
        settings = await self._api_client.run_sync(
            self._dashboard.camera.getDeviceCameraVideoSettings, serial=serial
=======
        if self._api_client.dashboard is None:
            return {}
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.camera.getDeviceCameraVideoSettings,
            serial=serial,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_camera_video_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=30)
    async def get_device_camera_video_link(self, serial: str) -> dict[str, Any]:
        """Get video link for a specific camera."""
<<<<<<< HEAD
        link = await self._api_client.run_sync(
            self._dashboard.camera.getDeviceCameraVideoLink, serial=serial
=======
        if self._api_client.dashboard is None:
            return {}
        link = await self._api_client.run_sync(
            self._api_client.dashboard.camera.getDeviceCameraVideoLink, serial=serial
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        )
        validated = validate_response(link)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_device_camera_video_link did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_camera_video_settings(
        self, serial: str, **kwargs
    ) -> dict[str, Any]:
        """Update video settings for a specific camera."""
<<<<<<< HEAD
        result = await self._api_client.run_sync(
            self._dashboard.camera.updateDeviceCameraVideoSettings,
=======
        if self._api_client.dashboard is None:
            return {}
        result = await self._api_client.run_sync(
            self._api_client.dashboard.camera.updateDeviceCameraVideoSettings,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
            serial=serial,
            **kwargs,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_camera_video_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_camera_sense_settings(
        self, serial: str, **kwargs
    ) -> dict[str, Any]:
        """Update sense settings for a specific camera."""
<<<<<<< HEAD
        result = await self._api_client.run_sync(
            self._dashboard.camera.updateDeviceCameraSense,
=======
        if self._api_client.dashboard is None:
            return {}
        result = await self._api_client.run_sync(
            self._api_client.dashboard.camera.updateDeviceCameraSense,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
            serial=serial,
            **kwargs,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_camera_sense_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=30)
    async def get_device_camera_analytics_recent(
        self, serial: str, object_type: str = "person"
    ) -> list[dict[str, Any]]:
        """Get recent analytics for a specific camera."""
<<<<<<< HEAD
        recent = await self._api_client.run_sync(
            self._dashboard.camera.getDeviceCameraAnalyticsRecent,
=======
        if self._api_client.dashboard is None:
            return []
        recent = await self._api_client.run_sync(
            self._api_client.dashboard.camera.getDeviceCameraAnalyticsRecent,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
            serial=serial,
            objectType=object_type,
        )
        validated = validate_response(recent)
        if not isinstance(validated, list):
            _LOGGER.warning("get_device_camera_analytics_recent did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=30)
    async def get_device_camera_analytics_zones(
        self, serial: str
    ) -> list[dict[str, Any]]:
        """Get analytics zones for a specific camera."""
<<<<<<< HEAD
        zones = await self._api_client.run_sync(
            self._dashboard.camera.getDeviceCameraAnalyticsZones,
=======
        if self._api_client.dashboard is None:
            return []
        zones = await self._api_client.run_sync(
            self._api_client.dashboard.camera.getDeviceCameraAnalyticsZones,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
            serial=serial,
        )
        validated = validate_response(zones)
        if not isinstance(validated, list):
            _LOGGER.warning("get_device_camera_analytics_zones did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    async def generate_device_camera_snapshot(
        self, serial: str, **kwargs
    ) -> dict[str, Any]:
        """Generate a snapshot of what the camera sees."""
<<<<<<< HEAD
        snapshot = await self._api_client.run_sync(
            self._dashboard.camera.generateDeviceCameraSnapshot,
=======
        if self._api_client.dashboard is None:
            return {}
        snapshot = await self._api_client.run_sync(
            self._api_client.dashboard.camera.generateDeviceCameraSnapshot,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
            serial=serial,
            **kwargs,
        )
        validated = validate_response(snapshot)
        if not isinstance(validated, dict):
            _LOGGER.warning("generate_device_camera_snapshot did not return a dict.")
            return {}
        return validated
