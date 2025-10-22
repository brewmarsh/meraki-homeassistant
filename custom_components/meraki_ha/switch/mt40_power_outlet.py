"""
Switch entity for Meraki MT40 power outlet.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinator import MerakiDataUpdateCoordinator
from ..helpers.device_info_helpers import resolve_device_info
from ..core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiMt40PowerOutlet(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SwitchEntity
):
    """Representation of a Meraki MT40 power outlet."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: Dict[str, Any],
        config_entry: ConfigEntry,
        meraki_client: MerakiAPIClient,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device_info = device_info
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._attr_unique_id = f"{self._device_info['serial']}-outlet"
        self._attr_name = f"{self._device_info['name']} Outlet"
        self._attr_is_on: bool | None = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return resolve_device_info(self._device_info, self._config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device.get("serial") == self._device_info["serial"]:
                self._device_info = device
                if not self.coordinator.is_pending(self.unique_id):
                    self._attr_is_on = self._get_power_state()
                self.async_write_ha_state()
                return
        super()._handle_coordinator_update()

    def _get_power_state(self) -> bool | None:
        """Get the power state from the device's readings."""
        readings = self._device_info.get("readings")
        if not isinstance(readings, list):
            return None
        for reading in readings:
            # Assuming the metric for the outlet state is 'downstream_power'
            if reading.get("metric") == "downstream_power":
                return reading.get("value")
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the power outlet on."""
        self._attr_is_on = True
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)

        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=self._device_info["serial"],
                operation="enableDownstreamPower",
            )
        except Exception as e:
            _LOGGER.error("Error turning on MT40 outlet %s: %s", self.unique_id, e)
            self.coordinator.cancel_pending_update(self.unique_id)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the power outlet off."""
        self._attr_is_on = False
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)

        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=self._device_info["serial"],
                operation="disableDownstreamPower",
            )
        except Exception as e:
            _LOGGER.error("Error turning off MT40 outlet %s: %s", self.unique_id, e)
            self.coordinator.cancel_pending_update(self.unique_id)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return super().available and self._get_power_state() is not None
