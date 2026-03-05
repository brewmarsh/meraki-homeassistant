"""Protocol for Meraki API Client."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, Protocol

import meraki


class ApplianceEndpointsProtocol(Protocol):
    """Protocol for appliance endpoints."""

    ...


class CameraEndpointsProtocol(Protocol):
    """Protocol for camera endpoints."""

    ...


class DevicesEndpointsProtocol(Protocol):
    """Protocol for devices endpoints."""

    ...


class NetworkEndpointsProtocol(Protocol):
    """Protocol for network endpoints."""

    ...


class OrganizationEndpointsProtocol(Protocol):
    """Protocol for organization endpoints needed by the API Client."""

    async def get_organization_networks(self) -> list[dict[str, Any]]:
        """Get the organization networks."""
        ...


class SwitchEndpointsProtocol(Protocol):
    """Protocol for switch endpoints."""

    ...


class WirelessEndpointsProtocol(Protocol):
    """Protocol for wireless endpoints."""

    ...


class SensorEndpointsProtocol(Protocol):
    """Protocol for sensor endpoints."""

    ...


class MerakiApiClientProtocol(Protocol):
    """Protocol defining the interface for the Meraki API Client."""

    @property
    def dashboard(self) -> meraki.DashboardAPI:
        """Get the Dashboard API instance."""
        ...

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        ...

    @property
    def appliance(self) -> ApplianceEndpointsProtocol:
        """Get the appliance endpoints."""
        ...

    @property
    def camera(self) -> CameraEndpointsProtocol:
        """Get the camera endpoints."""
        ...

    @property
    def devices(self) -> DevicesEndpointsProtocol:
        """Get the devices endpoints."""
        ...

    @property
    def network(self) -> NetworkEndpointsProtocol:
        """Get the network endpoints."""
        ...

    @property
    def organization(self) -> OrganizationEndpointsProtocol:
        """Get the organization endpoints."""
        ...

    @property
    def switch(self) -> SwitchEndpointsProtocol:
        """Get the switch endpoints."""
        ...

    @property
    def wireless(self) -> WirelessEndpointsProtocol:
        """Get the wireless endpoints."""
        ...

    @property
    def sensor(self) -> SensorEndpointsProtocol:
        """Get the sensor endpoints."""
        ...

    async def run_sync(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run a synchronous function in a thread pool."""
        ...

    async def run_with_semaphore(self, coro: Awaitable[Any]) -> Any:
        """Run an awaitable with the semaphore."""
        ...
