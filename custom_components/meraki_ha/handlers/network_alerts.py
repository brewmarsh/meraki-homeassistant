"""Handles network-related webhook alerts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.ALERTS


async def async_handle_network_alert(
    coordinator: MerakiDataCoordinator,
    alert_type: str,
    data: dict[str, Any],
) -> None:
    """Handle network settings alerts.

    When network settings change (SSIDs, VLANs, firewall rules), we trigger
    a refresh of the relevant data to update entities.

    Args:
    ----
        coordinator: The Meraki data coordinator.
        alert_type: The type of alert.
        data: The alert data from the webhook.

    """
    _LOGGER.info("Network alert received: %s", alert_type)

    network_id = data.get("networkId")
    if not network_id:
        _LOGGER.warning("Network alert missing 'networkId': %s", data)
        return

    # Determine what kind of refresh is needed based on alert type
    # Use debounced scheduling to avoid duplicate API calls from rapid webhooks
    if "SSID" in alert_type or "ssid" in alert_type.lower():
        # SSID settings changed - trigger SSID refresh
        _LOGGER.debug(
            "SSID settings changed for network %s, scheduling refresh", network_id
        )
        key = f"ssid:{network_id}"
        coordinator.schedule_debounced_refresh(
            key,
            coordinator._targeted_ssid_refresh(network_id),
        )
    elif "VLAN" in alert_type or "vlan" in alert_type.lower():
        # VLAN settings changed - trigger network refresh
        _LOGGER.debug(
            "VLAN settings changed for network %s, scheduling refresh", network_id
        )
        key = f"network:{network_id}"
        coordinator.schedule_debounced_refresh(
            key,
            coordinator._targeted_network_refresh(network_id),
        )
    elif "Firewall" in alert_type or "firewall" in alert_type.lower():
        # Firewall rules changed - trigger network refresh
        _LOGGER.debug(
            "Firewall rules changed for network %s, scheduling refresh", network_id
        )
        key = f"network:{network_id}"
        coordinator.schedule_debounced_refresh(
            key,
            coordinator._targeted_network_refresh(network_id),
        )
    else:
        # Generic settings change - trigger a network refresh
        _LOGGER.debug(
            "Network settings changed for network %s, scheduling refresh", network_id
        )
        key = f"network:{network_id}"
        coordinator.schedule_debounced_refresh(
            key,
            coordinator._targeted_network_refresh(network_id),
        )

    coordinator.async_update_listeners()
