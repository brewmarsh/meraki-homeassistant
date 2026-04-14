"""
Meraki API client wrapper.

This module defines the main API client that acts as a facade for various
Meraki API endpoint categories.
"""

from __future__ import annotations

import asyncio
import logging
import os
from collections.abc import Awaitable, Callable
from typing import Any, cast

import braintrust
import meraki.aio
from dotenv import load_dotenv

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from ...core.errors import (
    ApiClientCommunicationError,
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
)
from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.devices import DevicesEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.sensor import SensorEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints
from .protocol import (
    ApplianceEndpointsProtocol,
    CameraEndpointsProtocol,
    DevicesEndpointsProtocol,
    NetworkEndpointsProtocol,
    OrganizationEndpointsProtocol,
    SensorEndpointsProtocol,
    SwitchEndpointsProtocol,
    WirelessEndpointsProtocol,
)
from .shared_cache import MerakiApiCache

_LOGGER = logging.getLogger(__name__)

FRIENDLY_FEATURE_NAMES = {
    "getNetworkTraffic": "Network traffic analysis",
    "getNetworkApplianceVlans": "VLAN tracking",
    "getNetworkAppliancePorts": "Appliance port tracking",
    "getNetworkApplianceTraffic": "Appliance traffic analysis",
    "getNetworkApplianceFirewallL3FirewallRules": "L3 firewall rules",
    "getNetworkApplianceL7FirewallRules": "L7 firewall rules",
    "getNetworkApplianceContentFiltering": "Content filtering",
    "getNetworkApplianceVpnSiteToSiteVpn": "Site-to-site VPN",
    "getNetworkEvents": "Network events",
    "getDeviceCameraAnalyticsRecent": "Camera analytics",
}

# Initialize Braintrust for observability
load_dotenv()
if os.getenv("BRAINTRUST_API_KEY"):
    braintrust.init(project="Meraki HA", api_key=os.getenv("BRAINTRUST_API_KEY"))


class MerakiClient:
    """
    Facade for the Meraki Dashboard API client.

    This client provides access to various endpoint categories and handles
    the underlying API session and asynchronous execution.
    """

    _disabled_features: set[str] = set()
    _enable_vpn_management: bool = False

    # Type hints for endpoint protocols
    appliance: ApplianceEndpointsProtocol
    camera: CameraEndpointsProtocol
    devices: DevicesEndpointsProtocol
    network: NetworkEndpointsProtocol
    organization: OrganizationEndpointsProtocol
    switch: SwitchEndpointsProtocol
    wireless: WirelessEndpointsProtocol
    sensor: SensorEndpointsProtocol

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str | None = None,
        base_url: str = "https://api.meraki.com/api/v1",
        enabled_networks: list[str] | None = None,
    ) -> None:
        """Initialize the API client and compose endpoint handlers."""
        self._api_key = api_key
        self._org_id = org_id
        self._hass = hass
        self._base_url = base_url
        self.enabled_networks = enabled_networks or []

        self.dashboard: meraki.aio.AsyncDashboardAPI | None = None

        # Priority queue for API requests to ensure real-time updates aren't blocked
        self._priority_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._worker_tasks: list[asyncio.Task] = []

        # Shared cache for preventing thundering herd
        self.api_cache = MerakiApiCache()

        # Request counter for deterministic cache hit detection
        self.request_count = 0

        # Set of disabled features to prevent repetitive API calls
        self._disabled_features: set[str] = set()
        self._enable_vpn_management = False

        # Action 2: Initialize endpoint handlers to prevent AttributeErrors
        # in config flow
        self.organization = OrganizationEndpoints(self)
        self.appliance = ApplianceEndpoints(self, self._hass)
        self.camera = CameraEndpoints(self)
        self.devices = DevicesEndpoints(self)
        self.network = NetworkEndpoints(self)
        self.sensor = SensorEndpoints(self)
        self.switch = SwitchEndpoints(self)
        self.wireless = WirelessEndpoints(self)

    @property
    def has_dashboard(self) -> bool:
        """Check if the dashboard is initialized."""
        return self.dashboard is not None

    async def async_setup(self) -> None:
        """Perform asynchronous setup of the API client."""
        if self.dashboard is None:
            self.dashboard = meraki.aio.AsyncDashboardAPI(
                api_key=self._api_key,
                base_url=self._base_url,
                output_log=False,
                print_console=False,
                suppress_logging=True,
                maximum_retries=3,
                wait_on_rate_limit=True,
                nginx_429_retry_wait_time=2,
                aiohttp_session=async_get_clientsession(self._hass),
            )
        
        if self._worker_tasks is None or not self._worker_tasks:
            self._worker_tasks = [
                asyncio.create_task(self._worker_loop(i)) 
                for i in range(5) # 5 concurrent workers
            ]

    async def _worker_loop(self, worker_id: int) -> None:
        """Background worker loop to process API requests based on priority."""
        _LOGGER.debug("Starting Meraki API worker %d", worker_id)
        while True:
            try:
                priority, func, args, kwargs, future = await self._priority_queue.get()
                if future.done() or future.cancelled():
                    self._priority_queue.task_done()
                    continue

                self.request_count += 1
                try:
                    result = await func(*args, **kwargs)
                    if not future.done():
                        future.set_result(result)
                except Exception as e:
                    if not future.done():
                        future.set_exception(e)
                finally:
                    self._priority_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                _LOGGER.error("Error in Meraki API worker %d: %s", worker_id, e)
                await asyncio.sleep(1)

    @braintrust.traced
    async def run_async(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run an asynchronous function with rate limiting and priority."""
        # Default priority: 1 (Medium)
        # 0: High (Webhooks, User actions)
        # 1: Medium (Standard sensors)
        # 2: Low (Bulk polls, Background sync)
        priority = kwargs.pop("priority", 1)

        org_id = kwargs.get("organizationId") or self.organization_id
        serial = kwargs.get("serial") or kwargs.get("deviceSerial")
        if not serial and args and isinstance(args[0], str):
            serial = args[0]

        # Extract network_id for endpoint-specific blacklisting
        network_id = kwargs.get("networkId") or kwargs.get("network_id")
        if (
            not network_id
            and args
            and isinstance(args[0], str)
            and args[0].startswith(("N_", "L_"))
        ):
            network_id = args[0]

        # Action 3: Pre-flight check for blacklisted endpoints
        endpoint = getattr(func, "__name__", "mocked_endpoint")
        if self.is_feature_disabled(endpoint, network_id):
            _LOGGER.debug("Skipping blacklisted endpoint: %s", endpoint)
            return []

        braintrust.current_span().log(
            metadata={
                "organization_id": org_id,
                "device_serial": serial,
            }
        )

        # Use priority queue instead of direct semaphore acquisition
        future = asyncio.get_event_loop().create_future()
        await self._priority_queue.put((priority, func, args, kwargs, future))
        
        try:
            result = await future
        except Exception as e:
            # Capture any Meraki API specific error
            # Note: Async SDK still uses common APIError from meraki package
            import meraki
            if isinstance(e, meraki.APIError):
                braintrust.current_span().log(
                    metadata={
                        "error_message": str(e),
                        "status_code": getattr(e, "status", None),
                        "meraki_request_id": (
                            e.response.headers.get("X-Cisco-Meraki-API-Request-Id")
                            if e.response is not None and hasattr(e.response, "headers")
                            else None
                        ),
                    }
                )

                error_msg = str(e)
                status_code = getattr(e, "status", None)

                # Action 2: Endpoint-specific blacklisting for 400 errors
                if status_code == 400 and (
                    "not enabled" in error_msg.lower()
                    or "must be enabled" in error_msg.lower()
                ):
                    feature_name = FRIENDLY_FEATURE_NAMES.get(endpoint, endpoint)
                    _LOGGER.warning(
                        "%s is not enabled for network %s and will not be checked "
                        "until the integration restarts. To add %s support, enable "
                        "it on the Cisco Meraki dashboard.",
                        feature_name.capitalize(),
                        network_id or "Unknown",
                        feature_name.lower(),
                    )
                    self.mark_feature_disabled(endpoint, network_id)
                    return []

                if (
                    "Traffic Analysis with Hostname Visibility" in error_msg
                    or "VLANs are not enabled" in error_msg
                ):
                    _LOGGER.debug("Meraki API Informational Error: %s", e)
                    if "Traffic Analysis" in error_msg:
                        raise MerakiTrafficAnalysisError(error_msg) from e
                    if "VLANs" in error_msg:
                        raise MerakiVlansDisabledError(error_msg) from e
                    raise MerakiInformationalError(error_msg) from e
                _LOGGER.warning("Meraki API Error encountered: %s", e)
                raise ApiClientCommunicationError(
                    f"Error communicating with Meraki API: {e}"
                ) from e
            
            # Non-Meraki error
            _LOGGER.warning(
                "An unexpected error occurred: %s. Type: %s",
                e,
                type(e).__name__,
            )
            if "JSON" in str(e):
                raise ApiClientCommunicationError(
                    f"Invalid JSON response from Meraki API: {e}"
                ) from e
            raise ApiClientCommunicationError(
                f"An unexpected error occurred: {e}"
            ) from e

        await asyncio.sleep(0.1)
        return result

    async def run_with_semaphore(self, coro: Awaitable[Any]) -> Any:
        """Run an awaitable with the rate limiter (wrapped in run_async compatible way)."""
        # If it's already an awaitable, we wrap it in a function for run_async
        async def _wrapper():
            return await coro
        
        return await self.run_async(_wrapper, priority=2) # Bulk polls use priority 2


    async def run_with_cache(
        self, key: str, fetch_coro: Any, ttl: int | None = None
    ) -> Any:
        """Run an awaitable with the shared cache and lock."""
        return await self.api_cache.async_get_or_fetch(key, fetch_coro, ttl)

    def mark_feature_disabled(
        self, feature: str, network_id: str | None = None
    ) -> None:
        """Mark a feature as disabled for the current session."""
        key = feature
        if network_id:
            key = f"{feature}_{network_id}"
        self._disabled_features.add(key)
        _LOGGER.debug("Feature %s marked as disabled for the session", key)

    def is_feature_disabled(self, feature: str, network_id: str | None = None) -> bool:
        """Check if a feature is disabled for the current session."""
        key = feature
        if network_id:
            key = f"{feature}_{network_id}"
        return key in self._disabled_features

    @property
    def organization_id(self) -> str | None:
        """Get the organization ID."""
        return self._org_id

    async def register_webhook(
        self, webhook_url: str, secret: str, config_entry_id: str
    ) -> list[str]:
        """Register a webhook with the Meraki API."""
        return await self.network.register_webhook(webhook_url, secret, config_entry_id)

    async def unregister_webhook(self, config_entry_id: str) -> None:
        """Unregister a webhook with the Meraki API."""
        await self.network.unregister_webhook(config_entry_id)

    async def async_reboot_device(self, serial: str) -> dict[str, Any]:
        """Reboot a device via the appliance endpoint handler."""
        return cast(dict[str, Any], await self.appliance.reboot_device(serial))

    async def get_organizations(self) -> list[dict[str, Any]]:
        """Fetch organizations using the composed handler (Action 4)."""
        return await self.organization.get_organizations()

    async def async_get_switch_port_statuses(
        self,
        serial: str,
    ) -> list[dict[str, Any]]:
        """Get switch port statuses via the switch endpoint handler."""
        return await self.switch.get_device_switch_ports_statuses(serial)

    async def async_cycle_switch_ports(
        self,
        serial: str,
        ports: list[str],
    ) -> dict[str, Any]:
        """Cycle switch ports via the switch endpoint handler."""
        return cast(
            dict[str, Any], await self.switch.cycle_device_switch_ports(serial, ports)
        )
