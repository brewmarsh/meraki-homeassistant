"""Base entity for Meraki VLANs."""

from __future__ import annotations

<<<<<<< HEAD
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
import dataclasses

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from ...types import MerakiVlan
from . import BaseMerakiEntity


class MerakiVLANEntity(BaseMerakiEntity):
    """Representation of a Meraki VLAN."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        config_entry: ConfigEntry,
        network_id: str,
        vlan: MerakiVlan,
    ) -> None:
        """Initialize the VLAN entity."""
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            network_id=network_id,
        )
        self._vlan = vlan
        if self._network_id is None:
            raise ValueError("Network ID cannot be None for a VLAN entity")
<<<<<<< HEAD
        vlan_device_data = {**vlan, "productType": "vlan"}
=======

        # vlan is a dataclass, so we need to convert it to a dict for format_device_name
        vlan_device_data = dataclasses.asdict(vlan)
        vlan_device_data["productType"] = "vlan"

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        formatted_name = format_device_name(
            device=vlan_device_data,
            config=self._config_entry.options,
        )

<<<<<<< HEAD
        self._attr_device_info = DeviceInfo(
            identifiers={
                (self._config_entry.domain, f"vlan_{network_id}_{vlan['id']}")
            },
=======
        vlan_id = vlan.id
        if not vlan_id:
            raise ValueError("VLAN ID not found in VLAN data")
        self._attr_device_info = DeviceInfo(
            identifiers={(self._config_entry.domain, f"vlan_{network_id}_{vlan_id}")},
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="VLAN",
            via_device=(self._config_entry.domain, f"network_{network_id}"),
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
