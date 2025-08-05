"""Support for Meraki cameras."""

import asyncio
import logging
from typing import Any, Dict, Optional

from homeassistant.components.camera import (
    Camera,
    CameraEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_AUTO_ENABLE_RTSP,
    DATA_CLIENT,
    CONF_DEVICE_NAME_FORMAT,
    DEFAULT_DEVICE_NAME_FORMAT,
)
from .core.coordinators.device import MerakiDeviceCoordinator
from .helpers.entity_helpers import format_entity_name


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki camera entities from a config entry."""
    meraki_device_coordinator = hass.data[DOMAIN][config_entry.entry_id].get(
        "coordinator"
    )

    if meraki_device_coordinator and meraki_device_coordinator.data:
        entities = [
            MerakiCamera(
                meraki_device_coordinator,
                device,
                config_entry.options.get(CONF_AUTO_ENABLE_RTSP, False),
            )
            for device in meraki_device_coordinator.data.get("devices", [])
            if device.get("productType") == "camera"
        ]
        async_add_entities(entities, True)


class MerakiCamera(CoordinatorEntity[MerakiDeviceCoordinator], Camera):
    """Representation of a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
        auto_enable_rtsp: bool = False,
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        self._device = device
        self._auto_enable_rtsp = auto_enable_rtsp
        self._attr_unique_id = f"{self._device['serial']}-camera"
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            self._device["name"],
            self._device.get("productType", "camera"),
            name_format,
            apply_format=False,
        )
        # Support streaming via RTSP
        features = set()
        if self._device.get("video_settings", {}).get("externalRtspEnabled"):
            features.add(CameraEntityFeature.STREAM)
        self._attr_supported_features = features
        self._rtsp_url: Optional[str] = None
        self._webrtc_provider = None
        self._legacy_webrtc_provider = None
        self.access_tokens = []
        self._supports_native_async_webrtc = False
        self._supports_native_sync_webrtc = False
        self._cache = {}
        self._create_stream_lock = asyncio.Lock()
        self.stream = None

        if self._device.get("video_settings", {}).get("externalRtspEnabled"):
            self._rtsp_url = self._device.get("video_settings", {}).get("rtspUrl")

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    @property
    def stream_source(self) -> str | None:
        """Return the source of the stream."""
        return self._rtsp_url

    async def async_camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return a still image from the camera."""
        return None

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()

    async def _enable_rtsp(self) -> None:
        """Enable the RTSP stream for the camera."""
        client = self.coordinator.hass.data[DOMAIN][
            self.coordinator.config_entry.entry_id
        ][DATA_CLIENT]
        try:
            await self.hass.async_add_executor_job(
                lambda: client._dashboard.camera.updateDeviceCameraVideoSettings(
                    serial=self._device["serial"],
                    externalRtspEnabled=True,
                )
            )
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to enable RTSP for camera %s: %s", self._device["serial"], e
            )

    @property
    def is_streaming(self) -> bool:
        """Return true if the camera is streaming."""
        return self._rtsp_url is not None

    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture to use in the frontend, if any."""
        if not self.access_tokens:
            return None
        return super().entity_picture

    @property
    def state_attributes(self) -> dict[str, Any] | None:
        """Return the state attributes."""
        attrs = {}
        if self.is_streaming and self.access_tokens:
            attrs["access_token"] = self.access_tokens[-1]
        return attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                video_settings = device.get("video_settings", {})

                if self._auto_enable_rtsp and not video_settings.get(
                    "externalRtspEnabled"
                ):
                    self.coordinator.hass.async_create_task(self._enable_rtsp())

                # Update RTSP URL and supported features
                features = set()
                if video_settings.get("externalRtspEnabled"):
                    features.add(CameraEntityFeature.STREAM)
                    rtsp_url = video_settings.get("rtspUrl")
                    lan_ip = self._device.get("lanIp")
                    if lan_ip and rtsp_url:
                        rtsp_url = f"rtsp://{lan_ip}:{rtsp_url.split(':')[-1]}"
                    self._rtsp_url = rtsp_url
                else:
                    self._rtsp_url = None
                self._attr_supported_features = features
                self.async_write_ha_state()
                return

    async def async_stream(self) -> dict:
        """Return streaming information."""
        if not self._rtsp_url:
            if self._auto_enable_rtsp:
                await self._enable_rtsp()
                # Give the camera a moment to enable RTSP
                await asyncio.sleep(2)
                # Refresh to get the new RTSP URL
                await self.coordinator.async_request_refresh()
            else:
                return {}

        if not self._rtsp_url:
            return {}

        return {
            "stream_source": self._rtsp_url,
            "use_stream_source": True,
        }
