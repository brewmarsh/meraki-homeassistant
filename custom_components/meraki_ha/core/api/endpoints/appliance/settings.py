"""Appliance settings endpoints."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.api.cache import async_timed_cache
from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

if TYPE_CHECKING:
    from custom_components.meraki_ha.core.api.protocol import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)


class ApplianceSettingsMixin:
    """Mixin for appliance settings endpoints."""

    if TYPE_CHECKING:
        _api_client: MerakiApiClientProtocol

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_vlans(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get VLANs for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            A list of VLANs.

        """
        vlans = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceVlans,
            networkId=network_id,
        )
        validated = validate_response(vlans)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_vlans did not return a list")
            return []
        return validated

    @handle_meraki_errors
    async def update_network_vlan(
        self,
        network_id: str,
        vlan_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update a VLAN.

        Args:
            network_id: The ID of the network.
            vlan_id: The ID of the VLAN.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated VLAN.

        """
        vlan = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.updateNetworkApplianceVlan,
            networkId=network_id,
            vlanId=vlan_id,
            **kwargs,
        )
        validated = validate_response(vlan)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_network_vlan did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def reboot_device(self, serial: str) -> dict[str, Any]:
        """
        Reboot a device.

        Args:
            serial: The serial number of the device.

        Returns
        -------
            The response from the API.

        """
        result = await self._api_client.run_sync(
            self._api_client.dashboard.devices.rebootDevice,
            serial=serial,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("reboot_device did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_appliance_ports(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get all ports for an appliance.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            A list of ports.

        """
        ports = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkAppliancePorts,
            networkId=network_id,
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning("get_appliance_ports did not return a list")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_settings(self, network_id: str) -> dict[str, Any]:
        """
        Get settings for a network appliance.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The settings for the network appliance.

        """
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceSettings,
            networkId=network_id,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_appliance_settings did not return a dict")
            return {}
        return validated
