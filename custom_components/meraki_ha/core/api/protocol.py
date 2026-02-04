"""Protocol for Meraki API Client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Protocol

import meraki

if TYPE_CHECKING:
    from .endpoints.organization import OrganizationEndpoints


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
    def organization(self) -> OrganizationEndpoints:
        """Get the organization endpoints."""
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

    async def get_vlan_data(self, network_id: str) -> list[dict[str, Any]]:
        """Get VLAN data with fallback logic."""
        ...
