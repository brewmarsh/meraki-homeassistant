"""
Meraki API client wrapper.

This module defines the main API client that acts as a facade for various
Meraki API endpoint categories.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from functools import partial
from typing import Any, cast

import meraki
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

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """
    Facade for the Meraki Dashboard API client.

    This client provides access to various endpoint categories and handles
    the underlying API session and asynchronous execution.
    """

    _disabled_features: set[str] = set()
    _enable_vpn_management: bool = False
    appliance: ApplianceEndpoints
    camera: CameraEndpoints
    devices: DevicesEndpoints
    network: NetworkEndpoints
    organization: OrganizationEndpoints
    switch: SwitchEndpoints
    wireless: WirelessEndpoints
    sensor: SensorEndpoints

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        base_url: str = "https://api.meraki.com/api/v1",
    ) -> None:
        """
        Initialize the API client.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The organization ID.
            base_url: The base URL for the Meraki API.

        """
        self._api_key = api_key
        self._org_id = org_id
        self._hass = hass
        self._base_url = base_url

        self.dashboard = meraki.DashboardAPI(
            api_key=self._api_key,
            base_url=self._base_url,
            output_log=False,
            print_console=False,
            suppress_logging=True,
            maximum_retries=3,
            wait_on_rate_limit=True,
            nginx_429_retry_wait_time=2,
        )

        # Initialize endpoint handlers
        self.appliance = ApplianceEndpoints(self, self._hass)
        self.camera = CameraEndpoints(self)
        self.devices = DevicesEndpoints(self)
        self.network = NetworkEndpoints(self)
        self.organization = OrganizationEndpoints(self)
        self.switch = SwitchEndpoints(self)
        self.wireless = WirelessEndpoints(self)
        self.sensor = SensorEndpoints(self)

        # Semaphore to limit concurrent API calls
        self._semaphore = asyncio.Semaphore(2)

        # Set of disabled features to prevent repetitive API calls
        self._disabled_features: set[str] = set()
        self._enable_vpn_management = False

    @property
    def has_dashboard(self) -> bool:
        """Check if the dashboard is initialized."""
        return self.dashboard is not None

    async def async_setup(self) -> None:
        """Perform asynchronous setup of the API client."""
        # Dashboard API is now initialized in __init__
        pass

    async def run_sync(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Run a synchronous function in a thread pool with rate limiting.

        Args:
            func: The synchronous function to run.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns
        -------
            The result of the function.

        """
        async with self._semaphore:
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, partial(func, *args, **kwargs)
                )
            except meraki.APIError as e:
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
                _LOGGER.debug("Meraki API Error stack trace", exc_info=True)
                raise ApiClientCommunicationError(
                    f"Error communicating with Meraki API: {e}"
                ) from e
            except Exception as e:
                _LOGGER.warning(
                    "An unexpected error occurred during API call: %s. Type: %s",
                    e,
                    type(e).__name__,
                )
                _LOGGER.debug("Unexpected API error stack trace", exc_info=True)
                if "JSON" in str(e):
                    raise ApiClientCommunicationError(
                        f"Invalid JSON response from Meraki API. "
                        f"Please check Meraki logs or network connectivity. "
                        f"Details: {e}"
                    ) from e
                else:
                    raise ApiClientCommunicationError(
                        f"An unexpected error occurred: {e}"
                    ) from e

        await asyncio.sleep(0.1)
        return result

    async def run_with_semaphore(self, coro: Awaitable[Any]) -> Any:
        """
        Run an awaitable with the rate limiter.

        Args:
            coro: The awaitable to run.

        Returns
        -------
            The result of the awaitable.

        """
        # Governance is now handled at the API level via run_sync.
        # This wrapper is maintained for compatibility with the fetch strategies.
        return await coro

    def mark_feature_disabled(
        self, feature: str, network_id: str | None = None
    ) -> None:
        """
        Mark a feature as disabled for the current session.

        Args:
            feature: The feature to disable (e.g., "traffic", "vlans").
            network_id: The ID of the network.

        """
        key = feature
        if network_id:
            key = f"{feature}_{network_id}"
        self._disabled_features.add(key)
        _LOGGER.debug("Feature %s marked as disabled for the session", key)

    def is_feature_disabled(self, feature: str, network_id: str | None = None) -> bool:
        """
        Check if a feature is disabled for the current session.

        Args:
            feature: The feature to check.
            network_id: The ID of the network.

        Returns
        -------
            True if disabled, False otherwise.

        """
        key = feature
        if network_id:
            key = f"{feature}_{network_id}"
        return key in self._disabled_features

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self._org_id

    async def register_webhook(
        self, webhook_url: str, secret: str, config_entry_id: str
    ) -> None:
        """
        Register a webhook with the Meraki API.

        Args:
            webhook_url: The URL of the webhook.
            secret: The secret for the webhook.
            config_entry_id: The ID of the Home Assistant config entry.

        """
        await self.network.register_webhook(webhook_url, secret, config_entry_id)

    async def unregister_webhook(self, config_entry_id: str) -> None:
        """
        Unregister a webhook with the Meraki API.

        Args:
            config_entry_id: The ID of the Home Assistant config entry.

        """
        await self.network.unregister_webhook(config_entry_id)

    async def async_reboot_device(self, serial: str) -> dict[str, Any]:
        """
        Reboot a device.

        Args:
            serial: The serial number of the device to reboot.

        Returns
        -------
            The API response.

        """
        return cast(dict[str, Any], await self.appliance.reboot_device(serial))

    async def async_get_switch_port_statuses(
        self,
        serial: str,
    ) -> list[dict[str, Any]]:
        """
        Get statuses for all ports of a switch.

        Args:
            serial: The serial number of the switch.

        Returns
        -------
            A list of port statuses.

        """
        return await self.switch.get_device_switch_ports_statuses(serial)

    async def async_cycle_switch_ports(
        self,
        serial: str,
        ports: list[str],
    ) -> dict[str, Any]:
        """
        Cycle a set of switch ports.

        Args:
            serial: The serial number of the switch.
            ports: A list of port IDs to cycle.

        Returns
        -------
            The API response.

        """
        return cast(
            dict[str, Any], await self.switch.cycle_device_switch_ports(serial, ports)
        )
