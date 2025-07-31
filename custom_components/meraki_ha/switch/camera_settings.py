"""Switch entities for controlling Meraki Camera settings."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..core.api.client import MerakiAPIClient
from ..core.coordinators.device import MerakiDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSettingSwitchBase(
    CoordinatorEntity[MerakiDeviceCoordinator], SwitchEntity
):
    """Base class for Meraki Camera Setting Switches."""

    _attr_has_entity_name = True
    entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
        switch_type: str,
        attribute_to_check: str,
    ) -> None:
        """Initialize the base camera setting switch."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._device_serial: str = device_data["serial"]
        self._attribute_to_check = attribute_to_check
        self._attribute_path = attribute_to_check.split(".")
        self._attr_unique_id = f"{self._device_serial}_{switch_type}_switch"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=device_data.get("name"),
        )
        self._update_internal_state()

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this switch's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        _LOGGER.debug(
            "Device data for serial '%s' not found in coordinator for switch '%s'.",
            self._device_serial,
            self.unique_id,
        )
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the `_attr_is_on` state of the switch based on coordinator data."""
        current_device_data = self._get_current_device_data()
        if current_device_data:
            raw_value = current_device_data
            for key in self._attribute_path:
                if isinstance(raw_value, dict):
                    raw_value = raw_value.get(key)
                else:
                    raw_value = None
                    break
            self._attr_is_on = bool(raw_value)
        else:
            self._attr_is_on = False

    async def _update_camera_setting(self, value: bool) -> None:
        """Update the specific camera setting via the Meraki API."""
        kwargs_for_api = {}
        if self._attribute_path == ["senseEnabled"]:
            kwargs_for_api["sense_enabled"] = value
        elif self._attribute_path == ["audioDetection", "enabled"]:
            kwargs_for_api["audio_detection_enabled"] = value
        elif self._attribute_path == ["externalRtspEnabled"]:
            await self._meraki_client.update_camera_video_settings(
                serial=self._device_serial, rtsp_server_enabled=value
            )
            await self.coordinator.async_request_refresh()
            self._attr_is_on = value
            self.async_write_ha_state()
            return
        else:
            _LOGGER.error("Unsupported attribute path: %s", self._attribute_path)
            return

        try:
            await self._meraki_client.update_camera_sense_settings(
                serial=self._device_serial, **kwargs_for_api
            )
            await self.coordinator.async_request_refresh()
            self._attr_is_on = value
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error(
                "Failed to update camera setting %s for %s: %s",
                self._attribute_to_check,
                self._device_serial,
                e,
            )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._update_camera_setting(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._update_camera_setting(False)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available:
            return False
        current_device_data = self._get_current_device_data()
        if not current_device_data:
            return False
        value = current_device_data
        for key in self._attribute_path:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return False
        return value is not None
