"""Discovery coordinator for Meraki Orgs and Networks."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const.integration import DOMAIN
from ..core.api import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)


class DiscoveryCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to discover and map Meraki Orgs and Networks to HA Devices."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: MerakiApiClientProtocol,
    ) -> None:
        """Initialize the discovery coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_discovery",
            update_interval=timedelta(hours=1),
        )
        self.api = api
        self.config_entry = entry

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch organization and network data."""
        try:
            org = await self.api.organization.get_organization()
            networks = await self.api.organization.get_organization_networks()

            # Filter enabled networks if specified
            enabled_networks = networks
            if self.api.enabled_networks:
                enabled_networks = [
                    n
                    for n in networks
                    if n.get("id") in self.api.enabled_networks
                    or n.get("name") in self.api.enabled_networks
                ]

            data = {
                "organization": org,
                "networks": enabled_networks,
            }

            # Update the device registry with the hierarchical mapping
            await self._async_update_device_registry(data)

            return data
        except Exception as err:
            _LOGGER.error("Error fetching discovery data: %s", err)
            raise UpdateFailed(f"Error fetching discovery data: {err}") from err

    async def _async_update_device_registry(self, data: dict[str, Any]) -> None:
        """Update HA Device Registry with Organization and Network devices."""
        dev_reg = dr.async_get(self.hass)
        org = data.get("organization")
        if not org or not isinstance(org, dict):
            return

        org_id = org.get("id")
        org_name = org.get("name")
        if not org_id:
            return

        # 1. Create/Update Organization Device
        # This serves as the root of the Meraki hierarchy in HA.
        dev_reg.async_get_or_create(
            config_entry_id=self.config_entry.entry_id,
            identifiers={(DOMAIN, f"org_{org_id}")},
            name=f"Cisco Meraki: {org_name}",
            manufacturer="Cisco Meraki",
            model="Organization",
            entry_type=dr.DeviceEntryType.SERVICE,
            configuration_url=f"https://dashboard.meraki.com/o/{org_id}/manage/organization/overview",
        )

        # 2. Create/Update Network Devices
        # Each network is linked to the Organization device via via_device.
        for network in data.get("networks", []):
            if not isinstance(network, dict):
                continue
            net_id = network.get("id")
            net_name = network.get("name")
            if not net_id:
                continue

            dev_reg.async_get_or_create(
                config_entry_id=self.config_entry.entry_id,
                identifiers={(DOMAIN, f"network_{net_id}")},
                name=f"Meraki Network: {net_name}",
                manufacturer="Cisco Meraki",
                model="Network",
                via_device=(DOMAIN, f"org_{org_id}"),
                entry_type=dr.DeviceEntryType.SERVICE,
                configuration_url=f"https://dashboard.meraki.com/{net_id}/manage/usage/list",
            )
