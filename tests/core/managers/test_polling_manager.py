"""Tests for the PollingManager."""

from datetime import timedelta

import pytest

from custom_components.meraki_ha.core.managers import PollingManager


@pytest.fixture
def polling_manager():
    """Fixture for PollingManager."""
    return PollingManager(default_interval=timedelta(seconds=60))


def test_initialization(polling_manager):
    """Test initialization values."""
    assert polling_manager.default_interval == timedelta(seconds=60)
    assert polling_manager.update_interval == timedelta(seconds=60)
    assert polling_manager.consecutive_successes == 0
    assert polling_manager.success_history == []
    assert polling_manager.get_success_rate() == 100.0


def test_record_success_basic(polling_manager):
    """Test basic success recording."""
    assert polling_manager.record_success() is False
    assert polling_manager.consecutive_successes == 1
    assert polling_manager.success_history == [True]
    assert polling_manager.get_success_rate() == 100.0


def test_record_failure_basic(polling_manager):
    """Test basic failure recording."""
    error = Exception("Some error")
    assert polling_manager.record_failure(error) is False
    assert polling_manager.consecutive_successes == 0
    assert polling_manager.success_history == [False]
    assert polling_manager.get_success_rate() == 0.0


def test_rate_limit_backoff(polling_manager):
    """Test backoff on 429 error."""
    error = Exception("meraki.exceptions.APIError: 429 Too Many Requests")

    # First 429
    assert polling_manager.record_failure(error) is True
    assert polling_manager.update_interval == timedelta(seconds=120)

    # Second 429
    assert polling_manager.record_failure(error) is True
    assert polling_manager.update_interval == timedelta(seconds=240)


def test_recovery(polling_manager):
    """Test recovery after 3 consecutive successes."""
    error = Exception("meraki.exceptions.APIError: 429 Too Many Requests")
    polling_manager.record_failure(error)  # 120s

    # 1st success
    assert polling_manager.record_success() is False
    assert polling_manager.update_interval == timedelta(seconds=120)

    # 2nd success
    assert polling_manager.record_success() is False

    # 3rd success - should reset
    assert polling_manager.record_success() is True
    assert polling_manager.update_interval == timedelta(seconds=60)


def test_success_history_limit(polling_manager):
    """Test that success history is limited to 5."""
    for _ in range(6):
        polling_manager.record_success()

    assert len(polling_manager.success_history) == 5
    assert all(polling_manager.success_history)


def test_success_rate_calculation(polling_manager):
    """Test success rate calculation."""
    polling_manager.record_success()  # [True]
    polling_manager.record_success()  # [True, True]
    polling_manager.record_failure(Exception("Error"))  # [True, True, False]
    polling_manager.record_success()  # [True, True, False, True]
    polling_manager.record_failure(Exception("Error"))  # [True, True, False, True, False]

    # 3 successes out of 5 = 60%
    assert polling_manager.get_success_rate() == 60.0
