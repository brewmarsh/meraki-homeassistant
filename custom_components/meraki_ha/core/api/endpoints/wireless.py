"""Meraki API endpoints for wireless devices."""

import logging
from typing import Any, Dict, List

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)
from ..cache import async_timed_cache

_LOGGER = logging.getLogger(__name__)


class WirelessEndpoints:
    """Wireless-related endpoints."""

    def __init__(self, api_client):
        """Initialize the endpoint."""
        self._api_client = api_client
        self._dashboard = api_client._dashboard

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_ssids(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all SSIDs for a network."""
        ssids = await self._api_client._run_sync(
            self._dashboard.wireless.get_network_wireless_ssids, networkId=network_id
        )
        validated = validate_response(ssids)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_ssids did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_wireless_settings(self, serial: str) -> Dict[str, Any]:
        """Get wireless radio settings for an access point."""
        settings = await self._api_client._run_sync(
            self._dashboard.wireless.get_device_wireless_radio_settings, serial=serial
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_wireless_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_wireless_ssid(
        self, network_id: str, number: str
    ) -> Dict[str, Any]:
        """Get a single SSID."""
        ssid = await self._api_client._run_sync(
            self._dashboard.wireless.get_network_wireless_ssid,
            networkId=network_id,
            number=number,
        )
        validated = validate_response(ssid)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_wireless_ssid did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_wireless_ssid(
        self, network_id: str, number: str, **kwargs
    ) -> Dict[str, Any]:
        """Update an SSID."""
        ssid = await self._api_client._run_sync(
            self._dashboard.wireless.update_network_wireless_ssid,
            networkId=network_id,
            number=number,
            **kwargs,
        )
        validated = validate_response(ssid)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_network_wireless_ssid did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_wireless_rf_profiles(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Get all RF profiles for a network."""
        profiles = await self._api_client._run_sync(
            self._dashboard.wireless.get_network_wireless_rf_profiles,
            networkId=network_id,
        )
        validated = validate_response(profiles)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_wireless_rf_profiles did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_wireless_ssid_l7_firewall_rules(
        self, network_id: str, number: str
    ) -> Dict[str, Any]:
        """Get L7 firewall rules for an SSID."""
        rules = await self._api_client._run_sync(
            self._dashboard.wireless.get_network_wireless_ssid_l7_firewall_rules,
            networkId=network_id,
            number=number,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "getNetworkWirelessSsidFirewallL7FirewallRules did not return a dict."
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_wireless_ssid_l7_firewall_rules(
        self, network_id: str, number: str, **kwargs
    ) -> Dict[str, Any]:
        """Update L7 firewall rules for an SSID."""
        rules = await self._api_client._run_sync(
            self._dashboard.wireless.update_network_wireless_ssid_l7_firewall_rules,
            networkId=network_id,
            number=number,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "updateNetworkWirelessSsidFirewallL7FirewallRules did not return a dict."
            )
            return {}
        return validated