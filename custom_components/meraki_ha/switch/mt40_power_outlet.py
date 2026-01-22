"""Switch entity for Meraki MT40 power outlet."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.api.client import MerakiAPIClient
from ..helpers.device_info_helpers import resolve_device_info
from ..types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiMt40PowerOutlet(
    CoordinatorEntity,
    SwitchEntity,
):
    """Representation of a Meraki MT40 power outlet."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: MerakiDevice,
        config_entry: ConfigEntry,
        meraki_client: MerakiAPIClient,
    ) -> None:
        """
        Initialize the switch.

        Args:
        ----
            coordinator: The data update coordinator.
            device_info: The device information.
            config_entry: The config entry.
            meraki_client: The Meraki API client.

        """
        super().__init__(coordinator)
        self._device_info = device_info
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._attr_unique_id = f"{self._device_info.serial}-outlet"
        self._attr_name = f"{self._device_info.name} Outlet"
        self._attr_is_on: bool | None = None

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device_info, self._config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device: MerakiDevice | None = self.coordinator.get_device(
            serial=self._device_info.serial
        )
        if device:
            self._device_info = device
            if not self.coordinator.is_pending(self.unique_id):
                self._attr_is_on = self._get_power_state()
            self.async_write_ha_state()
        else:
            super()._handle_coordinator_update()

    def _get_power_state(self) -> bool | None:
        """Get the power state from the device's readings."""
        if not isinstance(self._device_info.readings, list):
            return None
        return next(
            (
                reading.get("value")
                for reading in self._device_info.readings
                if reading.get("metric") == "downstream_power"
            ),
            None,
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """
        Turn the power outlet on.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        self._attr_is_on = True
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)

        if not self._device_info.serial:
            _LOGGER.warning("Device serial not available for %s", self.name)
            return

        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=self._device_info.serial,
                operation="enableDownstreamPower",
            )
        except Exception as e:
            _LOGGER.error("Error turning on MT40 outlet %s: %s", self.unique_id, e)
            self.coordinator.cancel_pending_update(self.unique_id)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """
        Turn the power outlet off.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        self._attr_is_on = False
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)

        if not self._device_info.serial:
            _LOGGER.warning("Device serial not available for %s", self.name)
            return

        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=self._device_info.serial,
                operation="disableDownstreamPower",
            )
        except Exception as e:
            _LOGGER.error("Error turning off MT40 outlet %s: %s", self.unique_id, e)
            self.coordinator.cancel_pending_update(self.unique_id)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return super().available and self._get_power_state() is not None
