"""Support for Meraki cameras."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.helpers.aiohttp_client import async_get_clientsession

# Adopting Decomposed Constants
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.const.config import CONF_ENABLE_CAMERA_ENTITIES
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
    from .discovery.service import DeviceDiscoveryService

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki camera entities via Centralized Discovery."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    discovery_service: DeviceDiscoveryService = entry_data["discovery_service"]

    # Retrieve pre-filtered camera entities from the central discovery service
    camera_entities = [
        entity
        for entity in discovery_service.all_entities
        if isinstance(entity, Camera)
    ]

    if camera_entities:
        _LOGGER.debug("Adding %d camera entities via discovery", len(camera_entities))
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
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._device_serial = device.serial or ""
        self._camera_service = camera_service

        # Standardizing naming: None + has_entity_name=True uses Device Name
        self._attr_name = None

    @property
    def device_data(self) -> MerakiDevice:
        """Return the device data from the coordinator."""
        return self.coordinator.get_device(self._device_serial) or MerakiDevice()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self.device_data, self.coordinator.config_entry)

    async def async_added_to_hass(self) -> None:
        """Handle RTSP initialization in the background to prevent setup timeouts."""
        await super().async_added_to_hass()

        # Check if camera entities are enabled and if RTSP needs provisioning
        if (
            self.coordinator.config_entry.options.get(CONF_ENABLE_CAMERA_ENTITIES, True)
            and not self.device_data.rtsp_url
        ):
            self.coordinator.config_entry.async_create_background_task(
                self.hass,
                self._async_enable_rtsp(),
                f"meraki_ha_enable_rtsp_{self._device_serial}",
            )

    async def _async_enable_rtsp(self) -> None:
        """Enable RTSP stream in the background via the CameraService."""
        try:
            _LOGGER.debug("Provisioning RTSP for camera %s", self._device_serial)
            
            # 1. Trigger the API to enable the stream
            await self._camera_service.async_set_rtsp_stream_enabled(
                self._device_serial, True
            )

            # 2. Immediately attempt to grab the URL
            url = await self._camera_service.get_video_stream_url(self._device_serial)
            if url:
                self.device_data.rtsp_url = url
                self.async_write_ha_state()
            else:
                _LOGGER.debug("RTSP provisioned for %s; waiting for URL on next refresh", self._device_serial)

        except Exception as e:
            _LOGGER.warning("Background RTSP provisioning failed for %s: %s", self._device_serial, e)

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera using the Meraki Snapshot API."""
        if not self.available or self.device_data.status != "online":
            return None

        try:
            url = await self._camera_service.generate_snapshot(self._device_serial)
            if not url:
                return None

            session = async_get_clientsession(self.hass)
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()
        except Exception as err:
            _LOGGER.warning("Failed to fetch camera snapshot: %s", err)
            return None

    async def async_stream_source(self) -> str | None:
        """Return the source of the RTSP stream."""
        return await self._camera_service.get_video_stream_url(self._device_serial)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose the RTSP URL as an attribute for advanced dashboard use."""
        attrs = {}
        if rtsp_url := self.device_data.rtsp_url:
            attrs["rtsp_url"] = rtsp_url
        return attrs

    async def async_turn_on(self) -> None:
        """Enable the camera stream via the dashboard."""
        await self._camera_service.async_set_rtsp_stream_enabled(self._device_serial, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Disable the camera stream."""
        await self._camera_service.async_set_rtsp_stream_enabled(self._device_serial, False)
        await self.coordinator.async_request_refresh()