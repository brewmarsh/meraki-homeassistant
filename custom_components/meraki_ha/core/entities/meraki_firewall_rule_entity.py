"""Base entity for Meraki Firewall Rules."""

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
from ...types import MerakiFirewallRule
from . import BaseMerakiEntity


class MerakiFirewallRuleEntity(BaseMerakiEntity):
    """Representation of a Meraki Firewall Rule."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        config_entry: ConfigEntry,
        network_id: str,
        rule: MerakiFirewallRule,
        rule_index: int,
    ) -> None:
        """
        Initialize the firewall rule entity.

        Args:
        ----
            coordinator: The data update coordinator.
            config_entry: The config entry.
            network_id: The ID of the network.
            rule: The firewall rule.
            rule_index: The index of the rule.

        """
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            network_id=network_id,
        )
        self._rule = rule
        self._rule_index = rule_index
        if self._network_id is None:
            raise ValueError("Network ID cannot be None for a firewall rule entity")
<<<<<<< HEAD
        rule_device_data = {**rule, "productType": "firewall_rule"}
=======

        rule_device_data = dataclasses.asdict(rule)
        rule_device_data["productType"] = "firewall_rule"

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        formatted_name = format_device_name(
            device=rule_device_data,
            config=self._config_entry.options,
        )

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    self._config_entry.domain,
                    f"firewall_rule_{network_id}_{rule_index}",
                ),
            },
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="L3 Firewall Rule",
            via_device=(self._config_entry.domain, f"network_{network_id}"),
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
