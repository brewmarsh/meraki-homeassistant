"""Tests for the Data Fetch Manager feature-specific error handling."""

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
        response.text = str({"errors": [message]})
        self.message = message
        super().__init__(metadata, response)

    def __str__(self):
        """Return the error message as a string."""
        return str(self.message)


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
async def test_async_gather_with_timeout_intercepts_traffic_analysis_error(
    data_fetch_manager,
):
    """Test that Traffic Analysis 400 errors are intercepted and logged at DEBUG."""

    async def traffic_error_coro():
        raise MockAPIError(
            400, "Traffic Analysis with Hostname Visibility must be enabled"
        )

    tasks = {"test_key": traffic_error_coro()}

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER"
    ) as mock_logger:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import (
            async_gather_with_timeout,
        )

        results = await async_gather_with_timeout(tasks, label="Test Intercept")

    # Assert
    assert isinstance(results["test_key"], MerakiTrafficAnalysisError)
    mock_logger.debug.assert_any_call(
        "Skipping %s: Configuration requirement not met in Meraki Dashboard.",
        "test_key",
    )
    # Ensure NO error was logged
    mock_logger.error.assert_not_called()


@pytest.mark.asyncio
async def test_async_gather_with_timeout_intercepts_vlans_error(data_fetch_manager):
    """Test that VLANs 400 errors are intercepted and logged at DEBUG."""

    async def vlan_error_coro():
        raise MockAPIError(400, "VLANs are not enabled for this network")

    tasks = {"test_key": vlan_error_coro()}

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER"
    ) as mock_logger:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import (
            async_gather_with_timeout,
        )

        results = await async_gather_with_timeout(tasks, label="Test Intercept")

    # Assert
    assert isinstance(results["test_key"], MerakiVlansDisabledError)
    mock_logger.debug.assert_any_call(
        "Skipping %s: Configuration requirement not met in Meraki Dashboard.",
        "test_key",
    )
    # Ensure NO error was logged
    mock_logger.error.assert_not_called()


@pytest.mark.asyncio
async def test_async_gather_with_timeout_fallback_to_error_for_other_400(
    data_fetch_manager,
):
    """Test that other 400 errors are still logged as ERROR."""

    async def other_error_coro():
        raise MockAPIError(400, "Some other bad request")

    tasks = {"test_key": other_error_coro()}

    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.batch_utils._LOGGER"
    ) as mock_logger:
        from custom_components.meraki_ha.core.coordinator_helpers.batch_utils import (
            async_gather_with_timeout,
        )

        results = await async_gather_with_timeout(tasks, label="Test Fallback")

    # Assert
    assert results["test_key"] is None
    mock_logger.error.assert_called_once()
    # Arguments: (format_string, key, label, exception)
    assert mock_logger.error.call_args[0][1] == "test_key"
