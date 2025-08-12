"""Meraki API endpoints for cameras."""

import logging
from typing import Any, Dict

from ...utils.api_utils import handle_meraki_errors, validate_response
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
        return validate_response(settings)

    @handle_meraki_errors
    @async_timed_cache()
    async def get_camera_video_settings(self, serial: str) -> Dict[str, Any]:
        """Get video settings for a specific camera."""
        settings = await self._api_client._run_sync(
            self._dashboard.camera.getDeviceCameraVideoSettings, serial=serial
        )
        return validate_response(settings)

    @handle_meraki_errors
    @async_timed_cache(timeout=30)
    async def get_device_camera_video_link(self, serial: str) -> Dict[str, Any]:
        """Get video link for a specific camera."""
        link = await self._api_client._run_sync(
            self._dashboard.camera.getDeviceCameraVideoLink, serial=serial
        )
        return validate_response(link)

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
        return validate_response(result)
