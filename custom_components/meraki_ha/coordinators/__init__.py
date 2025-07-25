"""Initializes the coordinators module for the Meraki Home Assistant integration.

This file re-exports the primary coordinator classes from their respective
modules. This makes them available for more straightforward import by other
parts of the integration, such as the main `__init__.py` or platform setup files.

The coordinators manage various aspects of data fetching, processing, and
distribution from the Meraki API.
"""

# Import and re-export key coordinator classes for simpler access from
# other modules.
from .base_coordinator import (
    MerakiDataUpdateCoordinator,
)

# Added for completeness if used externally
from .data_processor import MerakiDataProcessor

# Added for completeness if used externally
from .data_aggregator import DataAggregator

# MerakiDeviceCoordinator import removed as file is deleted
# DeviceTagUpdateCoordinator import removed as file is deleted
from .tag_eraser_coordinator import (
    TagEraserCoordinator,
)  # If still used
from .ssid_device_coordinator import (
    SSIDDeviceCoordinator,
)


# __all__ defines the public API of this module when `from .coordinators import *`
# is used. It's generally better to use direct imports, but __all__ is provided
# for completeness and to explicitly state what is intended for export.
__all__ = [
    "MerakiDataUpdateCoordinator",  # The main orchestrating coordinator.
    # Handles direct API calls to fetch raw data.
    "MerakiApiDataFetcher",
    # Coordinates processing and aggregation of data.
    "DataAggregationCoordinator",
    # Processes raw data into structured formats.
    "MerakiDataProcessor",
    # Aggregates various data types and calculates statuses.
    "DataAggregator",
    # MerakiDeviceCoordinator removed from __all__
    # DeviceTagUpdateCoordinator removed from __all__
    "TagEraserCoordinator",  # Handles erasing tags from devices.
    "SSIDDeviceCoordinator",  # Manages SSID data and device registration.
]

# Comments for removed coordinators (MerakiSsidCoordinator, MerakiNetworkCoordinator, DeviceTagFetchCoordinator, DeviceTagUpdateCoordinator)
# have been cleared from the __all__ list and imports.
# Ensure that TagEraserCoordinator is still relevant
# and used. If not, they should also be removed from __all__ and imports.
# For this review, assuming it is still part of the active design.
