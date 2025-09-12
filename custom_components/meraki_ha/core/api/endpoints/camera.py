"""Meraki API endpoints for cameras."""

import logging
from typing import Any, Dict, List

from ..utils.api_utils import handle_meraki_errors, validate_response
from ..cache import async_timed_cache

_LOGGER = logging.getLogger(__name__)


class CameraEndpoints:
    """Camera-related endpoints."""

    def __init__(self, api_client):
        """Initialize the endpoint."""
        self._api_client = api_client
        self._dashboard = api_client._dashboard

    @handle_meraki_errors
    @async_timed_cache()
    async def get_camera_sense_settings(self, serial: str) -> Dict[str, Any]:
        """Get sense settings for a specific camera."""
        settings = await self._api_client._run_sync(
            self._dashboard.camera.getDeviceCameraSense, serial=serial
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_camera_sense_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_camera_video_settings(self, serial: str) -> Dict[str, Any]:
        """Get video settings for a specific camera."""
        settings = await self._api_client._run_sync(
            self._dashboard.camera.getDeviceCameraVideoSettings, serial=serial
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_camera_video_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=30)
    async def get_device_camera_video_link(self, serial: str) -> Dict[str, Any]:
        """Get video link for a specific camera."""
        link = await self._api_client._run_sync(
            self._dashboard.camera.getDeviceCameraVideoLink, serial=serial
        )
        validated = validate_response(link)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_device_camera_video_link did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_camera_video_settings(
        self, serial: str, **kwargs
    ) -> Dict[str, Any]:
        """Update video settings for a specific camera."""
        result = await self._api_client._run_sync(
            self._dashboard.camera.updateDeviceCameraVideoSettings,
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
    ) -> Dict[str, Any]:
        """Update sense settings for a specific camera."""
        result = await self._api_client._run_sync(
            self._dashboard.camera.updateDeviceCameraSense,
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
    ) -> List[Dict[str, Any]]:
        """Get recent analytics for a specific camera."""
        recent = await self._api_client._run_sync(
            self._dashboard.camera.getDeviceCameraAnalyticsRecent,
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
    ) -> List[Dict[str, Any]]:
        """Get analytics zones for a specific camera."""
        zones = await self._api_client._run_sync(
            self._dashboard.camera.getDeviceCameraAnalyticsZones,
            serial=serial,
        )
        validated = validate_response(zones)
        if not isinstance(validated, list):
            _LOGGER.warning("get_device_camera_analytics_zones did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    async def generate_device_camera_snapshot(self, serial: str) -> Dict[str, Any]:
        """Generate a snapshot of what the camera sees."""
        snapshot = await self._api_client._run_sync(
            self._dashboard.camera.generateDeviceCameraSnapshot,
            serial=serial,
            fullframe=False,
        )
        validated = validate_response(snapshot)
        if not isinstance(validated, dict):
            _LOGGER.warning("generate_device_camera_snapshot did not return a dict.")
            return {}
        return validated
