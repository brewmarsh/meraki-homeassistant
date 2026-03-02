"""Support for Meraki cameras."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import aiohttp
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .const_conf import CONF_ENABLE_CAMERA_ENTITIES
from .entity import MerakiEntity
from .helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.device_registry import DeviceInfo
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from ..coordinators import MerakiCameraCoordinator
    from .core.models.device import MerakiDevice
    from .services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki camera entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: MerakiCameraCoordinator = entry_data["coordinator"]
    camera_service: CameraService = entry_data["camera_service"]

    devices: list[MerakiDevice] = coordinator.data.get("devices", [])
    camera_entities: list[MerakiRTSPStreamCamera] = []

    for device in devices:
        if device.product_type == "camera":
            _LOGGER.debug("Found camera device: %s", device.serial)
            camera_entities.append(
                MerakiRTSPStreamCamera(
                    coordinator,
                    device,
                    camera_service,
                    config_entry,
                )
            )

    if camera_entities:
        _LOGGER.debug("Adding %d camera entities", len(camera_entities))
        async_add_entities(camera_entities)


class MerakiRTSPStreamCamera(MerakiEntity, Camera):
    """
    Representation of a Meraki RTSP stream camera.

    This entity is state-driven by the central MerakiCameraCoordinator.
    """

    _attr_brand = "Cisco Meraki"
    _attr_has_entity_name = True
    _attr_supported_features = CameraEntityFeature.STREAM

    coordinator: MerakiCameraCoordinator

    def __init__(
        self,
        coordinator: MerakiCameraCoordinator,
        device: MerakiDevice,
        camera_service: CameraService,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._device_serial = device.serial or ""
        self._camera_service = camera_service
        self._config_entry = config_entry

        # Setting name to None with has_entity_name=True makes this the "Main" entity
        self._attr_name = None
        self._attr_model = self.device_data.model

        _LOGGER.debug(
            "Naming Debug - Entity: %s | Class: %s | has_entity_name: %s "
            "| _attr_name: %s | Device Identifiers: %s",
            self.entity_id if hasattr(self, "entity_id") else "New Entity",
            self.__class__.__name__,
            getattr(self, "_attr_has_entity_name", "Not Set"),
            getattr(self, "_attr_name", "None"),
            self.device_info.get("identifiers")
            if self.device_info
            else "NO DEVICE INFO",
        )

    @property
    def device_data(self) -> MerakiDevice:
        """Return the device data from the coordinator."""
        return self.coordinator.get_device(self._device_serial) or MerakiDevice()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self.device_data, self._config_entry)

    async def async_added_to_hass(self) -> None:
        """Handle when entity is added to hass."""
        await super().async_added_to_hass()

        if (
            self._config_entry.options.get(CONF_ENABLE_CAMERA_ENTITIES, True)
            and not self.device_data.rtsp_url
        ):
            try:
                _LOGGER.debug(
                    "RTSP stream is missing, enabling for camera %s",
                    self._device_serial,
                )
                await self._camera_service.async_set_rtsp_stream_enabled(
                    self._device_serial, True
                )
            except Exception as e:
                _LOGGER.warning(
                    "Could not enable RTSP stream for %s: %s", self._device_serial, e
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
            _LOGGER.debug("Failed to get snapshot URL for %s", self.name)
            return None

        try:
            session = async_get_clientsession(self.hass)
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()
        except aiohttp.ClientError as e:
            _LOGGER.error("Error fetching snapshot for %s: %s", self.name, e)
            return None

    @property
    def is_streaming(self) -> bool:
        """Return True if the camera is streaming."""
        if self.device_data.rtsp_url is None:
            return False
        return True

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        if self.device_data.rtsp_url is None:
            return None
        return self.device_data.rtsp_url

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs = {}
        if rtsp_url := self.device_data.rtsp_url:
            attrs["rtsp_url"] = rtsp_url
        return attrs

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
