"""Tests for coordinator debouncing and deduplication functionality."""

from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import MagicMock


class TestWebhookDeduplication:
    """Test webhook event deduplication."""

    def test_is_duplicate_alert_new(self):
        """Test that new alerts are not marked as duplicates."""
        from custom_components.meraki_ha.meraki_data_coordinator import (
            MerakiDataCoordinator,
        )

        coordinator = MagicMock(spec=MerakiDataCoordinator)
        coordinator._processed_alert_ids = {}
        coordinator._alert_dedup_ttl_seconds = 300

        # Bind the actual method
        coordinator._is_duplicate_alert = (
            MerakiDataCoordinator._is_duplicate_alert.__get__(
                coordinator, MerakiDataCoordinator
            )
        )
        coordinator._cleanup_dedup_cache = (
            MerakiDataCoordinator._cleanup_dedup_cache.__get__(
                coordinator, MerakiDataCoordinator
            )
        )

        # First time should not be duplicate
        assert coordinator._is_duplicate_alert("alert-123") is False
        assert "alert-123" in coordinator._processed_alert_ids

    def test_is_duplicate_alert_existing(self):
        """Test that recently processed alerts are marked as duplicates."""
        from custom_components.meraki_ha.meraki_data_coordinator import (
            MerakiDataCoordinator,
        )

        coordinator = MagicMock(spec=MerakiDataCoordinator)
        coordinator._processed_alert_ids = {"alert-123": datetime.now()}
        coordinator._alert_dedup_ttl_seconds = 300

        coordinator._is_duplicate_alert = (
            MerakiDataCoordinator._is_duplicate_alert.__get__(
                coordinator, MerakiDataCoordinator
            )
        )
        coordinator._cleanup_dedup_cache = (
            MerakiDataCoordinator._cleanup_dedup_cache.__get__(
                coordinator, MerakiDataCoordinator
            )
        )

        # Second time should be duplicate
        assert coordinator._is_duplicate_alert("alert-123") is True

    def test_cleanup_dedup_cache_removes_old_entries(self):
        """Test that old entries are cleaned from the cache."""
        from custom_components.meraki_ha.meraki_data_coordinator import (
            MerakiDataCoordinator,
        )

        coordinator = MagicMock(spec=MerakiDataCoordinator)
        coordinator._alert_dedup_ttl_seconds = 300
        coordinator._processed_alert_ids = {
            "old-alert": datetime.now() - timedelta(seconds=400),
            "new-alert": datetime.now(),
        }

        coordinator._cleanup_dedup_cache = (
            MerakiDataCoordinator._cleanup_dedup_cache.__get__(
                coordinator, MerakiDataCoordinator
            )
        )

        coordinator._cleanup_dedup_cache()

        assert "old-alert" not in coordinator._processed_alert_ids
        assert "new-alert" in coordinator._processed_alert_ids


class TestMarkWebhookReceived:
    """Test mark_webhook_received functionality."""

    def test_mark_webhook_received_updates_timestamp(self):
        """Test that marking webhook received updates the timestamp."""
        from custom_components.meraki_ha.meraki_data_coordinator import (
            MerakiDataCoordinator,
        )

        coordinator = MagicMock(spec=MerakiDataCoordinator)
        coordinator._last_webhook_received = None
        coordinator._webhook_received_count = 0
        coordinator._processed_alert_ids = {}
        coordinator._alert_dedup_ttl_seconds = 300

        coordinator.mark_webhook_received = (
            MerakiDataCoordinator.mark_webhook_received.__get__(
                coordinator, MerakiDataCoordinator
            )
        )
        coordinator._is_duplicate_alert = (
            MerakiDataCoordinator._is_duplicate_alert.__get__(
                coordinator, MerakiDataCoordinator
            )
        )
        coordinator._cleanup_dedup_cache = (
            MerakiDataCoordinator._cleanup_dedup_cache.__get__(
                coordinator, MerakiDataCoordinator
            )
        )

        result = coordinator.mark_webhook_received("test_alert", "alert-123")

        assert result is True
        assert coordinator._last_webhook_received is not None
        assert coordinator._webhook_received_count == 1

    def test_mark_webhook_received_with_duplicate(self):
        """Test that duplicate alerts return False."""
        from custom_components.meraki_ha.meraki_data_coordinator import (
            MerakiDataCoordinator,
        )

        coordinator = MagicMock(spec=MerakiDataCoordinator)
        coordinator._last_webhook_received = None
        coordinator._webhook_received_count = 0
        coordinator._processed_alert_ids = {"alert-123": datetime.now()}
        coordinator._alert_dedup_ttl_seconds = 300

        coordinator.mark_webhook_received = (
            MerakiDataCoordinator.mark_webhook_received.__get__(
                coordinator, MerakiDataCoordinator
            )
        )
        coordinator._is_duplicate_alert = (
            MerakiDataCoordinator._is_duplicate_alert.__get__(
                coordinator, MerakiDataCoordinator
            )
        )
        coordinator._cleanup_dedup_cache = (
            MerakiDataCoordinator._cleanup_dedup_cache.__get__(
                coordinator, MerakiDataCoordinator
            )
        )

        result = coordinator.mark_webhook_received("test_alert", "alert-123")

        assert result is False
        assert coordinator._webhook_received_count == 0


class TaskCaptureMock(MagicMock):
    """Mock that captures and closes coroutines to avoid warnings."""

    def __init__(self, *args, **kwargs):
        """Initialize with task tracking."""
        super().__init__(*args, **kwargs)
        self._captured_tasks = []
        self._inner_coros = []

    def set_inner_coro(self, coro):
        """Track inner coroutine that will be inside wrapper."""
        self._inner_coros.append(coro)

    def __call__(self, coro):
        """Capture the coroutine and close it properly."""
        super().__call__(coro)
        if hasattr(coro, "close"):
            coro.close()
        self._captured_tasks.append(coro)
        # Also close any inner coroutines that were tracked
        for inner in self._inner_coros:
            if hasattr(inner, "close"):
                inner.close()
        self._inner_coros.clear()
        return None


class TestDebouncedRefresh:
    """Test debounced refresh scheduling."""

    def test_schedule_debounced_refresh_new(self):
        """Test scheduling a new debounced refresh."""
        from custom_components.meraki_ha.meraki_data_coordinator import (
            MerakiDataCoordinator,
        )

        coordinator = MagicMock(spec=MerakiDataCoordinator)
        coordinator._pending_refreshes = {}
        coordinator._refresh_debounce_seconds = 5
        coordinator.hass = MagicMock()
        # Use TaskCaptureMock to properly close coroutines
        task_mock = TaskCaptureMock()
        coordinator.hass.async_create_task = task_mock

        coordinator.schedule_debounced_refresh = (
            MerakiDataCoordinator.schedule_debounced_refresh.__get__(
                coordinator, MerakiDataCoordinator
            )
        )

        # Create a simple coroutine function and get its coroutine
        async def dummy_refresh_new():
            pass

        coro = dummy_refresh_new()
        # Track this coroutine so it can be closed when the wrapper is closed
        task_mock.set_inner_coro(coro)
        result = coordinator.schedule_debounced_refresh("device:serial", coro)

        assert result is True
        assert "device:serial" in coordinator._pending_refreshes
        task_mock.assert_called_once()

    def test_schedule_debounced_refresh_already_pending(self):
        """Test that pending refresh blocks new ones for same key."""
        from custom_components.meraki_ha.meraki_data_coordinator import (
            MerakiDataCoordinator,
        )

        coordinator = MagicMock(spec=MerakiDataCoordinator)
        # Set a pending refresh in the future
        coordinator._pending_refreshes = {
            "device:serial": datetime.now() + timedelta(seconds=10)
        }
        coordinator._refresh_debounce_seconds = 5
        coordinator.hass = MagicMock()
        # Use TaskCaptureMock to properly close coroutines
        task_mock = TaskCaptureMock()
        coordinator.hass.async_create_task = task_mock

        coordinator.schedule_debounced_refresh = (
            MerakiDataCoordinator.schedule_debounced_refresh.__get__(
                coordinator, MerakiDataCoordinator
            )
        )

        # Create a simple coroutine and close it properly since it won't be scheduled
        async def dummy_refresh():
            pass

        coro = dummy_refresh()
        result = coordinator.schedule_debounced_refresh("device:serial", coro)
        # Close the coroutine since it won't be scheduled
        coro.close()

        assert result is False
        # Should not create a new task
        task_mock.assert_not_called()
