"""Switch entity for Meraki MT40 power outlet."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..core.api.client import MerakiAPIClient
from ..helpers.device_info_helpers import resolve_device_info
from ..helpers.logging_helper import MerakiLoggers
from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.SWITCH


class MerakiMt40PowerOutlet(
    CoordinatorEntity,  # type: ignore[type-arg]
    SwitchEntity,
    RestoreEntity,
):
    """Representation of a Meraki MT40 power outlet.

    Uses RestoreEntity to preserve state across Home Assistant restarts.
    """

    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_info: dict[str, Any],
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
        self._attr_unique_id = f"{self._device_info['serial']}-outlet"
        self._attr_name = f"{self._device_info['name']} Outlet"
        self._attr_is_on: bool | None = None

    async def async_added_to_hass(self) -> None:
        """Restore state when entity is added to HA."""
        await super().async_added_to_hass()

        # Restore previous state on restart if no fresh power state
        if self._attr_is_on is None:
            if (last_state := await self.async_get_last_state()) is not None:
                self._attr_is_on = last_state.state == "on"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device_info, self._config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device = next(
            (
                d
                for d in self.coordinator.data.get("devices", [])
                if d.get("serial") == self._device_info["serial"]
            ),
            None,
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
        # Use readings_raw (list format) for sensor entities
        readings = self._device_info.get("readings_raw") or self._device_info.get(
            "readings"
        )
        if not isinstance(readings, list):
            return None
        return next(
            (
                reading.get("value")
                for reading in readings
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

        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=self._device_info["serial"],
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

        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=self._device_info["serial"],
                operation="disableDownstreamPower",
            )
        except Exception as e:
            _LOGGER.error("Error turning off MT40 outlet %s: %s", self.unique_id, e)
            self.coordinator.cancel_pending_update(self.unique_id)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity state attributes with update timestamp."""
        attrs: dict[str, Any] = {}
        if self.coordinator.last_successful_update:
            attrs["last_meraki_update"] = (
                self.coordinator.last_successful_update.isoformat()
            )
        return attrs

    @property
    def available(self) -> bool:
        """Return if the entity is available.

        The entity is available if the device exists in coordinator data.
        We don't require downstream_power readings for availability since
        the outlet can still be controlled even if readings are delayed.
        """
        if not super().available:
            return False
        # Check if device exists in coordinator data
        device = next(
            (
                d
                for d in self.coordinator.data.get("devices", [])
                if d.get("serial") == self._device_info["serial"]
            ),
            None,
        )
        return device is not None
