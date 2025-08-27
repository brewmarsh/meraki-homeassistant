"""
Support for Meraki cameras.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

import aiohttp
from homeassistant.components.camera import (
    Camera,
    CameraEntityFeature,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN
from .core.errors import MerakiInformationalError
from .helpers.entity_helpers import format_entity_name
from .core.utils.naming_utils import format_device_name


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
    """Representation of a Meraki camera."""

    _attr_brand = "Cisco Meraki"

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        device: Dict[str, Any],
        camera_service: "CameraService",
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._device = device
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device['serial']}-camera"
        self._attr_name = format_entity_name(
            format_device_name(self._device, self.coordinator.config_entry.options),
            "",
        )
        self._attr_model = device.get("model")
        self._rtsp_url: Optional[str] = None
        self._stream_error: Optional[str] = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    async def async_camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return a still image from the camera."""
        serial = self._device["serial"]
        url = await self._camera_service.generate_snapshot(serial)
        if not url:
            _LOGGER.error("Failed to get snapshot URL for %s", serial)
            return None

        try:
            session = async_get_clientsession(self.hass)
            async with session.get(url) as response:
                if response.status != 200:
                    _LOGGER.error(
                        "Error fetching snapshot for %s: %s",
                        serial,
                        response.status,
                    )
                    return None
                return await response.read()
        except aiohttp.ClientError as e:
            _LOGGER.error("Error fetching snapshot for %s: %s", serial, e)
            return None

    async def stream_source(self) -> Optional[str]:
        """Return the source of the stream."""
        if self._rtsp_url is None and self._stream_error is None:
            try:
                self._rtsp_url = await self._camera_service.get_video_stream_url(
                    self._device["serial"]
                )
            except MerakiInformationalError as e:
                # Check for the specific, non-critical error about historical viewing
                if "Historical viewing is not supported" in str(e):
                    _LOGGER.info(
                        "Could not retrieve stream for camera %s because it does not have cloud archive enabled. This is expected for this device.",
                        self.name,
                    )
                else:
                    _LOGGER.warning(
                        "Could not retrieve stream for camera %s: %s", self.name, e
                    )
                self._stream_error = str(e)
                self.async_write_ha_state()
        return self._rtsp_url

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attrs = {}
        if self._stream_error:
            attrs["stream_error"] = self._stream_error
        return attrs

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Return supported features."""
        return CameraEntityFeature.STREAM

    @property
    def is_streaming(self) -> bool:
        """Return true if the camera is streaming."""
        return self._rtsp_url is not None
