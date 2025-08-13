"""Sensors for Meraki VLANs."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry

from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...core.entities.meraki_vlan_entity import MerakiVLANEntity
from ...core.utils.entity_id_utils import get_vlan_entity_id


_LOGGER = logging.getLogger(__name__)


class MerakiVLANSubnetSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN Subnet sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, self._vlan["id"], "subnet"
        )
        self._attr_name = f"{self._vlan['name']} Subnet"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._vlan.get("subnet")


class MerakiVLANApplianceIpSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN Appliance IP sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, self._vlan["id"], "appliance_ip"
        )
        self._attr_name = f"{self._vlan['name']} Appliance IP"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._vlan.get("applianceIp")
