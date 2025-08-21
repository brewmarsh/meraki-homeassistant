"""Meraki API endpoints for wireless devices."""

import logging
from typing import Any, Dict, List

from ...utils.api_utils import handle_meraki_errors, validate_response
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
            self._dashboard.wireless.getNetworkWirelessSsids, networkId=network_id
        )
        validated = validate_response(ssids)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_ssids did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_wireless_ssid(
        self, network_id: str, number: str
    ) -> Dict[str, Any]:
        """Get a single SSID."""
        ssid = await self._api_client._run_sync(
            self._dashboard.wireless.getNetworkWirelessSsid,
            networkId=network_id,
            number=number,
        )
        return validate_response(ssid)

    @handle_meraki_errors
    @async_timed_cache()
    async def get_wireless_settings(self, serial: str) -> Dict[str, Any]:
        """Get wireless radio settings for an access point."""
        settings = await self._api_client._run_sync(
            self._dashboard.wireless.getDeviceWirelessRadioSettings, serial=serial
        )
        return validate_response(settings)

    @handle_meraki_errors
    async def update_network_wireless_ssid(
        self, network_id: str, number: str, **kwargs
    ) -> Dict[str, Any]:
        """Update an SSID."""
        ssid = await self._api_client._run_sync(
            self._dashboard.wireless.updateNetworkWirelessSsid,
            networkId=network_id,
            number=number,
            **kwargs,
        )
        return validate_response(ssid)

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_wireless_rf_profiles(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Get all RF profiles for a network."""
        profiles = await self._api_client._run_sync(
            self._dashboard.wireless.getNetworkWirelessRfProfiles,
            networkId=network_id,
        )
        validated = validate_response(profiles)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_wireless_rf_profiles did not return a list.")
            return []
        return validated
