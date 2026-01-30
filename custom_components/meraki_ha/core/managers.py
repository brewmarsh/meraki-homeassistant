"""State managers for the Meraki HA integration."""

from __future__ import annotations

from datetime import datetime, timedelta


class AvailabilityTracker:
    """Tracks the availability check timestamps for network features."""

    def __init__(self) -> None:
        """Initialize the AvailabilityTracker."""
        self._check_timestamps: dict[str, dict[str, datetime]] = {}

    def is_check_due(
        self,
        network_id: str,
        feature: str,
        interval_hours: int = 24,
    ) -> bool:
        """
        Determine if an availability check is due for a network feature.

        Args:
        ----
            network_id: The ID of the network.
            feature: The feature to check (e.g., "vlan", "traffic").
            interval_hours: The interval in hours.

        Returns
        -------
            True if the check is due, False otherwise.

        """
        last_check = self._check_timestamps.get(network_id, {}).get(feature)
        if not last_check:
            return True
        return (datetime.now() - last_check) > timedelta(hours=interval_hours)

    def mark_check_done(self, network_id: str, feature: str) -> None:
        """
        Mark an availability check as done for the day.

        Args:
        ----
            network_id: The ID of the network.
            feature: The feature to mark (e.g., "vlan", "traffic").

        """
        if network_id not in self._check_timestamps:
            self._check_timestamps[network_id] = {}
        self._check_timestamps[network_id][feature] = datetime.now()
