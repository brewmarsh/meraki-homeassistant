"""Sensors for Meraki VLANs."""

from __future__ import annotations

import logging

from ...types import MerakiVlan

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry

from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_vlan_entity import MerakiVLANEntity
from ...core.utils.entity_id_utils import get_vlan_entity_id


_LOGGER = logging.getLogger(__name__)


class MerakiVLANSubnetSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN Subnet sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: MerakiVlan,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        assert self._network_id, "Network ID cannot be None for a VLAN entity"
        vlan_id = self._vlan.get("id")
        assert vlan_id, "VLAN ID should not be None here"
        self._attr_unique_id = get_vlan_entity_id(self._network_id, vlan_id, "subnet")
        self._attr_name = f"{self._vlan['name']} Subnet"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._vlan.get("subnet")


class MerakiVLANApplianceIpSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN Appliance IP sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: MerakiVlan,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        assert self._network_id, "Network ID cannot be None for a VLAN entity"
        vlan_id = self._vlan.get("id")
        assert vlan_id, "VLAN ID should not be None here"
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, vlan_id, "appliance_ip"
        )
        self._attr_name = f"{self._vlan['name']} Appliance IP"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._vlan.get("applianceIp")
