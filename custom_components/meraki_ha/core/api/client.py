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

        self._dashboard: meraki.DashboardAPI | None = None

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

    @property
    def has_dashboard(self) -> bool:
        """Check if the dashboard is initialized."""
        return self._dashboard is not None

    @property
    def dashboard(self) -> meraki.DashboardAPI:
        """
        Get the Dashboard API instance.

        Returns
        -------
            The Dashboard API instance.

        Raises
        ------
            RuntimeError: If the Dashboard API has not been initialized.

        """
        if self._dashboard is None:
            raise RuntimeError(
                "Meraki Dashboard API not initialized. Call async_setup() first."
            )
        return self._dashboard

    @dashboard.setter
    def dashboard(self, value: meraki.DashboardAPI | None) -> None:
        """Set the Dashboard API instance."""
        self._dashboard = value

    async def async_setup(self) -> None:
        """Perform asynchronous setup of the API client."""
        self._dashboard = await self._hass.async_add_executor_job(
            self._create_dashboard_api
        )

    def _create_dashboard_api(self) -> meraki.DashboardAPI:
        """Create and return the MerakiDashboardAPI instance."""
        return meraki.DashboardAPI(
            api_key=self._api_key,
            base_url=self._base_url,
            output_log=False,
            print_console=False,
            suppress_logging=True,
            maximum_retries=3,
            wait_on_rate_limit=True,
            nginx_429_retry_wait_time=2,
        )

    async def run_sync(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Run a synchronous function in a thread pool.

        Args:
            func: The synchronous function to run.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns
        -------
            The result of the function.

        """
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, partial(func, *args, **kwargs))
        except meraki.APIError as e:
            error_str = str(e).lower()
            if "traffic analysis" in error_str or "vlans are not enabled" in error_str:
                _LOGGER.info("Meraki API Informational Error: %s", e)
                if "traffic analysis" in error_str:
                    raise MerakiTrafficAnalysisError(str(e)) from e
                if "vlans are not enabled" in error_str:
                    raise MerakiVlansDisabledError(str(e)) from e
                raise MerakiInformationalError(str(e)) from e
            _LOGGER.error(
                "Meraki API Error encountered: %s",
                e,
                exc_info=True,
            )
            raise ApiClientCommunicationError(
                f"Error communicating with Meraki API: {e}"
            ) from e
        except Exception as e:
            _LOGGER.error(
                "An unexpected error occurred during API call: %s. Type: %s",
                e,
                type(e).__name__,
                exc_info=True,
            )
            if "JSON" in str(e):
                raise ApiClientCommunicationError(
                    f"Invalid JSON response from Meraki API. "
                    f"Please check Meraki logs or network connectivity. Details: {e}"
                ) from e
            else:
                raise ApiClientCommunicationError(
                    f"An unexpected error occurred: {e}"
                ) from e

    async def run_with_semaphore(self, coro: Awaitable[Any]) -> Any:
        """
        Run an awaitable with the semaphore.

        Args:
            coro: The awaitable to run.

        Returns
        -------
            The result of the awaitable.

        """
        async with self._semaphore:
            return await coro

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

    async def get_network_events(
        self,
        network_id: str,
        product_type: str | None = None,
        included_event_types: list[str] | None = None,
        excluded_event_types: list[str] | None = None,
        device_serial: str | None = None,
        device_mac: str | None = None,
        client_ip: str | None = None,
        client_mac: str | None = None,
        client_name: str | None = None,
        sm_device_mac: str | None = None,
        sm_device_name: str | None = None,
        per_page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> dict[str, Any]:
        """
        Fetch events for a network.

        Args:
            network_id: The ID of the network.
            product_type: Filter events by product type.
            included_event_types: Filter events by included event types.
            excluded_event_types: Filter events by excluded event types.
            device_serial: Filter events by device serial.
            device_mac: Filter events by device MAC.
            client_ip: Filter events by client IP.
            client_mac: Filter events by client MAC.
            client_name: Filter events by client name.
            sm_device_mac: Filter events by SM device MAC.
            sm_device_name: Filter events by SM device name.
            per_page: Number of events per page.
            starting_after: Token for next page.
            ending_before: Token for previous page.

        Returns
        -------
            A dictionary containing the events and next page token.

        """
        if not self._dashboard:
            await self.async_setup()

        # Create dictionary of arguments and filter out None values
        kwargs = {
            "productType": product_type,
            "includedEventTypes": included_event_types,
            "excludedEventTypes": excluded_event_types,
            "deviceSerial": device_serial,
            "deviceMac": device_mac,
            "clientIp": client_ip,
            "clientMac": client_mac,
            "clientName": client_name,
            "smDeviceMac": sm_device_mac,
            "smDeviceName": sm_device_name,
            "perPage": per_page,
            "startingAfter": starting_after,
            "endingBefore": ending_before,
        }
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        return await self.run_with_semaphore(
            self.run_sync(
                self.dashboard.networks.getNetworkEvents,
                network_id,
                **filtered_kwargs,
            )
        )
