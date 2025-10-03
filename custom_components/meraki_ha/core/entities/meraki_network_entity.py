"""Base entity for Meraki Networks."""

from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.config_entries import ConfigEntry
from ...coordinator import MerakiDataUpdateCoordinator
from ...types import MerakiNetwork
from ...core.utils.naming_utils import format_device_name


class MerakiNetworkEntity(CoordinatorEntity[MerakiDataUpdateCoordinator]):
    """Representation of a Meraki Network."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
    ) -> None:
        """Initialize the network entity."""
        super().__init__(coordinator=coordinator)
        self._config_entry = config_entry
        self._network = network
        self._network_id = network["id"]

        self._attr_device_info = DeviceInfo(
            identifiers={(self._config_entry.domain, network["id"])},
            name=format_device_name(network, config_entry.options),
            manufacturer="Cisco Meraki",
            model="Network",
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self._attr_device_info
