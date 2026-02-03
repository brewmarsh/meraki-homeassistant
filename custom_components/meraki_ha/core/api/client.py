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
from typing import TYPE_CHECKING, Any, cast

import meraki
from homeassistant.core import HomeAssistant

from ...core.errors import (
    ApiClientCommunicationError,
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
)
from ...types import MerakiDevice, MerakiNetwork
from ..coordinator_helpers.client_fetcher import ClientFetcher
from ..coordinator_helpers.detail_fetcher import DetailFetcher
from ..coordinator_helpers.detail_processor import DetailProcessor
from ..coordinator_helpers.device_fetcher import DeviceFetcher
from ..parsers.appliance import parse_appliance_data
from ..parsers.devices import parse_device_data
from ..parsers.sensors import parse_sensor_data
from .endpoints.appliance import ApplianceEndpoints
from .endpoints.camera import CameraEndpoints
from .endpoints.devices import DevicesEndpoints
from .endpoints.network import NetworkEndpoints
from .endpoints.organization import OrganizationEndpoints
from .endpoints.sensor import SensorEndpoints
from .endpoints.switch import SwitchEndpoints
from .endpoints.wireless import WirelessEndpoints

if TYPE_CHECKING:
    from ...coordinator import MerakiDataUpdateCoordinator


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
        coordinator: MerakiDataUpdateCoordinator | None = None,
        base_url: str = "https://api.meraki.com/api/v1",
        enable_vpn_management: bool = False,
    ) -> None:
        """
        Initialize the API client.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The organization ID.
            coordinator: The data update coordinator.
            base_url: The base URL for the Meraki API.
            enable_vpn_management: Whether to enable VPN management.

        """
        self._api_key = api_key
        self._org_id = org_id
        self._hass = hass
        self.coordinator = coordinator
        self._base_url = base_url
        self._enable_vpn_management = enable_vpn_management

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

        # Initialize helper classes
        self.client_fetcher = ClientFetcher(self)
        self.device_fetcher = DeviceFetcher(self)
        self.detail_fetcher = DetailFetcher(self)
        self.detail_processor = DetailProcessor(self)

        # Semaphore to limit concurrent API calls
        self._semaphore = asyncio.Semaphore(2)

        # Set of disabled features to prevent repetitive API calls
        self._disabled_features: set[str] = set()

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
                raise MerakiInformationalError(str(e