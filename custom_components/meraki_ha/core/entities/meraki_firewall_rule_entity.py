"""Base entity for Meraki Firewall Rules."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ...coordinator import MerakiDataUpdateCoordinator
from ...types import MerakiFirewallRule
from . import BaseMerakiEntity


class MerakiFirewallRuleEntity(BaseMerakiEntity):
    """Representation of a Meraki Firewall Rule."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    self._config_entry.domain,
                    f"firewall_rule_{network_id}_{rule_index}",
                ),
            },
            name=rule.comment,
            manufacturer="Cisco Meraki",
            model="L3 Firewall Rule",
            via_device=(self._config_entry.domain, f"network_{network_id}"),
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
