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

    from .coordinator import MerakiDataUpdateCoordinator
    from .services.camera_service import CameraService
    from .types import MerakiDevice


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
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        device: MerakiDevice,
        camera_service: CameraService,
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._config_entry = config_entry
        # device is passed as MerakiDevice
        self._device_serial = device.serial if device.serial else ""
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device_serial}-camera"
        self._attr_has_entity_name = True
        self._attr_name = None
        self._attr_model = self.device_data.model

    @property
    def device_data(self) -> MerakiDevice:
        """Return the device data from the coordinator."""
        from .types import MerakiDevice

        return self.coordinator.get_device(self._device_serial) or MerakiDevice()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(
                self.device_data, self.coordinator.config_entry.options
            ),
            model=self.device_data.model,
            manufacturer="Cisco Meraki",
        )

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        if self.device_data.status != "online":
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

    @property
    def _rtsp_url(self) -> str | None:
        """Return the RTSP URL, either from API or constructed."""
        if url := self.device_data.rtsp_url:
            return url

        # Fallback for MV cameras with LAN IP
        # The rtspServerEnabled flag is unreliable, so we fallback to
        # constructing the URL if the device is online and has a LAN IP.
        model = self.device_data.model or ""
        lan_ip = self.device_data.lan_ip
        if model.startswith("MV") and lan_ip:
            return f"rtsp://{lan_ip}:9000/live"

        return None

    async def stream_source(self) -> str | None:
        """Return the source of the stream, if enabled."""
        if self.is_streaming:
            return self._rtsp_url
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs = {}
        rtsp_url = self._rtsp_url
        video_settings = self.device_data.video_settings or {}
        rtsp_server_enabled = video_settings.get("rtspServerEnabled", False)

        if rtsp_url:
            attrs["stream_status"] = "Enabled"
            attrs["rtsp_url"] = rtsp_url
        elif not rtsp_server_enabled:
            attrs["stream_status"] = "Disabled in Meraki Dashboard"
            self.coordinator.add_status_message(
                self._device_serial, "RTSP stream is disabled in the Meraki dashboard."
            )
        else:
            attrs["stream_status"] = (
                "Stream URL not available. This may be because the camera does not"
                " support cloud archival."
            )
            self.coordinator.add_status_message(
                self._device_serial,
                "RTSP stream URL is not available. The camera might not support cloud"
                " archival.",
            )
        return attrs

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Return supported features."""
        return CameraEntityFeature.STREAM

    @property
    def is_streaming(self) -> bool:
        """
        Return true if the camera is streaming.

        We rely on the presence of a valid RTSP URL (either from API or constructed)
        as the primary indicator, as the rtspServerEnabled flag can be unreliable.
        """
        return self._rtsp_url is not None

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
