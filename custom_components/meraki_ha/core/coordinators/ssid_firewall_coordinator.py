"""Data update coordinator for Meraki SSID L7 firewall rules."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ....const import DOMAIN
from ....core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)

FIREWALL_RULE_COMMENT = "Managed by Home Assistant Meraki Parental Controls"


class SsidFirewallCoordinator(DataUpdateCoordinator):
    """A coordinator for Meraki L7 firewall settings for a single SSID."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        scan_interval: int,
        network_id: str,
        ssid_number: int,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_ssid_firewall_{network_id}_{ssid_number}",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api_client
        self.network_id = network_id
        self.ssid_number = ssid_number

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch SSID L7 firewall data from the API."""
        try:
            return await self.api.wireless.get_network_wireless_ssid_l7_firewall_rules(
                network_id=self.network_id, number=self.ssid_number
            )
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def async_block_client(self, client_ip: str):
        """Block a client by adding a firewall rule to the SSID."""
        rules = self.data.get("rules", [])
        new_rule = {
            "policy": "deny",
            "type": "ipRange",
            "value": client_ip,
            "comment": FIREWALL_RULE_COMMENT,
        }
        # Avoid adding duplicate rules
        if not any(r.get("value") == client_ip for r in rules):
            rules.append(new_rule)
            await self.api.wireless.update_network_wireless_ssid_l7_firewall_rules(
                network_id=self.network_id,
                number=self.ssid_number,
                rules=rules,
            )
            await self.async_refresh()

    async def async_unblock_client(self, client_ip: str):
        """Unblock a client by removing a firewall rule from the SSID."""
        rules = self.data.get("rules", [])
        updated_rules = [
            r
            for r in rules
            if not (
                r.get("value") == client_ip
                and r.get("comment") == FIREWALL_RULE_COMMENT
            )
        ]
        if len(updated_rules) < len(rules):
            await self.api.wireless.update_network_wireless_ssid_l7_firewall_rules(
                network_id=self.network_id,
                number=self.ssid_number,
                rules=updated_rules,
            )
            await self.async_refresh()
