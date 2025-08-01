"""Support for Meraki cameras."""

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
        "device_coordinator"
    )

    if meraki_device_coordinator and meraki_device_coordinator.data:
        entities = [
            MerakiCamera(meraki_device_coordinator, device)
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
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}-camera"
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            self._device["name"],
            self._device.get("productType", "camera"),
            name_format,
            apply_prefix=False,
        )
        self._attr_supported_features = CameraEntityFeature.STREAM
        self._rtsp_url: Optional[str] = None
        self._webrtc_provider = None
        self.access_tokens = []
        self._supports_native_async_webrtc = False
        self._cache = {}

        if self._device.get("video_settings", {}).get("externalRtspEnabled"):
            self._rtsp_url = self._device.get("video_settings", {}).get("rtspUrl")
        _LOGGER.debug("Camera %s initialized with RTSP URL: %s", self.name, self._rtsp_url)

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
    def stream_options(self) -> dict:
        """Return stream options."""
        return {}

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        _LOGGER.debug("Camera %s added to hass", self.name)
        await super().async_added_to_hass()

    async def _enable_rtsp(self) -> None:
        """Enable the RTSP stream for the camera."""
        _LOGGER.debug("Camera %s: enabling RTSP", self.name)
        client = self.coordinator.hass.data[DOMAIN][
            self.coordinator.config_entry.entry_id
        ][DATA_CLIENT]
        try:
            response = await client.camera.update_device_camera_video_settings(
                serial=self._device["serial"],
                externalRtspEnabled=True,
            )
            _LOGGER.debug("Camera %s: enable RTSP API response: %s", self.name, response)
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to enable RTSP for camera %s: %s", self._device["serial"], e
            )

    @property
    def is_streaming(self) -> bool:
        """Return true if the camera is streaming."""
        return self._rtsp_url is not None

    async def stream_source(self) -> Optional[str]:
        """Return the source of the stream."""
        _LOGGER.debug("Camera %s: stream_source requested, returning: %s", self.name, self._rtsp_url)
        return self._rtsp_url

    async def async_camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return a still image from the camera."""
        return None

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
        _LOGGER.debug("Camera %s: handling coordinator update", self.name)
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                video_settings = device.get("video_settings", {})
                _LOGGER.debug(
                    "Camera %s: found device data with video settings: %s",
                    self.name,
                    video_settings,
                )

                auto_enable_rtsp = self.coordinator.config_entry.options.get(
                    CONF_AUTO_ENABLE_RTSP
                )
                _LOGGER.debug(
                    "Camera %s: auto_enable_rtsp is %s, externalRtspEnabled is %s",
                    self.name,
                    auto_enable_rtsp,
                    video_settings.get("externalRtspEnabled"),
                )
                if auto_enable_rtsp and not video_settings.get("externalRtspEnabled"):
                    _LOGGER.debug("Camera %s: creating task to enable RTSP", self.name)
                    self.hass.async_create_task(self._enable_rtsp())

                if video_settings.get("externalRtspEnabled"):
                    rtsp_url = video_settings.get("rtspUrl")
                    if rtsp_url and rtsp_url.startswith("rtsp://:"):
                        lan_ip = self._device.get("lanIp")
                        if lan_ip:
                            rtsp_url = f"rtsp://{lan_ip}{rtsp_url[6:]}"
                    self._rtsp_url = rtsp_url
                    _LOGGER.debug(
                        "Camera %s: RTSP is enabled, URL: %s", self.name, self._rtsp_url
                    )
                else:
                    self._rtsp_url = None
                    _LOGGER.debug("Camera %s: RTSP is disabled", self.name)
                self.async_write_ha_state()
                return
        _LOGGER.debug(
            "Camera %s: device data not found in coordinator update", self.name
        )
