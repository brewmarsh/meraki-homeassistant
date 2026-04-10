"""Helper for processing appliance traffic and VLANs."""

from __future__ import annotations

import logging
from typing import Any

from ...core.errors import (
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlanError,
    MerakiVlansDisabledError,
)

_LOGGER = logging.getLogger(__name__)


class ApplianceTrafficHelper:
    """Helper class for processing network traffic and VLANs."""

    def __init__(self, disabled_features: set[str]) -> None:
        """Initialize the helper."""
        self._disabled_features = disabled_features

    def process_network_traffic(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        appliance_traffic: dict[str, Any],
    ) -> None:
        """Process traffic data for a network."""
        key = f"traffic_{network_id}"
        data = detail_data.get(key)

        if result := self._handle_traffic_error(network_id, key, data):
            appliance_traffic[network_id] = result
        elif isinstance(data, dict):
            appliance_traffic[network_id] = data
        elif previous_data and key in previous_data:
            appliance_traffic[network_id] = previous_data[key]

    def _handle_traffic_error(
        self, network_id: str, key: str, data: Any
    ) -> dict[str, str] | None:
        """Handle traffic analysis errors."""
        if isinstance(data, MerakiTrafficAnalysisError):
            self._disabled_features.add(key)
            _LOGGER.info(
                "Traffic analysis is not enabled for network %s.",
                network_id,
            )
            return {"error": "disabled", "reason": str(data)}

        if (
            isinstance(data, MerakiInformationalError)
            and "traffic analysis" in str(data).lower()
        ):
            self._disabled_features.add(key)
            return {"error": "disabled", "reason": str(data)}

        return None

    def process_network_vlans(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        vlan_by_network: dict[str, Any],
    ) -> None:
        """Process VLAN data for a network."""
        key = f"vlans_{network_id}"
        data = detail_data.get(key)

        if self._handle_vlan_error(key, data):
            vlan_by_network[network_id] = []
        elif isinstance(data, list):
            vlan_by_network[network_id] = data
        elif previous_data and key in previous_data:
            vlan_by_network[network_id] = previous_data[key]

    def _handle_vlan_error(self, key: str, data: Any) -> bool:
        """Handle VLAN errors and return True if feature should be disabled."""
        if isinstance(data, (MerakiVlanError, MerakiVlansDisabledError)):
            self._disabled_features.add(key)
            if isinstance(data, MerakiVlanError):
                _LOGGER.info(str(data))
            return True

        if isinstance(data, MerakiInformationalError):
            if "vlans are not enabled" in str(data).lower():
                self._disabled_features.add(key)
                return True

        return False
