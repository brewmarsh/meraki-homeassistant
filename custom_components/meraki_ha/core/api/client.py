"""Meraki API client wrapper."""

import asyncio
from functools import partial
import logging
from typing import Any, Dict, List, Optional
import time

import meraki

from ..utils.api_utils import handle_meraki_errors, validate_response

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """Wrapper for the Meraki Dashboard API client.

    This client wraps the Meraki Python SDK to provide:
    - Async operation with proper threading
    - Consistent error handling and logging
    - Response validation and normalization
    - Intelligent caching with timeouts
    """

    def __init__(
        self,
        api_key: str,
        org_id: str,
        base_url: str = "https://api.meraki.com/api/v1",
    ) -> None:
        """Initialize the API client."""
        self._api_key = api_key
        self._org_id = org_id
        self._dashboard = meraki.DashboardAPI(
            api_key=api_key,
            base_url=base_url,
            output_log=False,
            print_console=False,
            suppress_logging=True,
            maximum_retries=3,
            calls_per_second=10,
            wait_on_rate_limit=True,
            nginx_429_retry_wait_time=2,
        )

        # Initialize cache
        self._cache: Dict[str, Any] = {}
        self._cache_timeout = 300  # 5 minutes
        self._last_cache_update: Dict[str, float] = {}

    async def _run_sync(self, func, *args, **kwargs) -> Any:
        """Run a synchronous function in a thread pool."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    def _get_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate a cache key for a function call."""
        return f"{func_name}:{hash(str(args) + str(sorted(kwargs.items())))}"

    def _get_cached_data(self, cache_key: str) -> Optional[Any]:
        """Get data from cache if it exists and is not expired."""
        if cache_key not in self._cache:
            return None

        last_update = self._last_cache_update.get(cache_key, 0)
        if time.time() - last_update > self._cache_timeout:
            return None

        return self._cache[cache_key]

    def _cache_data(self, cache_key: str, data: Any) -> None:
        """Cache data with current timestamp."""
        self._cache[cache_key] = data
        self._last_cache_update[cache_key] = time.time()

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self._org_id

    @handle_meraki_errors
    async def get_organization(self) -> Dict[str, Any]:
        """Get organization details."""
        cache_key = self._get_cache_key("get_organization")

        if cached := self._get_cached_data(cache_key):
            return cached

        org = await self._run_sync(
            self._dashboard.organizations.getOrganization, organizationId=self._org_id
        )
        validated = validate_response(org)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_networks(self) -> List[Dict[str, Any]]:
        """Get all networks in the organization."""
        cache_key = self._get_cache_key("get_networks")

        if cached := self._get_cached_data(cache_key):
            return cached

        networks = await self._run_sync(
            self._dashboard.organizations.getOrganizationNetworks,
            organizationId=self._org_id,
        )
        validated = validate_response(networks)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_devices(
        self, network_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all devices in the organization or a specific network."""
        cache_key = self._get_cache_key("get_devices", network_id)

        if cached := self._get_cached_data(cache_key):
            return cached

        if network_id:
            devices = await self._run_sync(
                self._dashboard.networks.getNetworkDevices, networkId=network_id
            )
        else:
            devices = await self._run_sync(
                self._dashboard.organizations.getOrganizationDevices,
                organizationId=self._org_id,
            )

        validated = validate_response(devices)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_device_statuses(self, network_id: str) -> List[Dict[str, Any]]:
        """Get status information for all devices in a network."""
        cache_key = self._get_cache_key("get_device_statuses", network_id)

        # Status data should have a shorter cache timeout
        self._cache_timeout = 60  # 1 minute

        if cached := self._get_cached_data(cache_key):
            return cached

        statuses = await self._run_sync(
            self._dashboard.networks.getNetworkDevicesStatuses, networkId=network_id
        )
        validated = validate_response(statuses)
        self._cache_data(cache_key, validated)

        # Reset cache timeout
        self._cache_timeout = 300
        return validated

    @handle_meraki_errors
    async def get_device_clients(self, serial: str) -> List[Dict[str, Any]]:
        """Get client information for a specific device."""
        cache_key = self._get_cache_key("get_device_clients", serial)

        # Client data should have a shorter cache timeout
        self._cache_timeout = 60  # 1 minute

        if cached := self._get_cached_data(cache_key):
            return cached

        clients = await self._run_sync(
            self._dashboard.devices.getDeviceClients, serial=serial
        )
        validated = validate_response(clients)
        self._cache_data(cache_key, validated)

        # Reset cache timeout
        self._cache_timeout = 300
        return validated

    @handle_meraki_errors
    async def get_ssids(self, network_id: str) -> List[Dict[str, Any]]:
        """Get wireless SSIDs for a network."""
        cache_key = self._get_cache_key("get_ssids", network_id)

        if cached := self._get_cached_data(cache_key):
            return cached

        ssids = await self._run_sync(
            self._dashboard.wireless.getNetworkWirelessSsids, networkId=network_id
        )
        validated = validate_response(ssids)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_vlans(self, network_id: str) -> List[Dict[str, Any]]:
        """Get VLANs for a network."""
        cache_key = self._get_cache_key("get_vlans", network_id)

        if cached := self._get_cached_data(cache_key):
            return cached

        vlans = await self._run_sync(
            self._dashboard.appliance.getNetworkApplianceVlans, networkId=network_id
        )
        validated = validate_response(vlans)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_switch_ports(self, serial: str) -> List[Dict[str, Any]]:
        """Get ports for a switch."""
        cache_key = self._get_cache_key("get_switch_ports", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        ports = await self._run_sync(
            self._dashboard.switch.getDeviceSwitchPorts, serial=serial
        )
        validated = validate_response(ports)
        self._cache_data(cache_key, validated)
        return validated

    @handle_meraki_errors
    async def get_wireless_settings(self, serial: str) -> Dict[str, Any]:
        """Get wireless radio settings for an access point."""
        cache_key = self._get_cache_key("get_wireless_settings", serial)

        if cached := self._get_cached_data(cache_key):
            return cached

        settings = await self._run_sync(
            self._dashboard.wireless.getDeviceWirelessRadioSettings, serial=serial
        )
        validated = validate_response(settings)
        self._cache_data(cache_key, validated)
        return validated
