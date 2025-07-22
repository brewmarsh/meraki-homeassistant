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
from .data_aggregator import DataAggregator
from .data_processor import MerakiDataProcessor

if TYPE_CHECKING:
    # To avoid circular import issues, type hint the parent coordinator.
    from .coordinators.base_coordinator import (
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
        # relaxed_tag_match: bool, # Removed, no longer used
        coordinator: "MerakiDataUpdateCoordinator",  # Parent coordinator instance
    ) -> None:
        """Initialize the DataAggregationCoordinator.

        Args:
            hass: The Home Assistant instance.
            scan_interval: The interval for updating data, passed to the superclass.
                           This coordinator primarily updates when its `_async_update_data`
                           is explicitly called by the parent coordinator.
            coordinator: The main `MerakiDataUpdateCoordinator` instance, providing
                         access to the Meraki API client and other shared context.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data Aggregation Coordinator",
            update_interval=scan_interval,
        )
        # self.relaxed_tag_match removed
        self.coordinator: "MerakiDataUpdateCoordinator" = coordinator

        # Initialize helper classes for data processing and aggregation.
        # MerakiDataProcessor handles initial structuring of raw data.
        self.data_processor: MerakiDataProcessor = MerakiDataProcessor(
            # Pass parent for context if needed by processor.
            coordinator=self.coordinator
        )

        # Initialize SsidStatusCalculator first
        from .helpers.ssid_status_calculator import (
            SsidStatusCalculator,
        )
        self.ssid_status_calculator: SsidStatusCalculator = SsidStatusCalculator()

        # DataAggregator combines processed data and calculates SSID statuses.
        # It no longer takes data_processor as an argument.
        self.data_aggregator: DataAggregator = DataAggregator(
            # relaxed_tag_match removed from DataAggregator instantiation
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
    ) -> Dict[str, Any]:
        """Process and aggregate raw Meraki data, including camera-specific details."""
        from ..api.meraki_api import MerakiApiError
        import aiohttp

        try:
            if not (
                isinstance(device_data, list)
                and isinstance(ssid_data, list)
                and isinstance(network_data, list)
            ):
                _LOGGER.error(
                    "Essential data (devices, SSIDs, or networks) is not a list or is None. "
                    "Cannot proceed with data aggregation. Device type: %s, SSID type: %s, Network type: %s",
                    type(device_data).__name__,
                    type(ssid_data).__name__,
                    type(network_data).__name__,
                )
                raise UpdateFailed(
                    "Essential input data is not in the expected list format."
                )

            sanitized_client_data: Optional[List[Dict[str, Any]]] = None
            if client_data is not None:
                if isinstance(client_data, list):
                    sanitized_client_data = [
                        item for item in client_data if isinstance(item, dict)
                    ]
                    if len(sanitized_client_data) != len(client_data):
                        _LOGGER.warning(
                            "Some items in client_data were not dictionaries and were filtered out."
                        )
                else:
                    _LOGGER.warning(
                        "'client_data' provided but is not a list (type: %s). Treating as None.",
                        type(client_data).__name__,
                    )

            sanitized_network_client_counts: Optional[Dict[str, int]] = None
            if network_client_counts is not None:
                if isinstance(network_client_counts, dict):
                    sanitized_network_client_counts = network_client_counts
                else:
                    _LOGGER.warning(
                        "'network_client_counts' provided but is not a dict (type: %s). Treating as None.",
                        type(network_client_counts).__name__,
                    )

            processed_devices = await self.data_processor.process_devices(device_data)
            processed_networks = self.data_processor.process_networks(network_data)
            processed_ssids = self.data_processor.process_ssids(ssid_data)

            if self.coordinator.meraki_client:
                for device_idx, device_dict in enumerate(processed_devices):
                    if not isinstance(device_dict, dict):
                        _LOGGER.warning(
                            "Item at index %d in processed_devices is not a dictionary, skipping camera sense fetch.",
                            device_idx,
                        )
                        continue

                    serial = device_dict.get("serial")
                    product_type = str(device_dict.get("productType", "")).lower()
                    model = str(device_dict.get("model", "")).upper()

                    if serial and (
                        product_type == "camera" or model.startswith("MV")
                    ):
                        try:
                            sense_settings = (
                                await self.coordinator.meraki_client.get_camera_sense_settings(
                                    serial=serial
                                )
                            )

                            if sense_settings is not None and isinstance(
                                sense_settings, dict
                            ):
                                device_dict["senseEnabled"] = sense_settings.get(
                                    "senseEnabled"
                                )
                                device_dict["audioDetection"] = sense_settings.get(
                                    "audioDetection"
                                )
                            elif sense_settings is not None:
                                _LOGGER.warning(
                                    "Camera sense settings for %s were not a dictionary: %s",
                                    serial,
                                    str(sense_settings)[:100],
                                )
                        except MerakiApiError as e:
                            _LOGGER.warning(
                                "Meraki API error fetching camera sense settings for %s: %s. Status: %s. Details will be missing.",
                                serial,
                                e,
                                e.status if hasattr(e, "status") else "N/A",
                            )
                        except aiohttp.ClientError as e:
                            _LOGGER.warning(
                                "HTTP client error fetching camera sense settings for %s: %s. Details will be missing.",
                                serial,
                                e,
                            )
                        except Exception:
                            _LOGGER.exception(
                                "Unexpected error fetching or merging camera sense settings for %s. Details will be missing.",
                                serial,
                            )
            else:
                _LOGGER.warning(
                    "Meraki API client not available on parent coordinator, skipping camera sense settings."
                )

            aggregated_data: Dict[
                str, Any
            ] = await self.data_aggregator.aggregate_data(
                processed_devices=processed_devices,
                ssid_data=processed_ssids,
                network_data=processed_networks,
                client_data=sanitized_client_data,
                network_client_counts=sanitized_network_client_counts,
                clients_on_ssids=clients_on_ssids,
                clients_on_appliances=clients_on_appliances,
                clients_on_wireless=clients_on_wireless,
            )

            if not aggregated_data:
                _LOGGER.error(
                    "DataAggregator returned empty data. Aggregation failed."
                )
                raise UpdateFailed(
                    "Data aggregation by DataAggregator failed, returned empty."
                )

            return aggregated_data

        except UpdateFailed:
            raise
        except Exception as e:
            _LOGGER.exception(
                "Critical error during data aggregation coordination: %s", e
            )
            raise UpdateFailed(
                f"Overall data aggregation coordination failed: {e}"
            ) from e
