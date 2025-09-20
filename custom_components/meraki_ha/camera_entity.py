"""
A Meraki camera entity.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

import aiohttp
from homeassistant.components.camera import Camera
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .helpers.entity_helpers import format_entity_name
from .core.utils.naming_utils import format_device_name
from .core.utils.network_utils import is_private_ip, construct_rtsp_url
from .const import DOMAIN, CONF_MERAKI_API_KEY

# SUPPORT_STREAM was deprecated in 2024.2, and CameraEntityFeature was added.
# This try/except block is for backward compatibility.
try:
    from homeassistant.components.camera import CameraEntityFeature
    SUPPORT_STREAM = CameraEntityFeature.STREAM
except (ImportError, AttributeError):
    from homeassistant.components.camera import (
        SUPPORT_STREAM,
    )  # pyright: ignore[reportGeneralTypeIssues]


if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from .coordinator import MerakiDataUpdateCoordinator
    from .services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiCamera(CoordinatorEntity["MerakiDataUpdateCoordinator"], Camera):
    """
    Representation of a Meraki camera.

    This entity is state-driven by the central MerakiDataUpdateCoordinator.
    """

    _attr_brand = "Cisco Meraki"

    def __init__(
        self,
        coordinator: "MerakiDataUpdateCoordinator",
        config_entry: "ConfigEntry",
        device: Dict[str, Any],
        camera_service: "CameraService",
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._config_entry = config_entry
        self._device_serial = device["serial"]
        self._camera_service = camera_service
        self._device_data = device  # Store initial data
        self._attr_unique_id = f"{self._device_serial}-camera"
        self._attr_name = format_entity_name(
            format_device_name(
                self._device_data, self._config_entry.options
            ),
            "",
        )
        self._attr_model = self._device_data.get("model")
        self._attr_entity_registry_enabled_default = True
        self._disabled_reason = None

        if not self._device_data.get("rtspUrl") and not self._device_data.get("lanIp"):
            self._attr_entity_registry_enabled_default = False
            self._disabled_reason = "The camera did not provide a stream URL or a LAN IP address from the API."

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find the updated device data from the coordinator's payload
        for device in self.coordinator.data.get("devices", []):
            if device.get("serial") == self._device_serial:
                self._device_data = device
                break
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(
                self._device_data, self._config_entry.options
            ),
            model=self._device_data.get("model"),
            manufacturer="Cisco Meraki",
        )

    async def async_camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return a still image from the camera."""
        url = await self._camera_service.generate_snapshot(self._device_serial)
        if not url:
            msg = f"Failed to get snapshot URL for {self.name}"
            _LOGGER.error(msg)
            self.coordinator.add_status_message(self._device_serial, msg)
            return None

        try:
            api_key = self._config_entry.data[CONF_MERAKI_API_KEY]
            headers = {"X-Cisco-Meraki-API-Key": api_key}
            session = async_get_clientsession(self.hass)
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.read()
        except aiohttp.ClientError as e:
            msg = f"Error fetching snapshot for {self.name}: {e}"
            _LOGGER.error(msg)
            self.coordinator.add_status_message(self._device_serial, msg)
            return None

    async def stream_source(self) -> Optional[str]:
        """Return the source of the stream, if enabled."""
        if not self.is_streaming:
            return None

        api_url = self._device_data.get("rtspUrl")
        lan_ip = self._device_data.get("lanIp")

        final_url = None

        if api_url:
            final_url = api_url
        elif lan_ip:
            final_url = construct_rtsp_url(lan_ip)

        # Final validation before returning
        if final_url and final_url.startswith("rtsp://"):
            return final_url

        _LOGGER.warning("Could not determine a valid RTSP URL for camera %s", self.name)
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attrs = {}
        if self._disabled_reason:
            attrs["disabled_reason"] = self._disabled_reason
            return attrs

        video_settings = self._device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled", False):
            attrs["stream_status"] = "Disabled in Meraki Dashboard"
            self.coordinator.add_status_message(
                self._device_serial, "RTSP stream is disabled in the Meraki dashboard."
            )
        elif not self._device_data.get("rtspUrl"):
            attrs["stream_status"] = (
                "Stream URL not available. This may be because the camera does not support cloud archival."
            )
            self.coordinator.add_status_message(
                self._device_serial,
                "RTSP stream URL is not available. The camera might not support cloud archival.",
            )
        else:
            attrs["stream_status"] = "Enabled"
        return attrs

    @property
    def supported_features(self) -> int:
        """Return supported features."""
        return SUPPORT_STREAM

    @property
    def is_streaming(self) -> bool:
        """
        Return true if the camera is streaming.

        This requires both the rtspServerEnabled setting to be true and a
        valid rtsp:// URL to be available.
        """
        video_settings = self._device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled", False):
            return False

        url = self._device_data.get("rtspUrl")
        return url is not None and isinstance(url, str) and url.startswith("rtsp://")

    async def async_turn_on(self) -> None:
        """Turn on the camera stream."""
        _LOGGER.debug("Turning on stream for camera %s", self._device_serial)
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_serial, True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn off the camera stream."""
        _LOGGER.debug("Turning off stream for camera %s", self._device_serial)
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_serial, False
        )
        await self.coordinator.async_request_refresh()
