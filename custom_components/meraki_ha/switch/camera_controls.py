"""Switch entities for controlling Meraki camera settings."""

import logging
from typing import Any, Dict, TYPE_CHECKING

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator
from ..helpers.entity_helpers import format_entity_name
from ..core.utils.naming_utils import format_device_name
from .camera_settings import MerakiCameraSettingSwitchBase

if TYPE_CHECKING:
    from ..services.camera_service import CameraService
    from ..core.api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class RTSPStreamSwitch(CoordinatorEntity[MerakiDataUpdateCoordinator], SwitchEntity):
    """
    Switch to control the RTSP server on a Meraki camera.

    This switch implements the "Optimistic UI with Cooldown" pattern to provide a
    responsive user experience while handling the provisioning delay in the
    Meraki Cloud API.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        camera_service: "CameraService",
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the RTSP switch."""
        super().__init__(coordinator)
        self._camera_service = camera_service
        self._device_data = device_data
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_data['serial']}-rtsp-enabled"
        self._attr_name = format_entity_name(
            format_device_name(self._device_data, self._config_entry.options),
            "RTSP Enabled",
        )
        self._attr_icon = "mdi:cctv"

        # Set availability based on model
        model = self._device_data.get("model", "")
        if model.startswith("MV2"):
            self._attr_available = False

        # Set initial state
        self._update_internal_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch from coordinator data."""
        if self.coordinator.is_pending(self.unique_id):
            return  # Ignore update during cooldown

        # Find the updated device data from the coordinator's payload
        for device in self.coordinator.data.get("devices", []):
            if device.get("serial") == self._device_data["serial"]:
                self._device_data = device
                break

        video_settings = self._device_data.get("video_settings", {})
        self._attr_is_on = video_settings.get("rtspServerEnabled", False)

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the RTSP stream on."""
        self._attr_is_on = True
        self.async_write_ha_state()
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_data["serial"], True
        )
        self.coordinator.register_pending_update(self.unique_id)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the RTSP stream off."""
        self._attr_is_on = False
        self.async_write_ha_state()
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_data["serial"], False
        )
        self.coordinator.register_pending_update(self.unique_id)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_data["serial"])},
            name=format_device_name(self._device_data, self._config_entry.options),
            model=self._device_data.get("model"),
            manufacturer="Cisco Meraki",
        )


class AnalyticsSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control analytics on a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: "MerakiAPIClient",
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the analytics switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled",
            "sense.analyticsEnabled",
            config_entry,
        )
        self._attr_name = format_entity_name(
            format_device_name(device_data, config_entry.options),
            "Analytics",
        )
        self._attr_icon = "mdi:chart-bar"