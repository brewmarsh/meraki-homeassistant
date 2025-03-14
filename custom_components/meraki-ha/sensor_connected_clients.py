"""Sensor platform for the meraki_ha integration."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .meraki_api.devices import get_meraki_device_clients
from .meraki_api.exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiConnectedClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Connected Clients sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Connected Clients sensor."""
        super().__init__(coordinator)
        self._device = device
        _LOGGER.debug(f"Meraki: Device data: {device}")
        self._attr_name = f"{device['name']} Connected Clients"
        self._attr_unique_id = f"{device['serial']}_connected_clients"
        self._attr_icon = "mdi:account-network"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }
        self._attr_extra_state_attributes["serial_number"] = device.get("serial")
        _LOGGER.debug(
            f"Meraki: Connected Clients Sensor Initialized: {self._attr_name}"
        )

    async def async_update(self) -> None:
        """Update the sensor state."""
        _LOGGER.debug(f"Meraki: Updating sensor state for {self._attr_name}")
        try:
            clients = await get_meraki_device_clients(
                self.coordinator.api_key,
                self.coordinator.org_id,
                self._device["serial"],
            )
            self._attr_native_value = len(clients)
        except MerakiApiError as e:
            _LOGGER.error(f"Meraki: Error fetching connected clients: {e}")
            self._attr_native_value = None
        except Exception as e:
            _LOGGER.error(f"Meraki: Unexpected error fetching connected clients: {e}")
            self._attr_native_value = None

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        _LOGGER.debug(f"Meraki: Getting extra state attributes for {self._attr_name}")
        return self._attr_extra_state_attributes.copy()
