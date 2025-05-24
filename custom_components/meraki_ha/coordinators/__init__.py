"""Initializes the coordinators package for the Meraki Home Assistant integration.

This package contains various `DataUpdateCoordinator` implementations and related
helper classes responsible for fetching, processing, and managing data from the
Meraki API. Each coordinator typically handles a specific aspect of the Meraki
data, such as devices, networks, SSIDs, or tags.

This `__init__.py` file re-exports the primary coordinator classes for easier
access from other parts of the integration.
"""

# Explicitly re-exporting coordinators for cleaner imports elsewhere.
# The `as OriginalName` is redundant if the imported name is the same,
# but can be useful for clarity or if renaming is desired at this level.

from .api_data_fetcher import MerakiApiDataFetcher
from .data_aggregation_coordinator import DataAggregationCoordinator
from .device_coordinator import MerakiDeviceCoordinator
from .device_tag_fetch_coordinator import DeviceTagFetchCoordinator
from .device_tag_update_coordinator import DeviceTagUpdateCoordinator
from .network_coordinator import MerakiNetworkCoordinator
from .ssid_coordinator import MerakiSsidCoordinator
from .tag_eraser_coordinator import TagEraserCoordinator

__all__ = [
    "MerakiApiDataFetcher",
    "DataAggregationCoordinator",
    "MerakiDeviceCoordinator",
    "DeviceTagFetchCoordinator",
    "DeviceTagUpdateCoordinator",
    "MerakiNetworkCoordinator",
    "MerakiSsidCoordinator",
    "TagEraserCoordinator",
]
