"""Base fetch strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..api import MerakiApiClientProtocol
    from ..models.device import MerakiDevice


class BaseFetchStrategy:
    """Base class for fetch strategies."""

    def __init__(
        self, client: MerakiApiClientProtocol, _disabled_features: set[str]
    ) -> None:
        """
        Initialize the strategy.

        Args:
            client: The Meraki API client.
            _disabled_features: A set of disabled features.
        """
        self.client = client
        self._disabled_features = _disabled_features

    def build_device_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, Any],
        capabilities: list[str],
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """
        Add per-device detail tasks based on capabilities.

        Args:
            device: The Meraki device.
            tasks: The task dictionary to add to.
            capabilities: The list of device capabilities.
            detail_data: Optional dictionary of already fetched data.
        """

    def process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """
        Process per-device detail results.

        Args:
            device: The Meraki device.
            detail_data: The fetched detail data.
            prev_device: The previous device data for state retention.
        """
