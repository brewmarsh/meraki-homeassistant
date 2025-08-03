"""
Meraki API client wrapper.

This module defines the main API client that acts as a facade for various
Meraki API endpoint categories.
"""

import asyncio
from functools import partial
import logging
from typing import Any

import meraki

from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """
    Facade for the Meraki Dashboard API client.
    This client provides access to various endpoint categories and handles
    the underlying API session and asynchronous execution.
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
            wait_on_rate_limit=True,
            nginx_429_retry_wait_time=2,
        )

        # Initialize endpoint handlers
        self.appliance = ApplianceEndpoints(self)
        self.camera = CameraEndpoints(self)
        self.network = NetworkEndpoints(self)
        self.organization = OrganizationEndpoints(self)
        self.switch = SwitchEndpoints(self)
        self.wireless = WirelessEndpoints(self)

    async def _run_sync(self, func, *args, **kwargs) -> Any:
        """Run a synchronous function in a thread pool."""
        _LOGGER.debug("Running synchronous function: %s", func.__name__)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    async def get_all_data(self) -> dict:
        """Fetch all data from the Meraki API."""
        networks = await self.organization.get_organization_networks()
        devices = await self.organization.get_organization_devices()
        clients = []
        for network in networks:
            clients.extend(await self.network.get_network_clients(network["id"]))
        ssids = []
        for network in networks:
            ssids.extend(await self.wireless.get_network_ssids(network["id"]))

        for device in devices:
            if device.get("productType") == "wireless":
                radio_settings = await self.wireless.get_wireless_settings(
                    device["serial"]
                )
                device["radio_settings"] = radio_settings
        return {
            "networks": networks,
            "devices": devices,
            "clients": clients,
            "ssids": ssids,
        }

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self._org_id

    async def register_webhook(self, webhook_url: str, secret: str) -> None:
        """Register a webhook with the Meraki API."""
        # This is a placeholder. The actual implementation will be added in a future step.
        pass
