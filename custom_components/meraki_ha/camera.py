"""
Support for Meraki cameras.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

import aiohttp
from homeassistant.components.camera import Camera
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .helpers.entity_helpers import format_entity_name
from .core.utils.naming_utils import format_device_name
from .core.utils.network_utils import construct_rtsp_url
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
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from .coordinator import MerakiDataUpdateCoordinator
    from .services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki camera entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    camera_service = entry_data["camera_service"]

    camera_entities = [
        MerakiCamera(coordinator, config_entry, device, camera_service)
        for device in coordinator.data["devices"]
        if device.get("productType", "").startswith("camera")
    ]

    if camera_entities:
        async_add_entities(camera_entities)


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

        video_settings = self._device_data.get("video_settings", {})
        if not video_settings.get("rtspUrl") and not self._device_data.get("lanIp"):
            self._attr_entity_registry_enabled_default = False
            self._disabled_reason = "The camera did not provide a stream URL or a LAN IP address from the API."

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.is_pending(self.unique_id):
            return  # Ignore update during cooldown

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
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        snapshot_url = await self._camera_service.generate_snapshot(self._device_serial)

        if not snapshot_url:
            _LOGGER.error("Could not generate snapshot for camera %s", self.name)
            return None

        try:
            session = async_get_clientsession(self.hass)
            async with session.get(snapshot_url) as response:
                if response.status != 200:
                    _LOGGER.error(
                        "Error fetching snapshot for %s: %s", self.name, response.status
                    )
                    return None
                return await response.read()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching snapshot for %s: %s", self.name, err)
            return None

    async def stream_source(self) -> Optional[str]:
        """Return the source of the stream, prioritizing LAN IP."""
        if not self.is_streaming:
            return None

        lan_ip = self._device_data.get("lanIp")
        video_settings = self._device_data.get("video_settings", {})
        api_url = video_settings.get("rtspUrl")

        # Prioritize local LAN stream if an IP is available.
        if lan_ip:
            return construct_rtsp_url(lan_ip)

        # Fall back to the cloud-provided URL if it's a valid RTSP link.
        if api_url and api_url.startswith("rtsp://"):
            return api_url

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
        elif not video_settings.get("rtspUrl") and not self._device_data.get("lanIp"):
            attrs["stream_status"] = (
                "Stream URL not available. This may be because the camera does not support cloud archival or local streaming."
            )
            self.coordinator.add_status_message(
                self._device_serial,
                "RTSP stream URL is not available. The camera might not support cloud archival or local streaming.",
            )
        else:
            attrs["stream_status"] = "Enabled"
        return attrs

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Return supported features."""
        if self._attr_model and self._attr_model.startswith("MV2"):
            return CameraEntityFeature(0)
        return SUPPORT_STREAM

    @property
    def is_streaming(self) -> bool:
        """
        Return true if the camera is streaming.

        This requires the rtspServerEnabled setting to be true and for either a
        valid rtsp:// URL or a LAN IP to be available.
        """
        video_settings = self._device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled", False):
            return False

        # A stream is available if we have a LAN IP or a valid cloud-provided URL.
        has_lan_ip = self._device_data.get("lanIp") is not None
        cloud_url = video_settings.get("rtspUrl")
        has_valid_cloud_url = (
            cloud_url is not None
            and isinstance(cloud_url, str)
            and cloud_url.startswith("rtsp://")
        )

        return has_lan_ip or has_valid_cloud_url

    async def async_turn_on(self) -> None:
        """Turn on the camera stream."""
        _LOGGER.debug("Turning on stream for camera %s", self._device_serial)

        # Optimistically update the state
        if "video_settings" not in self._device_data:
            self._device_data["video_settings"] = {}
        self._device_data["video_settings"]["rtspServerEnabled"] = True
        self.async_write_ha_state()

        # Make the API call and register a cooldown
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_serial, True
        )
        self.coordinator.register_pending_update(self.unique_id)

    async def async_turn_off(self) -> None:
        """Turn off the camera stream."""
        _LOGGER.debug("Turning off stream for camera %s", self._device_serial)

        # Optimistically update the state
        if "video_settings" not in self._device_data:
            self._device_data["video_settings"] = {}
        self._device_data["video_settings"]["rtspServerEnabled"] = False
        self.async_write_ha_state()

        # Make the API call and register a cooldown
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_serial, False
        )
        self.coordinator.register_pending_update(self.unique_id)