"""Parsers for Meraki wireless data."""

from __future__ import annotations

from typing import Any, cast

from ...core.models.network import MerakiNetwork


def _update_ssids(processed_data: dict[str, Any], new_data: dict[str, Any]) -> None:
    """Update SSIDs in processed data, avoiding duplicates."""
    ssids = new_data.get("ssids", [])
    if not ssids:
        return

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


def _update_wireless_settings(
    processed_data: dict[str, Any], new_data: dict[str, Any]
) -> None:
    """Update wireless settings in processed data."""
    wireless_settings = new_data.get("wireless_settings", {})
    if not wireless_settings:
        return

    if "wireless_settings" not in processed_data:
        processed_data["wireless_settings"] = {}
    processed_data["wireless_settings"].update(wireless_settings)


def _update_rf_profiles(
    processed_data: dict[str, Any], new_data: dict[str, Any]
) -> None:
    """Update RF profiles in processed data."""
    rf_profiles = new_data.get("rf_profiles")
    if not isinstance(rf_profiles, dict):
        return

    if "rf_profiles" not in processed_data:
        processed_data["rf_profiles"] = {}
    processed_data["rf_profiles"].update(rf_profiles)


def update_processed_wireless_data(
    processed_data: dict[str, Any], new_data: dict[str, Any]
) -> None:
    """Update processed data with new wireless data, handling duplicates."""
    _update_ssids(processed_data, new_data)
    _update_wireless_settings(processed_data, new_data)
    _update_rf_profiles(processed_data, new_data)


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
    client_counts = _calculate_client_counts(clients)

    for network in networks:
        network_id = str(network.id) if network.id else ""
        if not network_id:
            continue

        processed_network_ssids = _process_network_ssids(
            network_id, detail_data, previous_data, client_counts
        )

        wireless_settings[network_id] = processed_network_ssids
        ssids.extend(processed_network_ssids)

        rf_profiles[network_id] = _process_network_rf_profiles(
            network_id, detail_data, previous_data
        )

    return {
        "ssids": ssids,
        "wireless_settings": wireless_settings,
        "rf_profiles": rf_profiles,
    }


def _is_online_wireless_client(client: dict[str, Any]) -> bool:
    """Check if client is online and has wireless info."""
    return bool(
        "networkId" in client
        and "ssid" in client
        and str(client.get("status", "")).lower() == "online"
    )


def _calculate_client_counts(
    clients: list[dict[str, Any]] | None,
) -> dict[tuple[str, str], int]:
    """Calculate online client counts per SSID."""
    client_counts: dict[tuple[str, str], int] = {}
    if not clients:
        return client_counts

    for client in clients:
        if _is_online_wireless_client(client):
            key = (str(client["networkId"]), str(client["ssid"]))
            client_counts[key] = client_counts.get(key, 0) + 1
    return client_counts


def _format_network_ssids(
    network_id: str,
    network_ssids_raw: list[Any],
    client_counts: dict[tuple[str, str], int],
) -> list[dict[str, Any]]:
    """Format and filter raw SSIDs for a network."""
    processed_ssids: list[dict[str, Any]] = []
    for ssid in network_ssids_raw:
        if not isinstance(ssid, dict):
            continue
        if "unconfigured ssid" in ssid.get("name", "").lower():
            continue

        ssid["networkId"] = network_id
        ssid_name = ssid.get("name")
        if ssid_name:
            count_key = (network_id, str(ssid_name))
            ssid["clientCount"] = client_counts.get(count_key, 0)
        else:
            ssid["clientCount"] = 0
        processed_ssids.append(ssid)
    return processed_ssids


def _fallback_network_ssids(
    network_id: str,
    network_ssids_key: str,
    previous_data: dict[str, Any],
) -> list[dict[str, Any]]:
    """Get fallback SSIDs from previous data."""
    if not previous_data:
        return []

    if "wireless_settings" in previous_data:
        return previous_data["wireless_settings"].get(network_id, [])
    if network_ssids_key in previous_data:
        return previous_data.get(network_ssids_key, [])

    return []


def _process_network_ssids(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    client_counts: dict[tuple[str, str], int],
) -> list[dict[str, Any]]:
    """Process SSIDs for a single network."""
    network_ssids_key = f"ssids_{network_id}"
    network_ssids_raw = detail_data.get(network_ssids_key)

    if isinstance(network_ssids_raw, list):
        return _format_network_ssids(network_id, network_ssids_raw, client_counts)

    return _fallback_network_ssids(network_id, network_ssids_key, previous_data)


def _fallback_network_rf_profiles(
    network_id: str,
    network_rf_profiles_key: str,
    previous_data: dict[str, Any],
) -> list[dict[str, Any]]:
    """Get fallback RF Profiles from previous data."""
    if not previous_data:
        return []

    if "rf_profiles" in previous_data:
        return previous_data["rf_profiles"].get(network_id, [])
    if network_rf_profiles_key in previous_data:
        return previous_data.get(network_rf_profiles_key, [])

    return []


def _process_network_rf_profiles(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
) -> list[dict[str, Any]]:
    """Process RF Profiles for a single network."""
    network_rf_profiles_key = f"rf_profiles_{network_id}"
    network_rf_profiles = detail_data.get(network_rf_profiles_key)

    if isinstance(network_rf_profiles, list):
        return network_rf_profiles

    return _fallback_network_rf_profiles(
        network_id, network_rf_profiles_key, previous_data
    )
