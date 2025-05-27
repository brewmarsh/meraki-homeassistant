"""Initializes the coordinators module for the Meraki Home Assistant integration.

This file re-exports the primary coordinator classes from their respective
modules. This makes them available for more straightforward import by other
parts of the integration, such as the main `__init__.py` or platform setup files.

The coordinators manage various aspects of data fetching, processing, and
distribution from the Meraki API.
"""

# Import and re-export key coordinator classes for simpler access from other modules.
from .base_coordinator import MerakiDataUpdateCoordinator
from .api_data_fetcher import MerakiApiDataFetcher
from .data_aggregation_coordinator import DataAggregationCoordinator
from .data_processor import MerakiDataProcessor # Added for completeness if used externally
from .data_aggregator import DataAggregator     # Added for completeness if used externally
from .device_coordinator import MerakiDeviceCoordinator # If still used
from .device_tag_update_coordinator import DeviceTagUpdateCoordinator # If still used
from .tag_eraser_coordinator import TagEraserCoordinator # If still used


# __all__ defines the public API of this module when `from .coordinators import *`
# is used. It's generally better to use direct imports, but __all__ is provided
# for completeness and to explicitly state what is intended for export.
__all__ = [
    "MerakiDataUpdateCoordinator",    # The main orchestrating coordinator.
    "MerakiApiDataFetcher",           # Handles direct API calls to fetch raw data.
    "DataAggregationCoordinator",     # Coordinates processing and aggregation of data.
    "MerakiDataProcessor",            # Processes raw data into structured formats.
    "DataAggregator",                 # Aggregates various data types and calculates statuses.
    "MerakiDeviceCoordinator",        # Example: If there's a specific device coordinator. (Review if still needed)
    "DeviceTagUpdateCoordinator",     # Handles updating device tags. (Review if still needed)
    "TagEraserCoordinator",           # Handles erasing tags from devices.
]

# Comments for removed coordinators (MerakiSsidCoordinator, MerakiNetworkCoordinator, DeviceTagFetchCoordinator)
# have been cleared from the __all__ list and imports.
# Ensure that MerakiDeviceCoordinator and DeviceTagUpdateCoordinator are still relevant
# and used. If not, they should also be removed from __all__ and imports.
# For this review, assuming they are still part of the active design.
