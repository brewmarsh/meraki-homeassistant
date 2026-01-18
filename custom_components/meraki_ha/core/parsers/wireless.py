"""Parsers for Meraki wireless data."""
from __future__ import annotations

from typing import Any

from ...types import MerakiNetwork


def parse_wireless_data(
    detail_data: dict[str, Any],
    networks: list[MerakiNetwork],
    previous_data: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Parse and process wireless data, primarily SSIDs.

    Args:
        detail_data: The raw detailed data from the API.
        networks: A list of Meraki networks.
        previous_data: The previous data from the coordinator.

    Returns
    -------
        A list of processed SSIDs.
    """
    ssids: list[dict[str, Any]] = []
    for network in networks:
        if not isinstance(network, dict) or "id" not in network:
            continue

        network_id = network["id"]
        network_ssids_key = f"ssids_{network_id}"
        network_ssids = detail_data.get(network_ssids_key)

        if isinstance(network_ssids, list):
            for ssid in network_ssids:
                if (
                    isinstance(ssid, dict)
                    and "unconfigured ssid" not in ssid.get("name", "").lower()
                ):
                    ssid["networkId"] = network_id
                    ssids.append(ssid)
        elif previous_data and network_ssids_key in previous_data:
            ssids.extend(previous_data[network_ssids_key])

    return ssids
