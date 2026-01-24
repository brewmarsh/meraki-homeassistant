"""Binary sensor for Meraki network status."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator
from ..types import MerakiNetwork


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki network status binary sensor entities."""
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]

    if coordinator.data.get("networks"):
        async_add_entities(
            [MerakiNetworkStatus(network) for network in coordinator.data["networks"]]
        )


class MerakiNetworkStatus(BinarySensorEntity):
    """Representation of a Meraki network status sensor."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True

    def __init__(
        self,
        network: MerakiNetwork,
    ) -> None:
        """Initialize the sensor."""
        self._network = network

        # Ensure network ID is available
        network_id = network.id if network.id else "unknown_network"
        self._attr_unique_id = f"{network_id}-status"
        self._attr_name = "Status"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        # Ensure network ID is available
        network_id = self._network.id if self._network.id else "unknown_network"
        return DeviceInfo(
            identifiers={(DOMAIN, network_id)},
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return True
