"""Base entity for Meraki Networks."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
=======
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
from ...types import MerakiNetwork
from ..utils.naming_utils import format_device_name


class MerakiNetworkEntity(CoordinatorEntity):
    """Representation of a Meraki Network."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
    ) -> None:
        from dataclasses import asdict

=======
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
    ) -> None:
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        """Initialize the network entity."""
        super().__init__(coordinator=coordinator)
        self._config_entry = config_entry
        self._network = network
<<<<<<< HEAD
        self._network_id = network.id

        device_data_for_naming = {**asdict(network), "productType": "network"}
=======
        self._network_id = network["id"]

        device_data_for_naming = {**network, "productType": "network"}
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        formatted_name = format_device_name(
            device=device_data_for_naming,
            config=config_entry.options,
        )
        self._attr_device_info = DeviceInfo(
<<<<<<< HEAD
            identifiers={(self._config_entry.domain, f"network_{network.id}")},
=======
            identifiers={(self._config_entry.domain, f"network_{network['id']}")},
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Network",
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
