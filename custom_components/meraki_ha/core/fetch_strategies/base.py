"""Base fetch strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient


class BaseFetchStrategy:
    """Base class for fetch strategies."""

    def __init__(self, client: MerakiAPIClient, _disabled_features: set[str]) -> None:
        """
        Initialize the strategy.

        Args:
            client: The Meraki API client.
            _disabled_features: A set of disabled features.
        """
        self.client = client
        self._disabled_features = _disabled_features
