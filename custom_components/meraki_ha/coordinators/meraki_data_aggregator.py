"""Data aggregation for the Meraki Home Assistant integration.

This module provides the `MerakiDataAggregator` class, which is responsible
for processing and structuring the data fetched from the Meraki API.
"""

import logging
from typing import Any, Dict, List

from .helpers.utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiDataAggregator:
    """Aggregates and processes Meraki data."""

    def __init__(self, coordinator) -> None:
        """Initialize the data aggregator."""
        self.coordinator = coordinator

    def aggregate_data(
        self,
        devices: List[Dict[str, Any]],
        ssids: List[Dict[str, Any]],
        networks: List[Dict[str, Any]],
        clients_list: List[Dict[str, Any]],
        network_client_counts: Dict[str, int],
        clients_on_ssids: int,
        clients_on_appliances: int,
        clients_on_wireless: int,
    ) -> Dict[str, Any]:
        """Aggregate all data into a structured format."""
        device_name_format = self.coordinator.device_name_format
        for device in devices:
            device["formatted_name"] = format_device_name(
                device.get("name") or device.get("serial"),
                device.get("model", "Unknown"),
                device_name_format,
                is_org_device=False,
            )

        return {
            "devices": devices,
            "ssids": ssids,
            "networks": networks,
            "clients": clients_list,
            "network_client_counts": network_client_counts,
            "clients_on_ssids": clients_on_ssids,
            "clients_on_appliances": clients_on_appliances,
            "clients_on_wireless": clients_on_wireless,
        }
