# test_api_data_fetcher.py
import pytest
import aiohttp
from unittest.mock import Mock
from meraki_ha.api_data_fetcher import MerakiApiDataFetcher
from meraki_ha.device_coordinator import MerakiDeviceCoordinator
from meraki_ha.network_coordinator import MerakiNetworkCoordinator
from meraki_ha.ssid_coordinator import MerakiSsidCoordinator


@pytest.fixture
def mock_coordinators():
    return (
        Mock(spec=MerakiDeviceCoordinator),
        Mock(spec=MerakiNetworkCoordinator),
        Mock(spec=MerakiSsidCoordinator),
    )


@pytest.fixture
def api_fetcher(mock_coordinators):
    device_coordinator, network_coordinator, ssid_coordinator = mock_coordinators
    return MerakiApiDataFetcher(
        "test_api_key", device_coordinator, network_coordinator, ssid_coordinator
    )


@pytest.mark.asyncio
async def test_fetch_data_success(aiohttp_client, api_fetcher):
    # Mock a successful API response
    mock_response = [{"key": "value"}]

    async def mock_handler(request):
        return aiohttp.web.json_response(mock_response)

    app = aiohttp.web.Application()
    app.router.add_get("/test_url", mock_handler)
    client = await aiohttp_client(app)

    result = await api_fetcher._fetch_data(f"{client.make_url('/test_url')}")
    assert result == mock_response
