"""Data Aggregator for the meraki_ha integration."""

import logging
from typing import Dict, List, Any

from .data_processor import MerakiDataProcessor
from .ssid_status_calculator import SsidStatusCalculator

_LOGGER = logging.getLogger(__name__)


class DataAggregator:
    """Aggregates data from Meraki coordinators."""

    def __init__(
        self,
        relaxed_tag_match: bool,
        data_processor: MerakiDataProcessor,
        ssid_status_calculator: SsidStatusCalculator,
    ) -> None:
        """Initialize the DataAggregator."""
        self.relaxed_tag_match = relaxed_tag_match
        self.data_processor = data_processor
        self.ssid_status_calculator = ssid_status_calculator

    async def aggregate_data(
        self,
        device_data: List[Dict[str, Any]],
        ssid_data: List[Dict[str, Any]],
        network_data: List[Dict[str, Any]],
        device_tags: Dict[str, List[str]],
    ) -> Dict[str, Any]:
        """Aggregates data from Meraki coordinators."""
        try:
            # Process and aggregate data
            aggregated_data = self.data_processor.process_data(
                device_data,
                ssid_data,
                network_data,
                device_tags,
                self.relaxed_tag_match,
            )
            return aggregated_data
        except Exception as e:
            _LOGGER.error(f"Error aggregating data: {e}")
            return {}  # Return empty dict on error
