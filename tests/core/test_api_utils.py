"""Test the API utility functions."""

from unittest.mock import MagicMock, patch

import pytest
from aiohttp import ClientError
from meraki.exceptions import APIError

from custom_components.meraki_ha.core.errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
)
from custom_components.meraki_ha.core.utils.api_utils import handle_meraki_errors


@pytest.fixture
def mock_api_client():
    client = MagicMock()
    client.mark_feature_disabled = MagicMock()
    return client


@pytest.fixture
def mock_instance(mock_api_client):
    instance = MagicMock()
    instance._api_client = mock_api_client
    return instance


@pytest.mark.asyncio
async def test_feature_disabled_traffic_analysis(mock_instance):
    """Test handling traffic analysis disabled error."""

    async def api_call(self, network_id: str) -> dict:
        metadata = {"tags": ["test"], "operation": "test_op"}
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = {
            "errors": ["Traffic Analysis with Hostname Visibility is not enabled"]
        }
        raise APIError(metadata, response)

    decorated = handle_meraki_errors(api_call)

    with patch(
        "custom_components.meraki_ha.core.utils.api.handlers._LOGGER"
    ) as mock_logger:
        result = await decorated(mock_instance, "N_123")

        assert result == {}
        mock_instance._api_client.mark_feature_disabled.assert_called_with(
            "api_call", "N_123"
        )
        mock_logger.debug.assert_called()


@pytest.mark.asyncio
async def test_feature_disabled_vlan(mock_instance):
    """Test handling VLAN disabled error."""

    async def api_call(self, network_id: str) -> list:
        metadata = {"tags": ["test"], "operation": "test_op"}
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = {
            "errors": ["VLANs are not enabled for this network"]
        }
        raise APIError(metadata, response)

    decorated = handle_meraki_errors(api_call)

    result = await decorated(mock_instance, "N_123")

    assert result == []
    mock_instance._api_client.mark_feature_disabled.assert_called_with(
        "api_call", "N_123"
    )


@pytest.mark.asyncio
async def test_auth_error():
    """Test handling authentication error."""

    async def api_call():
        metadata = {"tags": ["test"], "operation": "test_op"}
        response = MagicMock()
        response.status_code = 401
        response.json.return_value = {"errors": ["Invalid API key"]}
        raise APIError(metadata, response)

    decorated = handle_meraki_errors(api_call)

    with pytest.raises(MerakiAuthenticationError):
        await decorated()


@pytest.mark.asyncio
async def test_client_error():
    """Test handling aiohttp ClientError."""

    async def api_call():
        raise ClientError("Connection failed")

    decorated = handle_meraki_errors(api_call)

    with pytest.raises(MerakiConnectionError):
        await decorated()


@pytest.mark.asyncio
async def test_unexpected_error():
    """Test handling unexpected error."""

    async def api_call():
        raise ValueError("Unexpected")

    decorated = handle_meraki_errors(api_call)

    with pytest.raises(MerakiConnectionError) as excinfo:
        await decorated()
    assert "Unexpected error" in str(excinfo.value)
