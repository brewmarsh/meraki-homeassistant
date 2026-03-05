"""State managers for the Meraki HA integration."""

from __future__ import annotations

import logging
from collections import deque
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)


class PollingManager:
    """Manages adaptive polling intervals based on API success rates."""

    def __init__(self, default_interval: timedelta) -> None:
        """Initialize the PollingManager."""
        self.default_interval = default_interval
        self._current_interval = default_interval
        self._success_history: deque[bool] = deque(maxlen=5)
        self._consecutive_successes = 0

    @property
    def update_interval(self) -> timedelta:
        """Get the current update interval."""
        return self._current_interval

    @property
    def consecutive_successes(self) -> int:
        """Get the number of consecutive successful updates."""
        return self._consecutive_successes

    @property
    def success_history(self) -> list[bool]:
        """Get the success history."""
        return list(self._success_history)

    def record_success(self) -> bool:
        """
        Record a successful update.

        Returns
        -------
            True if the interval was reset to default, False otherwise.

        """
        self._consecutive_successes += 1
        self._success_history.append(True)

        if (
            self._consecutive_successes >= 3
            and self._current_interval != self.default_interval
        ):
            _LOGGER.info(
                "Meraki API recovered (3 consecutive successes). "
                "Resetting update interval to %s",
                self.default_interval,
            )
            self._current_interval = self.default_interval
            return True
        return False

    def record_failure(self, error: Exception) -> bool:
        """
        Record a failure.

        Returns
        -------
            True if the interval was increased, False otherwise.

        """
        self._consecutive_successes = 0
        self._success_history.append(False)

        error_str = str(error)
        if "429" in error_str:
            old_interval = self._current_interval
            # Double the interval, capped at 10 minutes (600 seconds)
            new_seconds = min(old_interval.total_seconds() * 2, 600)
            # Ensure it's at least 60 seconds if it was somehow lower
            new_seconds = max(new_seconds, 60)
            self._current_interval = timedelta(seconds=new_seconds)

            if self._current_interval != old_interval:
                _LOGGER.warning(
                    "Meraki API rate limit detected (429). Entering cooldown state. "
                    "Update interval increased from %s to %s",
                    old_interval,
                    self._current_interval,
                )
                return True
        return False

    def get_success_rate(self) -> float:
        """Get the success rate percentage of the last 5 updates."""
        if not self._success_history:
            return 100.0
        return (sum(self._success_history) / len(self._success_history)) * 100


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
