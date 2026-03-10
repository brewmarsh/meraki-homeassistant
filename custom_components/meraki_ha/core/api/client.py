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
from functools import partial
from typing import Any, cast

import braintrust
import meraki
from dotenv import load_dotenv
from homeassistant.core import HomeAssistant

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

_LOGGER = logging.getLogger(__name__)

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
    ) -> None:
        """Initialize the API client and compose endpoint handlers."""
        self._api_key = api_key
        self._org_id = org_id
        self._hass = hass
        self._base_url = base_url

        self.dashboard: meraki.DashboardAPI | None = None

        # Semaphore to limit concurrent API calls
        self._semaphore = asyncio.Semaphore(2)

        # Set of disabled features to prevent repetitive API calls
        self._disabled_features: set[str] = set()
        self._enable_vpn_management = False

        # Action 2: Initialize endpoint handlers to prevent AttributeErrors in config flow
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
            self.dashboard = await self._hass.async_add_executor_job(
                partial(
                    meraki.DashboardAPI,
                    api_key=self._api_key,
                    base_url=self._base_url,
                    output_log=False,
                    print_console=False,
                    suppress_logging=True,
                    maximum_retries=3,
                    wait_on_rate_limit=True,
                    nginx_429_retry_wait_time=2,
                )
            )

    @braintrust.traced
    async def run_sync(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run a synchronous function in a thread pool with rate limiting."""
        org_id = kwargs.get("organizationId") or self.organization_id
        serial = kwargs.get("serial") or kwargs.get("deviceSerial")
        if not serial and args and isinstance(args[0], str):
            serial = args[0]

        braintrust.current_span().log(
            metadata={
                "organization_id": org_id,
                "device_serial": serial,
            }
        )

        async with self._semaphore:
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, partial(func, *args, **kwargs)
                )
            except meraki.APIError as e:
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
            except Exception as e:
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
        """Run an awaitable with the rate limiter."""
        return await coro

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
        """Action 4: Fetch organizations using the composed handler."""
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
