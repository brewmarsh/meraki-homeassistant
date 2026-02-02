"""State managers for the Meraki HA integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)


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


class PendingUpdateManager:
    """Manages pending updates (cooldowns) for entities."""

    def __init__(self) -> None:
        """Initialize the PendingUpdateManager."""
        self._pending_updates: dict[str, datetime] = {}

    def register(self, unique_id: str | None, expiry_seconds: int = 150) -> None:
        """
        Register a pending update to ignore coordinator data.

        This prevents overwriting an optimistic state with stale data from the
        Meraki API, which can have a significant provisioning delay.

        Args:
        ----
            unique_id: The unique ID of the entity.
            expiry_seconds: The duration of the cooldown period.

        """
        if not unique_id:
            return

        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        self._pending_updates[unique_id] = expiry_time
        _LOGGER.debug(
            "Registered pending update for %s, ignoring coordinator updates until %s",
            unique_id,
            expiry_time,
        )

    def is_pending(self, unique_id: str | None) -> bool:
        """
        Check if an entity is in a pending (cooldown) state.

        Args:
        ----
            unique_id: The unique ID of the entity.

        Returns
        -------
            True if the entity is in a pending state, False otherwise.

        """
        if not unique_id:
            return False

        if unique_id not in self._pending_updates:
            return False

        now = datetime.now()
        expiry_time = self._pending_updates[unique_id]

        if now > expiry_time:
            # Cooldown has expired, remove it from the dictionary
            del self._pending_updates[unique_id]
            _LOGGER.debug("Pending update expired for %s", unique_id)
            return False

        # Cooldown is still active
        _LOGGER.debug("Update for %s is still pending (on cooldown)", unique_id)
        return True

    def cancel(self, unique_id: str | None) -> None:
        """
        Cancel a pending update for a device.

        Args:
        ----
            unique_id: The unique ID of the entity.

        """
        if unique_id and unique_id in self._pending_updates:
            del self._pending_updates[unique_id]
            _LOGGER.debug("Cancelled pending update for %s", unique_id)
