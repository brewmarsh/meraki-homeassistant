"""Parsers for Meraki wireless data."""

from __future__ import annotations

from typing import Any

from ...core.models.network import MerakiNetwork


def parse_wireless_data(
    detail_data: dict[str, Any],
    networks: list[MerakiNetwork],
    previous_data: dict[str, Any],
    clients: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Parse and process wireless data, primarily SSIDs.

    Args:
        detail_data: The raw detailed data from the API.
        networks: A list of Meraki networks.
        previous_data: The previous data from the coordinator.
        clients: A list of clients from the API.

    Returns
    -------
        A dictionary containing processed SSIDs, wireless settings, and RF profiles.
    """
    ssids: list[dict[str, Any]] = []
    wireless_settings: dict[str, list[dict[str, Any]]] = {}
    rf_profiles: dict[str, list[dict[str, Any]]] = {}
    client_counts: dict[tuple[str, str], int] = {}

    # Calculate online client counts per SSID
    if clients:
        for client in clients:
            if (
                "networkId" in client
                and "ssid" in client
                and str(client.get("status", "")).lower() == "online"
            ):
                key = (str(client["networkId"]), str(client["ssid"]))
                client_counts[key] = client_counts.get(key, 0) + 1

    for network in networks:
        network_id = str(network.id) if network.id else ""
        if not network_id:
            continue

        # Process SSIDs
        network_ssids_key = f"ssids_{network_id}"
        network_ssids_raw = detail_data.get(network_ssids_key)

        processed_network_ssids: list[dict[str, Any]] = []

        if isinstance(network_ssids_raw, list):
            for ssid in network_ssids_raw:
                if (
                    isinstance(ssid, dict)
                    and "unconfigured ssid" not in ssid.get("name", "").lower()
                ):
                    ssid["networkId"] = network_id
                    ssid_name = ssid.get("name")
                    if ssid_name:
                        count_key = (network_id, str(ssid_name))
                        ssid["clientCount"] = client_counts.get(count_key, 0)
                    else:
                        ssid["clientCount"] = 0
                    processed_network_ssids.append(ssid)
        elif previous_data and "wireless_settings" in previous_data:
            processed_network_ssids = previous_data["wireless_settings"].get(
                network_id, []
            )
        elif previous_data and network_ssids_key in previous_data:
            # Fallback for older data structure
            processed_network_ssids = previous_data.get(network_ssids_key, [])

        wireless_settings[network_id] = processed_network_ssids
        ssids.extend(processed_network_ssids)

        # Process RF Profiles
        network_rf_profiles_key = f"rf_profiles_{network_id}"
        network_rf_profiles = detail_data.get(network_rf_profiles_key)
        if isinstance(network_rf_profiles, list):
            rf_profiles[network_id] = network_rf_profiles
        elif previous_data and "rf_profiles" in previous_data:
            rf_profiles[network_id] = previous_data["rf_profiles"].get(network_id, [])
        elif previous_data and network_rf_profiles_key in previous_data:
            rf_profiles[network_id] = previous_data.get(network_rf_profiles_key, [])

    return {
        "ssids": ssids,
        "wireless_settings": wireless_settings,
        "rf_profiles": rf_profiles,
    }
