"""Support for Meraki cameras."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

import aiohttp
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .core.utils.naming_utils import format_device_name

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .meraki_data_coordinator import MerakiDataCoordinator
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
        _LOGGER.debug("Adding %d camera entities", len(camera_entities))
        chunk_size = 50
        for i in range(0, len(camera_entities), chunk_size):
            chunk = camera_entities[i : i + chunk_size]
            async_add_entities(chunk)
            if len(camera_entities) > chunk_size:
                await asyncio.sleep(1)


class MerakiCamera(CoordinatorEntity, Camera):
    """
    Representation of a Meraki camera.

    This entity is state-driven by the central MerakiDataCoordinator.
    """

    _attr_brand = "Cisco Meraki"

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        device: dict[str, Any] | Any,
        camera_service: CameraService,
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._config_entry = config_entry
        # Handle both dict and dataclass for device
        self._device_serial = (
            device.get("serial") if isinstance(device, dict) else device.serial
        )
        name = device.get("name") if isinstance(device, dict) else device.name
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device_serial}-camera"
        self._attr_name = f"[Camera] {name}"
        self._attr_model = self.device_data.get("model")

    @property
    def device_data(self) -> dict[str, Any]:
        """Return the device data from the coordinator."""
        import dataclasses

        data = self.coordinator.get_device(self._device_serial)
        if dataclasses.is_dataclass(data):
            return dataclasses.asdict(data)
        return data or {}

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
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        if self.device_data.get("status") != "online":
            _LOGGER.debug("Skipping snapshot for offline camera: %s", self.name)
            return None

        url = await self._camera_service.generate_snapshot(self._device_serial)
        if not url:
            msg = f"Failed to get snapshot URL for {self.name}"
            _LOGGER.error(msg)
            self.coordinator.add_status_message(self._device_serial, msg)
            return None

        try:
            session = async_get_clientsession(self.hass)
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()
        except aiohttp.ClientError as e:
            msg = f"Error fetching snapshot for {self.name}: {e}"
            _LOGGER.error(msg)
            self.coordinator.add_status_message(self._device_serial, msg)
            return None

    async def stream_source(self) -> str | None:
        """Return the source of the stream, if enabled."""
        if self.is_streaming:
            return self.device_data.get("rtsp_url")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs = {}
        video_settings = self.device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled", False):
            attrs["stream_status"] = "Disabled in Meraki Dashboard"
            self.coordinator.add_status_message(
                self._device_serial, "RTSP stream is disabled in the Meraki dashboard."
            )
        elif not self.device_data.get("rtsp_url"):
            attrs["stream_status"] = (
                "Stream URL not available. This may be because the camera does not"
                " support cloud archival."
            )
            self.coordinator.add_status_message(
                self._device_serial,
                "RTSP stream URL is not available. The camera might not support cloud"
                " archival.",
            )
        else:
            attrs["stream_status"] = "Enabled"
        return attrs

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Return supported features."""
        return CameraEntityFeature.STREAM

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
        return url is not None and isinstance(url, str) and url.startswith("rtsp://")

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        # Disable the entity if there is no RTSP URL available
        return bool(self.device_data.get("rtsp_url"))

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
