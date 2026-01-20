"""Base entity for Meraki Networks."""

from __future__ import annotations

from dataclasses import asdict

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...types import MerakiNetwork
from ..utils.naming_utils import format_device_name


class MerakiNetworkEntity(CoordinatorEntity):
    """Representation of a Meraki Network."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
    ) -> None:
        from dataclasses import asdict

        """Initialize the network entity."""
        super().__init__(coordinator=coordinator)
        self._config_entry = config_entry
        self._network = network
        self._network_id = network.id

        device_data_for_naming = {**asdict(network), "productType": "network"}
        formatted_name = format_device_name(
            device=device_data_for_naming,
            config=config_entry.options,
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(self._config_entry.domain, f"network_{network.id}")},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Network",
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
