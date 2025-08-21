"""Data update coordinator for Meraki client firewall rules."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...const import DOMAIN
from ...core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)

FIREWALL_RULE_COMMENT = "Managed by Home Assistant Meraki Parental Controls"


class ClientFirewallCoordinator(DataUpdateCoordinator):
    """A coordinator for Meraki client firewall settings for a single network."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        scan_interval: int,
        network_id: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_client_firewall_{network_id}",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api_client
        self.network_id = network_id

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch client and firewall data from the API."""
        try:
            clients = await self.api.network.get_network_clients(
                network_id=self.network_id
            )
            l7_firewall_rules = (
                await self.api.appliance.get_network_appliance_l7_firewall_rules(
                    network_id=self.network_id
                )
            )
            return {"clients": clients, "l7_firewall_rules": l7_firewall_rules}
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def async_block_client(self, client_ip: str):
        """Block a client by adding a firewall rule."""
        rules = self.data.get("l7_firewall_rules", {}).get("rules", [])
        new_rule = {
            "policy": "deny",
            "type": "ipRange",
            "value": client_ip,
            "comment": FIREWALL_RULE_COMMENT,
        }
        # Avoid adding duplicate rules
        if not any(r == new_rule for r in rules):
            rules.append(new_rule)
            await self.api.appliance.update_network_appliance_l7_firewall_rules(
                network_id=self.network_id, rules=rules
            )
            await self.async_refresh()

    async def async_unblock_client(self, client_ip: str):
        """Unblock a client by removing a firewall rule."""
        rules = self.data.get("l7_firewall_rules", {}).get("rules", [])
        updated_rules = [
            r
            for r in rules
            if not (
                r.get("value") == client_ip
                and r.get("comment") == FIREWALL_RULE_COMMENT
            )
        ]
        if len(updated_rules) < len(rules):
            await self.api.appliance.update_network_appliance_l7_firewall_rules(
                network_id=self.network_id, rules=updated_rules
            )
            await self.async_refresh()
