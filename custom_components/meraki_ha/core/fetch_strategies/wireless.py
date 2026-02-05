"""Wireless fetch strategy."""

from __future__ import annotations

from typing import Any, cast

from ...core.models.network import MerakiNetwork
from ..parsers.wireless import parse_wireless_data
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
        # Use the common wireless parser. Since this strategy method is called
        # per network, we pass the individual network's data.
        # We create a dummy MerakiNetwork object if we don't have the full list
        # but the parser only really needs the ID from it.
        network = MerakiNetwork(id=network_id, name="", product_types=["wireless"])

        wireless_data = parse_wireless_data(
            detail_data,
            [network],
            previous_data,
            clients=detail_data.get("clients"),
        )

        ssids = wireless_data.get("ssids", [])
        if ssids:
            if "ssids" not in processed_data:
                processed_data["ssids"] = []

            # SSID Duplicates Fix & Canonical Data Population
            existing_ids = {
                (s.get("networkId"), s.get("number"))
                for s in cast(list[dict[str, Any]], processed_data["ssids"])
            }

            for ssid in ssids:
                ssid_id = (ssid.get("networkId"), ssid.get("number"))
                if ssid_id not in existing_ids:
                    cast(list[dict[str, Any]], processed_data["ssids"]).append(ssid)
                    existing_ids.add(ssid_id)

        wireless_settings = wireless_data.get("wireless_settings", {})
        if wireless_settings:
            if "wireless_settings" not in processed_data:
                processed_data["wireless_settings"] = {}
            processed_data["wireless_settings"].update(wireless_settings)

        rf_profiles = wireless_data.get("rf_profiles")
        if isinstance(rf_profiles, dict):
            if "rf_profiles" not in processed_data:
                processed_data["rf_profiles"] = {}
            processed_data["rf_profiles"].update(rf_profiles)
