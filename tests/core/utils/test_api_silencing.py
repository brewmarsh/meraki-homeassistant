"""Tests for API silencing and feature disabling."""

from unittest.mock import MagicMock

import pytest
from meraki.exceptions import APIError

from custom_components.meraki_ha.core.api import (
    MerakiApiClientProtocol,
)
from custom_components.meraki_ha.core.utils.api_utils import handle_meraki_errors


class DummyEndpoint:
    """Dummy endpoint class for testing handle_meraki_errors."""

    def __init__(self, client):
        self._api_client = client

    @handle_meraki_errors
    async def get_traffic(self, network_id: str) -> list:
        """Mock traffic analysis call."""
        metadata = {"tags": ["test"], "operation": "getNetworkTraffic"}
        response = MagicMock()
        response.status_code = 400
        response.reason = "Bad Request"
        response.json.return_value = {
            "errors": ["Traffic Analysis with Hostname Visibility must be enabled"]
        }
        raise APIError(metadata, response)

    @handle_meraki_errors
    async def get_vlans(self, network_id: str) -> list:
        """Mock VLANs call."""
        metadata = {"tags": ["test"], "operation": "getNetworkApplianceVlans"}
        response = MagicMock()
        response.status_code = 400
        response.reason = "Bad Request"
        response.json.return_value = {
            "errors": ["VLANs are not enabled for this network"]
        }
        raise APIError(metadata, response)


@pytest.mark.asyncio
async def test_api_silencing_traffic():
    """Test that traffic analysis 400 error is silenced and feature disabled."""
    client = MagicMock(spec=MerakiApiClientProtocol)
    # Mock the behavior of mark_feature_disabled
    client._disabled_features = set()

    def mark_disabled(feature, network_id):
        client._disabled_features.add(f"{feature}_{network_id}")

    client.mark_feature_disabled.side_effect = mark_disabled

    endpoint = DummyEndpoint(client)

    result = await endpoint.get_traffic(network_id="N_123")

    assert result == []
    client.mark_feature_disabled.assert_called_once_with("get_traffic", "N_123")
    assert "get_traffic_N_123" in client._disabled_features


@pytest.mark.asyncio
async def test_api_silencing_vlans():
    """Test that VLANs 400 error is silenced and feature disabled."""
    client = MagicMock(spec=MerakiApiClientProtocol)
    client._disabled_features = set()

    def mark_disabled(feature, network_id):
        client._disabled_features.add(f"{feature}_{network_id}")

    client.mark_feature_disabled.side_effect = mark_disabled

    endpoint = DummyEndpoint(client)

    result = await endpoint.get_vlans(network_id="N_123")

    assert result == []
    client.mark_feature_disabled.assert_called_once_with("get_vlans", "N_123")
    assert "get_vlans_N_123" in client._disabled_features
