"""Sensors for Meraki VLANs."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry

<<<<<<< HEAD
from ...core.entities.meraki_vlan_entity import MerakiVLANEntity
from ...core.utils.entity_id_utils import get_vlan_entity_id
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_vlan_entity import MerakiVLANEntity
from ...core.utils.entity_id_utils import get_vlan_entity_id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from ...types import MerakiVlan

_LOGGER = logging.getLogger(__name__)


class MerakiVLANIDSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN ID sensor."""

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
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a VLAN entity")
<<<<<<< HEAD
        vlan_id = self._vlan.get("id")
=======
        vlan_id = self._vlan.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not vlan_id:
            raise ValueError("VLAN ID should not be None here")
        self._attr_unique_id = get_vlan_entity_id(self._network_id, vlan_id, "vlan_id")
        self._attr_name = "VLAN ID"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
<<<<<<< HEAD
        return self._vlan.get("id")
=======
        return self._vlan.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


class MerakiVLANIPv4EnabledSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN IPv4 Enabled sensor."""

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
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a VLAN entity")
<<<<<<< HEAD
        vlan_id = self._vlan.get("id")
=======
        vlan_id = self._vlan.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not vlan_id:
            raise ValueError("VLAN ID should not be None here")
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, vlan_id, "ipv4_enabled"
        )
        self._attr_name = "IPv4 Enabled"

    @property
    def native_value(self) -> bool:
        """Return the state of the sensor."""
<<<<<<< HEAD
        return self._vlan.get("applianceIp") is not None
=======
        return self._vlan.appliance_ip is not None
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


class MerakiVLANIPv4InterfaceSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN IPv4 Interface IP sensor."""

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
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a VLAN entity")
<<<<<<< HEAD
        vlan_id = self._vlan.get("id")
=======
        vlan_id = self._vlan.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not vlan_id:
            raise ValueError("VLAN ID should not be None here")
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, vlan_id, "ipv4_interface_ip"
        )
        self._attr_name = "IPv4 Interface IP"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
<<<<<<< HEAD
        return self._vlan.get("applianceIp")
=======
        return self._vlan.appliance_ip
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


class MerakiVLANIPv4UplinkSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN IPv4 Uplink sensor."""

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
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a VLAN entity")
<<<<<<< HEAD
        vlan_id = self._vlan.get("id")
=======
        vlan_id = self._vlan.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not vlan_id:
            raise ValueError("VLAN ID should not be None here")
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, vlan_id, "ipv4_uplink"
        )
        self._attr_name = "IPv4 Uplink"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        # This information does not appear to be directly available in the VLAN data
        return "Any"


class MerakiVLANIPv6EnabledSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN IPv6 Enabled sensor."""

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
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a VLAN entity")
<<<<<<< HEAD
        vlan_id = self._vlan.get("id")
=======
        vlan_id = self._vlan.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not vlan_id:
            raise ValueError("VLAN ID should not be None here")
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, vlan_id, "ipv6_enabled"
        )
        self._attr_name = "IPv6 Enabled"

    @property
    def native_value(self) -> bool:
        """Return the state of the sensor."""
<<<<<<< HEAD
        ipv6_data = self._vlan.get("ipv6")
=======
        ipv6_data = self._vlan.ipv6
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if ipv6_data is None:
            return False
        return ipv6_data.get("enabled", False)


class MerakiVLANIPv6InterfaceSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN IPv6 Interface IP sensor."""

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
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a VLAN entity")
<<<<<<< HEAD
        vlan_id = self._vlan.get("id")
=======
        vlan_id = self._vlan.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not vlan_id:
            raise ValueError("VLAN ID should not be None here")
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, vlan_id, "ipv6_interface_ip"
        )
        self._attr_name = "IPv6 Interface IP"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
<<<<<<< HEAD
        ipv6_data = self._vlan.get("ipv6")
=======
        ipv6_data = self._vlan.ipv6
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if ipv6_data is None:
            return None
        return ipv6_data.get("prefix")


class MerakiVLANIPv6UplinkSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN IPv6 Uplink sensor."""

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
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a VLAN entity")
<<<<<<< HEAD
        vlan_id = self._vlan.get("id")
=======
        vlan_id = self._vlan.id
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not vlan_id:
            raise ValueError("VLAN ID should not be None here")
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, vlan_id, "ipv6_uplink"
        )
        self._attr_name = "IPv6 Uplink"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
<<<<<<< HEAD
        ipv6_data = self._vlan.get("ipv6")
=======
        ipv6_data = self._vlan.ipv6
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if ipv6_data is None or not ipv6_data.get("enabled"):
            return None
        assignments = ipv6_data.get("prefixAssignments")
        if not assignments:
            return None
        interfaces = assignments[0].get("origin", {}).get("interfaces", [])
        return ", ".join(interfaces) if interfaces else None
