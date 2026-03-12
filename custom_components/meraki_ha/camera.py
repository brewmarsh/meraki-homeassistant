"""Support for Meraki cameras."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.meraki_ha.const.config import (
    CONF_RTSP_STREAM_ENABLED,
)
from custom_components.meraki_ha.const.integration import DOMAIN

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
    coordinator: MerakiCameraCoordinator = entry_data["camera_coordinator"]
    camera_service: CameraService = entry_data["camera_service"]

    devices: list[MerakiDevice] = list(coordinator.devices_by_serial.values())
    camera_entities: list[MerakiRTSPStreamCamera] = []

    for device in devices:
        try:
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
        except Exception as err:
            _LOGGER.error(
                "Failed to initialize camera for Meraki device %s: %s",
                getattr(device, "serial", "Unknown"),
                err,
                exc_info=True,
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
        return resolve_device_info(self.device_data, self.coordinator.config_entry)

    async def async_added_to_hass(self) -> None:
        """Handle when entity is added to hass."""
        await super().async_added_to_hass()

        if (
            self.coordinator.config_entry.options.get(CONF_RTSP_STREAM_ENABLED, False)
            and not self.device_data.rtsp_url
        ):
            # Move the blocking API call to a background task to prevent Setup timeout
            self.coordinator.config_entry.async_create_background_task(
                self.hass,
                self._async_enable_rtsp(),
                f"meraki_ha_enable_rtsp_{self._device_serial}",
            )

    async def _async_enable_rtsp(self) -> None:
        """Enable RTSP stream in the background."""
        try:
            _LOGGER.debug(
                "RTSP stream is missing, enabling for camera %s in background",
                self._device_serial,
            )
            # 1. Enable RTSP
            await self._camera_service.async_set_rtsp_stream_enabled(
                self._device_serial, True
            )

            # 2. Fetch the URL immediately
            url = await self._camera_service.get_video_stream_url(self._device_serial)
            if url:
                _LOGGER.debug(
                    "Successfully enabled and retrieved RTSP URL for %s: %s",
                    self._device_serial,
                    url,
                )
                # Update the device data model directly so the UI can use it
                self.device_data.rtsp_url = url
                self.async_write_ha_state()
            else:
                _LOGGER.debug(
                    "RTSP enabled for %s, but URL not yet available. "
                    "It will be picked up on the next coordinator refresh.",
                    self._device_serial,
                )

        except Exception as e:
            _LOGGER.warning(
                "Could not enable RTSP stream for %s in background: %s",
                self._device_serial,
                e,
            )

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        if not self._device_serial:
            _LOGGER.debug("Cannot fetch snapshot: Camera serial is missing.")
            return None

        if self.device_data.status != "online":
            _LOGGER.debug("Skipping snapshot for offline camera: %s", self.name)
            return None

        try:
            url = await self._camera_service.generate_snapshot(self._device_serial)
            if not url:
                _LOGGER.debug("Failed to get snapshot URL for %s", self.name)
                return None

            session = async_get_clientsession(self.hass)
            async with session.get(url) as response:
                # Meraki API sometimes returns 500 HTML on transient failures
                if response.status >= 500:
                    _LOGGER.warning(
                        "Meraki API returned %d for snapshot: %s",
                        response.status,
                        self.name,
                    )
                    return None
                response.raise_for_status()
                return await response.read()
        except Exception as err:
            _LOGGER.warning("Failed to fetch camera snapshot for %s: %s", self.name, err)
            return None

    @property
    def is_streaming(self) -> bool:
        """Return True if the camera is streaming."""
        if not self._device_serial or self.device_data.rtsp_url is None:
            return False
        return True

    async def async_stream_source(self) -> str | None:
        """Return the source of the stream."""
        if not self._device_serial:
            _LOGGER.debug("Cannot fetch stream: Camera serial is missing.")
            return None
        return await self._camera_service.get_video_stream_url(self._device_serial)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs = {}
        if rtsp_url := self.device_data.rtsp_url:
            attrs["rtsp_url"] = rtsp_url
        return attrs

    async def async_turn_on(self) -> None:
        """Turn on the camera stream."""
        if not self._device_serial:
            _LOGGER.warning("Cannot turn on stream: Camera serial is missing.")
            return
        _LOGGER.debug("Turning on stream for camera %s", self._device_serial)
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_serial, True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn off the camera stream."""
        if not self._device_serial:
            _LOGGER.warning("Cannot turn off stream: Camera serial is missing.")
            return
        _LOGGER.debug("Turning off stream for camera %s", self._device_serial)
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_serial, False
        )
        await self.coordinator.async_request_refresh()
