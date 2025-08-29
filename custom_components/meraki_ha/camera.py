"""
Support for Meraki cameras.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

import aiohttp
from homeassistant.components.camera import Camera
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, CONF_MERAKI_API_KEY
from .core.errors import MerakiInformationalError
from .helpers.entity_helpers import format_entity_name
from .core.utils.naming_utils import format_device_name

try:
    from homeassistant.components.camera import CameraEntityFeature
    SUPPORT_STREAM = CameraEntityFeature.STREAM
except (ImportError, AttributeError):
    from homeassistant.components.camera import SUPPORT_STREAM


if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from .core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from .services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki camera entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    discovered_entities = entry_data.get("entities", [])

    camera_entities = [e for e in discovered_entities if isinstance(e, MerakiCamera)]

    if camera_entities:
        async_add_entities(camera_entities)


class MerakiCamera(CoordinatorEntity["MerakiDataCoordinator"], Camera):
    """
    Representation of a Meraki camera.

    This entity is state-driven by the central MerakiDataCoordinator.
    """

    _attr_brand = "Cisco Meraki"

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
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
        self._attr_unique_id = f"{self._device_serial}-camera"
        self._attr_name = format_entity_name(
            format_device_name(self.device_data, self.coordinator.config_entry.options),
            "",
        )
        self._attr_model = self.device_data.get("model")

    @property
    def device_data(self) -> Dict[str, Any]:
        """Return the device data from the coordinator."""
        return self.coordinator.get_device(self._device_serial) or {}

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(
                self.device_data, self.coordinator.config_entry.options
            ),
            model=self.device_data.get("model"),
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
        if self.is_streaming:
            return self.device_data.get("rtsp_url")
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attrs = {}
        video_settings = self.device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled", False):
            attrs["stream_status"] = "Disabled in Meraki Dashboard"
            self.coordinator.add_status_message(
                self._device_serial, "RTSP stream is disabled in the Meraki dashboard."
            )
        elif not self.device_data.get("rtsp_url"):
            attrs["stream_status"] = "Stream URL not available. This may be because the camera does not support cloud archival."
            self.coordinator.add_status_message(
                self._device_serial, "RTSP stream URL is not available. The camera might not support cloud archival."
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
        video_settings = self.device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled", False):
            return False

        url = self.device_data.get("rtsp_url")
        return (
            url is not None and isinstance(url, str) and url.startswith("rtsp://")
        )

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
