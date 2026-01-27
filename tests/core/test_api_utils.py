"""Test the API utility functions."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from meraki.exceptions import APIError  # type: ignore

from custom_components.meraki_ha.core.errors import MerakiConnectionError
from custom_components.meraki_ha.core.utils.api_utils import handle_meraki_errors


@pytest.mark.asyncio
async def test_handle_meraki_errors_rate_limit_retry():
    """Test that the handle_meraki_errors decorator retries on 429 errors."""
    mock_api_call = AsyncMock()
    metadata = {
        "tags": ["rate-limit"],
        "operation": "getDevice",
        "errors": ["Rate limit hit"],
    }
    response_mock = MagicMock()
    response_mock.status_code = 429
    response_mock.headers = {"Retry-After": "2"}

    api_error = APIError(metadata, response=response_mock)
    mock_api_call.side_effect = api_error

    decorated_func = handle_meraki_errors(mock_api_call)

    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        with pytest.raises(MerakiConnectionError):
            await decorated_func()

        assert mock_api_call.call_count == 3
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(2)
