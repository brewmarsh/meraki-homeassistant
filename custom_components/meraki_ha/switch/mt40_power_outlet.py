"""Switch entity for Meraki MT40 power outlet."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..coordinators import MerakiSensorCoordinator
from ..core.api import MerakiApiClientProtocol
from ..core.models.device import MerakiDevice
from ..entity import MerakiEntity
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiMt40PowerOutlet(
    MerakiEntity,
    SwitchEntity,
):
    """Representation of a Meraki MT40 power outlet."""

    _attr_has_entity_name = True
    coordinator: MerakiSensorCoordinator

    def __init__(
        self,
        coordinator: MerakiSensorCoordinator,
        device_info: MerakiDevice,
        config_entry: ConfigEntry,
        meraki_client: MerakiApiClientProtocol,
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
        self._device_serial = device_info.serial
        self._network_id = device_info.network_id
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        # Explicitly set the unique ID here to override the base class logic
        # which might generate a different ID based on class name.
        self._unique_id_override = (
            f"{self._device_info.serial}_{self._device_info.network_id}_outlet"
        )
        self._attr_name = "Outlet"
        self._attr_is_on: bool | None = None

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device_info, self._config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self._device_info.serial:
            device: MerakiDevice | None = self.coordinator.get_device(
                serial=self._device_info.serial
            )
            if device:
                self._device_info = device
                if self.unique_id and not self.coordinator.is_pending(self.unique_id):
                    self._attr_is_on = self._get_power_state()

        super()._handle_coordinator_update()

    def _get_power_state(self) -> bool | None:
        """Get the power state from the device information."""
        return self._device_info.outlet_status

    async def async_turn_on(self, **kwargs: Any) -> None:
        """
        Turn the power outlet on.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        self._attr_is_on = True
        self.async_write_ha_state()
        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            if self._device_info.serial is None:
                raise ValueError("Device serial is missing")
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=self._device_info.serial,
                operation="enableDownstreamPower",
            )
        except Exception as e:
            _LOGGER.error("Error turning on MT40 outlet %s: %s", self.unique_id, e)
            if self.unique_id:
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
        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            if self._device_info.serial is None:
                raise ValueError("Device serial is missing")
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=self._device_info.serial,
                operation="disableDownstreamPower",
            )
        except Exception as e:
            _LOGGER.error("Error turning off MT40 outlet %s: %s", self.unique_id, e)
            if self.unique_id:
                self.coordinator.cancel_pending_update(self.unique_id)

    @property
    def unique_id(self) -> str | None:
        """Return the unique ID."""
        return self._unique_id_override

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return super().available and self._device_info.outlet_status is not None
