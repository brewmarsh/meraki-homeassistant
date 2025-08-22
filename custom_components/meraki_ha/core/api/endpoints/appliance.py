"""Meraki API endpoints for appliances."""

import logging
from typing import Any, Dict, List

from ...utils.api_utils import handle_meraki_errors, validate_response
from ..cache import async_timed_cache

_LOGGER = logging.getLogger(__name__)


class ApplianceEndpoints:
    """Appliance-related endpoints."""

    def __init__(self, api_client):
        """Initialize the endpoint."""
        self._api_client = api_client
        self._dashboard = api_client._dashboard

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_appliance_traffic(
        self, network_id: str, timespan: int = 86400
    ) -> List[Dict[str, Any]]:
        """Get traffic data for a network appliance."""
        traffic = await self._api_client._run_sync(
            self._dashboard.networks.getNetworkTraffic,
            networkId=network_id,
            timespan=timespan,
            deviceType="appliance",
        )
        validated = validate_response(traffic)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_appliance_traffic did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_vlans(self, network_id: str) -> List[Dict[str, Any]]:
        """Get VLANs for a network."""
        vlans = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceVlans, networkId=network_id
        )
        validated = validate_response(vlans)
        if not isinstance(validated, list):
            _LOGGER.warning("get_vlans did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_device_appliance_uplinks_settings(
        self, serial: str
    ) -> Dict[str, Any]:
        """Get uplinks settings for a device."""
        uplinks = await self._api_client._run_sync(
            self._dashboard.appliance.getDeviceApplianceUplinksSettings, serial=serial
        )
        validated = validate_response(uplinks)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_device_appliance_uplinks_settings did not return a dict."
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_appliance_ports(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all ports for an appliance."""
        ports = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkAppliancePorts, networkId=network_id
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning("get_appliance_ports did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_settings(self, network_id: str) -> Dict[str, Any]:
        """Get settings for a network appliance."""
        settings = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceSettings, networkId=network_id
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_appliance_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_l7_firewall_rules(
        self, network_id: str
    ) -> Dict[str, Any]:
        """Get L7 firewall rules for a network."""
        rules = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceL7FirewallRules,
            networkId=network_id,
        )
        return validate_response(rules)
