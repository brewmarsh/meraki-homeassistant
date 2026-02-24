"""Tests for API silencing and feature disabling."""

from unittest.mock import MagicMock

import pytest
from meraki.exceptions import APIError

from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.utils.api_utils import handle_meraki_errors


class MockResponse:
    """Mock response for APIError."""

    def __init__(self, status_code, reason, json_data):
        self.status_code = status_code
        self.reason = reason
        self._json_data = json_data

    def json(self):
        """Return the JSON data."""
        return self._json_data


class DummyEndpoint:
    """Dummy endpoint class for testing handle_meraki_errors."""

    def __init__(self, client):
        self._api_client = client

    @handle_meraki_errors
    async def get_traffic(self, network_id: str) -> list:
        """Mock traffic analysis call."""
        raise APIError(
            {"tags": ["test"], "operation": "test"},
            MockResponse(
                400,
                "Bad Request",
                {
                    "errors": [
                        "Traffic Analysis with Hostname Visibility must be enabled"
                    ]
                },
            ),
        )

    @handle_meraki_errors
    async def get_vlans(self, network_id: str) -> list:
        """Mock VLANs call."""
        raise APIError(
            {"tags": ["test"], "operation": "test"},
            MockResponse(
                400,
                "Bad Request",
                {"errors": ["VLANs are not enabled for this network"]},
            ),
        )


@pytest.mark.asyncio
async def test_api_silencing_traffic():
    """Test that traffic analysis 400 error is silenced and feature disabled."""
    client = MagicMock(spec=MerakiAPIClient)
    # Mock the behavior of mark_feature_disabled
    client._disabled_features = set()

    def mark_disabled(feature, network_id):
        client._disabled_features.add(f"{feature}_{network_id}")

    client.mark_feature_disabled.side_effect = mark_disabled

    endpoint = DummyEndpoint(client)

    result = await endpoint.get_traffic("N_123")

    assert result == []
    client.mark_feature_disabled.assert_called_once_with("traffic", "N_123")
    assert "traffic_N_123" in client._disabled_features


@pytest.mark.asyncio
async def test_api_silencing_vlans():
    """Test that VLANs 400 error is silenced and feature disabled."""
    client = MagicMock(spec=MerakiAPIClient)
    client._disabled_features = set()

    def mark_disabled(feature, network_id):
        client._disabled_features.add(f"{feature}_{network_id}")

    client.mark_feature_disabled.side_effect = mark_disabled

    endpoint = DummyEndpoint(client)

    result = await endpoint.get_vlans("N_123")

    assert result == []
    client.mark_feature_disabled.assert_called_once_with("vlans", "N_123")
    assert "vlans_N_123" in client._disabled_features
