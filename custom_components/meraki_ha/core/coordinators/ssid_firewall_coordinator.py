"""SSID Firewall coordinator for the Meraki integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...async_logging import async_log_time
from ...helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from ..api.client import MerakiAPIClient

_LOGGER = MerakiLoggers.COORDINATOR


class SsidFirewallCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for SSID firewall rules."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        network_id: str,
        ssid_number: int,
        scan_interval: int = 300,
        update_interval: int | None = None,
    ) -> None:
        """Initialize the SSID firewall coordinator."""
        self.api_client = api_client
        self.network_id = network_id
        self.ssid_number = ssid_number

        # Support both scan_interval and update_interval for compatibility
        interval = update_interval if update_interval is not None else scan_interval

        super().__init__(
            hass,
            _LOGGER,
            name=f"meraki_ssid_firewall_{network_id}_{ssid_number}",
            update_interval=timedelta(seconds=interval),
        )

    @async_log_time(MerakiLoggers.COORDINATOR, slow_threshold=3.0)
    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch SSID firewall data from the API."""
        try:
            wireless = self.api_client.wireless
            rules = await wireless.get_network_wireless_ssid_l7_firewall_rules(
                network_id=self.network_id,
                number=str(self.ssid_number),
            )
            return {"rules": rules}
        except Exception as err:
            raise UpdateFailed(f"Error fetching SSID firewall data: {err}") from err

    async def async_block_client(self, client_ip: str) -> None:
        """
        Block a client by adding a deny rule.

        Args:
        ----
            client_ip: The IP address of the client to block.

        """
        current_rules = self.data.get("rules", []) if self.data else []
        new_rule = {
            "policy": "deny",
            "type": "ipRange",
            "value": client_ip,
        }
        updated_rules = current_rules + [new_rule]
        await self.api_client.wireless.update_network_wireless_ssid_l7_firewall_rules(
            network_id=self.network_id,
            number=str(self.ssid_number),
            rules=updated_rules,
        )
        await self.async_request_refresh()

    async def async_unblock_client(self, client_ip: str) -> None:
        """
        Unblock a client by removing the deny rule.

        Args:
        ----
            client_ip: The IP address of the client to unblock.

        """
        current_rules = self.data.get("rules", []) if self.data else []
        updated_rules = [
            rule
            for rule in current_rules
            if not (rule.get("policy") == "deny" and client_ip in rule.get("value", ""))
        ]
        await self.api_client.wireless.update_network_wireless_ssid_l7_firewall_rules(
            network_id=self.network_id,
            number=str(self.ssid_number),
            rules=updated_rules,
        )
        await self.async_request_refresh()
