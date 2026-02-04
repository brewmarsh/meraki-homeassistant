"""Wireless fetch strategy."""

from __future__ import annotations

from typing import Any, cast

from .base import BaseFetchStrategy


class WirelessFetchStrategy(BaseFetchStrategy):
    """Strategy for fetching wireless data."""

    def build_network_tasks(
        self,
        network_id: str,
        product_types: list[str],
        tasks: dict[str, Any],
    ) -> None:
        """Add wireless specific network tasks."""
        tasks.update(
            self.client.wireless.get_network_detail_tasks(network_id, product_types)
        )

    def process_network_data(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        processed_data: dict[str, Any],
    ) -> None:
        """Process wireless data (SSIDs and RF Profiles) for a network."""
        wireless_data = self.client.wireless.process_network_detail_data(
            detail_data, network_id, previous_data
        )

        ssids = wireless_data.get("ssids", [])
        if ssids:
            cast(list[dict[str, Any]], processed_data["ssids"]).extend(ssids)

        rf_profiles = wireless_data.get("rf_profiles")
        if isinstance(rf_profiles, dict):
            processed_data["rf_profiles"].update(rf_profiles)
