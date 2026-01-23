"""Parsers for Meraki wireless data."""

from __future__ import annotations

from typing import Any

from ...types import MerakiNetwork


def parse_wireless_data(
    detail_data: dict[str, Any],
    networks: list[MerakiNetwork],
    previous_data: dict[str, Any],
    clients: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """
    Parse and process wireless data, primarily SSIDs.

    Args:
        detail_data: The raw detailed data from the API.
        networks: A list of Meraki networks.
        previous_data: The previous data from the coordinator.
        clients: A list of clients from the API.

    Returns
    -------
        A dictionary containing a list of processed SSIDs.
    """
    ssids: list[dict[str, Any]] = []
    client_counts: dict[tuple[str, str], int] = {}

    if clients:
        for client in clients:
            if "networkId" in client and "ssid" in client:
                key = (client["networkId"], client["ssid"])
                client_counts[key] = client_counts.get(key, 0) + 1

    for network in networks:
        network_id = network.id
        network_ssids_key = f"ssids_{network_id}"
        network_ssids = detail_data.get(network_ssids_key)

        if isinstance(network_ssids, list):
            for ssid in network_ssids:
                if (
                    isinstance(ssid, dict)
                    and "unconfigured ssid" not in ssid.get("name", "").lower()
                ):
                    ssid["networkId"] = network_id
                    ssid_name = ssid.get("name")
                    if ssid_name and network_id:
                        count_key = (network_id, str(ssid_name))
                        ssid["clientCount"] = client_counts.get(count_key, 0)
                    else:
                        ssid["clientCount"] = 0
                    ssids.append(ssid)
        elif previous_data and network_ssids_key in previous_data:
            # Restore previous data if API call fails
            ssids.extend(previous_data.get(network_ssids_key, []))

    return {"ssids": ssids}
