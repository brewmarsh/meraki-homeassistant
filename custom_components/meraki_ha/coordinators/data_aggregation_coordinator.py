"""Data Aggregation Coordinator for the Meraki Home Assistant integration.

This module defines `DataAggregationCoordinator`, responsible for taking raw
data fetched by `MerakiApiDataFetcher` (devices with tags, SSIDs, networks),
processing it using `MerakiDataProcessor`, and then aggregating it into a
unified structure with `DataAggregator`. This final structure is used by
Home Assistant entities.
"""

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

# SsidStatusCalculator is used by DataAggregator, not directly here.
from custom_components.meraki_ha.coordinators.data_aggregator import DataAggregator
from custom_components.meraki_ha.coordinators.data_processor import MerakiDataProcessor

if TYPE_CHECKING:
    # To avoid circular import issues, type hint the parent coordinator.
    from custom_components.meraki_ha.coordinators.base_coordinator import (
        MerakiDataUpdateCoordinator,
    )


_LOGGER = logging.getLogger(__name__)


class DataAggregationCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Aggregates raw Meraki data from various sources into a structured format.

    This coordinator is called by `MerakiDataUpdateCoordinator` (the parent)
    with raw data lists for devices, SSIDs, and networks. It uses
    `MerakiDataProcessor` to transform this raw data into a standardized format.
    For camera devices, it additionally fetches and merges specific sense settings
    (like `senseEnabled` and `audioDetection`) into the device's data.
    Finally, it uses `DataAggregator` to combine all processed data and calculate
    SSID statuses. Device tags are expected to be included within the `device_data`.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        scan_interval: timedelta,  # For DataUpdateCoordinator superclass
        coordinator: "MerakiDataUpdateCoordinator",  # Parent coordinator instance
    ) -> None:
        """Initialize the DataAggregationCoordinator.

        Args:
            hass: The Home Assistant instance.
            scan_interval: The interval for updating data (passed to superclass).
                           This coordinator updates when `_async_update_data` is called.
            coordinator: The main `MerakiDataUpdateCoordinator` instance, providing
                         context (e.g., for MerakiDataProcessor).
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data Aggregation Coordinator",  # More specific name
            update_interval=scan_interval,
            # For DataUpdateCoordinator's scheduling if used independently.
        )
        # Store parent coordinator
        self.coordinator: "MerakiDataUpdateCoordinator" = coordinator

        # Initialize helper classes for data processing and aggregation.
        # MerakiDataProcessor handles initial structuring of raw data.
        self.data_processor: MerakiDataProcessor = MerakiDataProcessor(
            # Pass parent for context if needed by processor.
            coordinator=self.coordinator
        )

        # Initialize SsidStatusCalculator first
        from custom_components.meraki_ha.helpers.ssid_status_calculator import (
            SsidStatusCalculator,
        )
        self.ssid_status_calculator: SsidStatusCalculator = SsidStatusCalculator()

        # DataAggregator combines processed data and calculates SSID statuses.
        # It no longer takes data_processor as an argument.
        self.data_aggregator: DataAggregator = DataAggregator(
            ssid_status_calculator=self.ssid_status_calculator,
        )

        # Ensure `self.data` (from DataUpdateCoordinator) is initialized.
        self.data: Dict[str, Any] = {}

    async def _async_update_data(
        self,
        # Raw device data from ApiDataFetcher
        device_data: Optional[List[Dict[str, Any]]],
        # Raw SSID data from ApiDataFetcher
        ssid_data: Optional[List[Dict[str, Any]]],
        # Raw network data from ApiDataFetcher
        network_data: Optional[List[Dict[str, Any]]],
        client_data: Optional[List[Dict[str, Any]]],
        network_client_counts: Optional[Dict[str, int]],
        clients_on_ssids: int = 0,
        clients_on_appliances: int = 0,
        clients_on_wireless: int = 0,
        # The `device_tags` parameter has been removed; tags are in
        # `device_data`.
    ) -> Dict[str, Any]:
        """Process and aggregate raw Meraki data, including camera-specific details.

        This method is called by the parent `MerakiDataUpdateCoordinator` with the latest
        raw data fetched by `MerakiApiDataFetcher`. It performs the following steps:
        1. Processes raw device, network, and SSID data using `MerakiDataProcessor`.
        2. For devices identified as cameras (by productType or model prefix 'MV'),
           it fetches additional camera sense settings (e.g., `senseEnabled`,
           `audioDetection`) using `self.coordinator.meraki_client.get_camera_sense_settings()`
           and merges these settings into the respective device's data dictionary.
           Errors during this fetch are logged, and processing continues without
           the specific camera settings for the affected device.
        3. Uses `DataAggregator` to combine all processed data (now including
           enriched camera data) and determine SSID operational statuses.

        Args:
            device_data: A list of raw device dictionaries from the API.
                         Expected to include tags. Can be None if initial fetching failed.
            ssid_data: A list of raw SSID dictionaries from the API.
                       Can be None if initial fetching failed.
            network_data: A list of raw network dictionaries from the API.
                          Can be None if initial fetching failed.
            client_data: A list of raw client dictionaries from the API. Can be None.
            network_client_counts: Dictionary mapping network IDs to client counts. Can be None.
            clients_on_ssids: Total count of clients connected to SSIDs.
            clients_on_appliances: Total count of clients connected to appliances.
            clients_on_wireless: Total count of wireless clients.

        Returns:
            A dictionary containing the aggregated and processed data, ready for
            use by Home Assistant entities. Returns an empty dictionary if
            essential input data is missing or an error occurs.

        Raises:
            UpdateFailed: If a significant error occurs during data processing
                          or aggregation that prevents a meaningful update.
        """
        _LOGGER.debug(
            "DataAggregationCoordinator received raw data. Processing and aggregating..."
        )
        try:
            # Validate that essential input data is available.
            if device_data is None or ssid_data is None or network_data is None:
                _LOGGER.error( # Changed to error
                    "Essential data (devices, SSIDs, or networks) is None. "
                    "Cannot proceed with data aggregation."
                )
                raise UpdateFailed("Essential data missing for aggregation.")

            # Step 0: Validate optional inputs client_data and network_client_counts
            sanitized_client_data: Optional[List[Dict[str, Any]]] = None
            if client_data is not None:
                if isinstance(client_data, list):
                    sanitized_client_data = []
                    for i, client_item in enumerate(client_data):
                        if isinstance(client_item, dict):
                            sanitized_client_data.append(client_item)
                        else:
                            _LOGGER.warning("Item at index %d in client_data is not a dictionary, skipping: %s", i, str(client_item)[:100])
                else:
                    _LOGGER.warning("'client_data' provided but is not a list (type: %s). Treating as None.", type(client_data).__name__)

            sanitized_network_client_counts: Optional[Dict[str, int]] = None
            if network_client_counts is not None:
                if isinstance(network_client_counts, dict):
                    sanitized_network_client_counts = network_client_counts
                else:
                    _LOGGER.warning("'network_client_counts' provided but is not a dict (type: %s). Treating as None.", type(network_client_counts).__name__)

            # Step 1: Sanitize and Process raw device data
            sanitized_device_data: List[Dict[str, Any]] = []
            if isinstance(device_data, list): # device_data itself is confirmed not None by earlier check
                for i, device_item in enumerate(device_data):
                    if not isinstance(device_item, dict):
                        _LOGGER.warning("Item at index %d in device_data is not a dictionary, skipping: %s", i, str(device_item)[:100])
                        continue
                    # Basic validation for critical keys (example)
                    if not device_item.get("serial") or not isinstance(device_item.get("serial"), str):
                        _LOGGER.warning("Device item at index %d missing or invalid 'serial', skipping: %s", i, str(device_item)[:100])
                        continue
                    if not device_item.get("model") or not isinstance(device_item.get("model"), str):
                        _LOGGER.warning("Device item at index %d missing or invalid 'model', skipping: %s", i, str(device_item)[:100])
                        continue
                    raw_tags = device_item.get("tags")
                    if raw_tags is not None and not isinstance(raw_tags, list):
                        _LOGGER.warning("Device item at index %d has 'tags' but it's not a list (type: %s). Correcting to empty list. Device: %s",
                                        i, type(raw_tags).__name__, device_item.get("serial", "N/A"))
                        device_item["tags"] = []
                    elif isinstance(raw_tags, list):
                        device_item["tags"] = [str(tag) for tag in raw_tags if isinstance(tag, str)] # Ensure tags are strings

                    sanitized_device_data.append(device_item)
                processed_devices = await self.data_processor.process_devices(sanitized_device_data)
            else: # Should not be reached if initial None check and UpdateFailed is effective
                _LOGGER.error("Device data is not a list after initial checks, this is unexpected. Proceeding with empty processed_devices.")
                processed_devices = []


            # Step 1.5: Fetch and merge camera-specific settings for camera devices.
            if self.coordinator.meraki_client:
                for device_idx, device_dict in enumerate(processed_devices):
                    if not isinstance(device_dict, dict):
                        _LOGGER.warning("Item at index %d in processed_devices is not a dictionary, skipping camera sense fetch: %s",
                                        device_idx, str(device_dict)[:100])
                        continue
                    serial = device_dict.get("serial")
                    product_type = device_dict.get("productType", "").lower()
                    model = device_dict.get("model", "").upper()

                    if serial and (product_type == "camera" or model.startswith("MV")):
                        try:
                            _LOGGER.debug(
                                "Fetching camera sense settings for camera %s", serial
                            )
                            sense_settings = await self.coordinator.meraki_client.get_camera_sense_settings(
                                serial=serial
                            )
                            if sense_settings:
                                # Merge relevant sense_settings into the device_dict.
                                # Entities will look for 'senseEnabled' and 'audioDetection' (which is a dict)
                                # directly in the device_info dictionary.
                                device_dict["senseEnabled"] = sense_settings.get("senseEnabled")
                                device_dict["audioDetection"] = sense_settings.get("audioDetection")
                                _LOGGER.debug(
                                    "Successfully merged camera sense settings for %s.", serial
                                )
                        except MerakiApiError as e: # Specific API error
                            _LOGGER.warning(
                                "Meraki API error fetching camera sense settings for %s: %s. Status: %s. "
                                "Entities for this camera's sense/audio status may be unavailable or show unknown.",
                                serial, e, e.status if hasattr(e, 'status') else 'N/A'
                            )
                        except aiohttp.ClientError as e: # Specific HTTP client error
                            _LOGGER.warning(
                                "HTTP client error fetching camera sense settings for %s: %s. "
                                "Entities for this camera's sense/audio status may be unavailable or show unknown.",
                                serial, e
                            )
                        except Exception as e: # Catch any other unexpected error for this specific camera
                            _LOGGER.exception( # Log with stack trace for unexpected issues
                                "Unexpected error fetching or merging camera sense settings for %s: %s. "
                                "Entities for this camera's sense/audio status may be unavailable or show unknown.",
                                serial, e
                            )
            else:
                _LOGGER.warning(
                    "Meraki API client not available on parent coordinator, "
                    "skipping fetch of camera-specific sense settings."
                )

            # Step 2: Sanitize and Process raw network data.
            sanitized_network_data: List[Dict[str, Any]] = []
            if isinstance(network_data, list): # network_data confirmed not None
                for i, network_item in enumerate(network_data):
                    if not isinstance(network_item, dict):
                        _LOGGER.warning("Item at index %d in network_data is not a dictionary, skipping: %s", i, str(network_item)[:100])
                        continue
                    if not network_item.get("id") or not isinstance(network_item.get("id"), str):
                        _LOGGER.warning("Network item at index %d missing or invalid 'id', skipping: %s", i, str(network_item)[:100])
                        continue
                    sanitized_network_data.append(network_item)
                processed_networks = self.data_processor.process_networks(sanitized_network_data)
            else: # Should not be reached
                _LOGGER.error("Network data is not a list after initial checks, this is unexpected. Proceeding with empty processed_networks.")
                processed_networks = []

            # Step 3: Sanitize and Process raw SSID data.
            sanitized_ssid_data: List[Dict[str, Any]] = []
            if isinstance(ssid_data, list): # ssid_data confirmed not None
                for i, ssid_item in enumerate(ssid_data):
                    if not isinstance(ssid_item, dict):
                        _LOGGER.warning("Item at index %d in ssid_data is not a dictionary, skipping: %s", i, str(ssid_item)[:100])
                        continue
                    if ssid_item.get("number") is None: # 'number' is critical for SSIDs
                        _LOGGER.warning("SSID item at index %d missing 'number', skipping: %s", i, str(ssid_item)[:100])
                        continue
                    # Ensure 'enabled' is boolean, default to False if missing or wrong type
                    enabled_flag = ssid_item.get("enabled")
                    if not isinstance(enabled_flag, bool):
                        _LOGGER.warning("SSID item at index %d 'enabled' flag is not bool (type: %s, value: %s). Defaulting to False.",
                                        i, type(enabled_flag).__name__, enabled_flag)
                        ssid_item["enabled"] = False
                    sanitized_ssid_data.append(ssid_item)
                processed_ssids = self.data_processor.process_ssids(sanitized_ssid_data)
            else: # Should not be reached
                _LOGGER.error("SSID data is not a list after initial checks, this is unexpected. Proceeding with empty processed_ssids.")
                processed_ssids = []

            # Note: Device tags are now part of `processed_devices` due to changes in
            # `MerakiApiDataFetcher` and `MerakiDataProcessor`.
            # The separate `device_tags` parameter is no longer needed here or
            # in `DataAggregator`.

            # Step 4: Aggregate all processed data using DataAggregator.
            # `DataAggregator.aggregate_data` now expects devices to contain their tags.
            aggregated_data: Dict[str, Any] = await self.data_aggregator.aggregate_data(
                processed_devices, # Now sanitized list of dicts, processed by data_processor
                processed_ssids,   # Now sanitized list of dicts, processed by data_processor
                processed_networks, # Now sanitized list of dicts, processed by data_processor
                sanitized_client_data, # Optional list of dicts, or None
                sanitized_network_client_counts, # Optional dict, or None
                clients_on_ssids=clients_on_ssids,
                clients_on_appliances=clients_on_appliances,
                clients_on_wireless=clients_on_wireless,
            )

            _LOGGER.debug(
                "Data aggregation successful. Aggregated data for %d devices, %d SSIDs, %d networks.", # Slightly rephrased
                len(aggregated_data.get("devices", [])), # Log count from aggregated_data for consistency
                len(aggregated_data.get("ssids", [])),
                len(aggregated_data.get("networks", [])),
            )
            return aggregated_data

        except UpdateFailed: # Re-raise UpdateFailed explicitly if caught
            raise
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception("Error during Meraki data aggregation: %s", e)
            raise UpdateFailed(f"Error aggregating Meraki data: {e}") from e
