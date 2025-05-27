"""Initializes the coordinators module for the Meraki Home Assistant integration.

This file re-exports the main coordinator classes from their respective
modules, making them available for easier import by other parts of the
integration. Coordinators are responsible for managing data fetching,
processing, and distribution for different aspects of the Meraki API
(e.g., devices, SSIDs, networks).
"""

# Import and re-export coordinators for cleaner access.
# Type hints for these are implicitly defined by the source classes.
from .api_data_fetcher import MerakiApiDataFetcher
from .data_aggregation_coordinator import DataAggregationCoordinator
from .device_coordinator import MerakiDeviceCoordinator
from .device_tag_fetch_coordinator import DeviceTagFetchCoordinator
from .device_tag_update_coordinator import DeviceTagUpdateCoordinator
from .network_coordinator import MerakiNetworkCoordinator
from .ssid_coordinator import MerakiSsidCoordinator
from .tag_eraser_coordinator import TagEraserCoordinator

# It's good practice to define __all__ to specify what is exported when
# `from .coordinators import *` is used, though direct imports are preferred.
__all__ = [
    "MerakiApiDataFetcher",
    "MerakiDeviceCoordinator",
    "MerakiSsidCoordinator",
    "MerakiNetworkCoordinator",
    "DeviceTagUpdateCoordinator",
    "TagEraserCoordinator",
    "DataAggregationCoordinator",
    "DeviceTagFetchCoordinator",
]
