"""Tests for the Data Fetch Manager graceful feature degradation."""

from unittest.mock import MagicMock, patch

import meraki
import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.core.errors import (
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
)


class MockAPIError(meraki.APIError):
    """Mock Meraki API Error for testing inheritance."""

    def __init__(self, status, message):
        """Initialize the mock error."""
        metadata = {"tags": ["test"], "operation": "test_op"}
        response = MagicMock()
        response.status_code = status
        response.reason = "Mock Reason"
        response.json.return_value = {"errors": [message]}
        super().__init__(metadata, response)
        # We need to ensure str(e) contains the message for our tests
        self.test_message = message

    def __str__(self):
        """Return the test message."""
        return str(self.test_message)


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client._disabled_features = set()
    client.has_dashboard = True
    return client


@pytest.fixture
def data_fetch_manager(mock_client):
    """Fixture for DataFetchManager."""
    return DataFetchManager(mock_client)


@pytest.mark.asyncio
async def test_async_gather_with_timeout_graceful_traffic_analysis(
    data_fetch_manager,
):
    """Test that specific Traffic Analysis error strings are intercepted gracefully."""

    async def traffic_error_coro():
        # Using the exact string from the requirement
        raise Exception("Traffic Analysis with Hostname Visibility must be enabled")

    tasks = {"test_traffic": traffic_error_coro()}

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER"
    ) as mock_logger:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import async_gather_with_timeout
        results = await async_gather_with_timeout(
            tasks, label="Test Graceful"
        )

    # Assert correct return type (SkipObject/Exception)
    assert isinstance(results["test_traffic"], MerakiTrafficAnalysisError)

    # Assert correct log message and level
    mock_logger.debug.assert_any_call(
        "Skipping %s: Configuration requirement not met in Meraki Dashboard.",
        "test_traffic",
    )
    # Ensure NO error was logged
    mock_logger.error.assert_not_called()


@pytest.mark.asyncio
async def test_async_gather_with_timeout_graceful_vlans(data_fetch_manager):
    """Test that specific VLANs error strings are intercepted gracefully."""

    async def vlan_error_coro():
        # Using the exact string from the requirement
        raise Exception("VLANs are not enabled for this network")

    tasks = {"test_vlans": vlan_error_coro()}

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER"
    ) as mock_logger:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import async_gather_with_timeout
        results = await async_gather_with_timeout(
            tasks, label="Test Graceful"
        )

    # Assert correct return type
    assert isinstance(results["test_vlans"], MerakiVlansDisabledError)

    # Assert correct log message and level
    mock_logger.debug.assert_any_call(
        "Skipping %s: Configuration requirement not met in Meraki Dashboard.",
        "test_vlans",
    )
    # Ensure NO error was logged
    mock_logger.error.assert_not_called()


@pytest.mark.asyncio
async def test_async_gather_with_timeout_handles_wrapped_meraki_errors(
    data_fetch_manager,
):
    """Test that it handles meraki.APIError when they contain the silent strings."""

    async def wrapped_error_coro():
        # Meraki SDK often returns errors in this format when converted to string
        raise MockAPIError(400, "VLANs are not enabled for this network")

    tasks = {"test_wrapped": wrapped_error_coro()}

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER"
    ) as mock_logger:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import async_gather_with_timeout
        results = await async_gather_with_timeout(
            tasks, label="Test Wrapped"
        )

    assert isinstance(results["test_wrapped"], MerakiVlansDisabledError)
    mock_logger.debug.assert_any_call(
        "Skipping %s: Configuration requirement not met in Meraki Dashboard.",
        "test_wrapped",
    )
    mock_logger.error.assert_not_called()


@pytest.mark.asyncio
async def test_async_gather_with_timeout_true_failures_still_log_error(
    data_fetch_manager,
):
    """Test that true failures (not silent) still log as ERROR."""

    async def true_failure_coro():
        raise Exception("Unexpected API Error 500")

    tasks = {"test_fail": true_failure_coro()}

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER"
    ) as mock_logger:
        # result will be None because _handle_fetch_exception returns None
        # and logs error
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import async_gather_with_timeout
        results = await async_gather_with_timeout(
            tasks, label="Test Failure"
        )

    assert results["test_fail"] is None
    mock_logger.error.assert_called_once()
