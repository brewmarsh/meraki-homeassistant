"""Test the API utility functions."""

from unittest.mock import AsyncMock, patch

import pytest

from custom_components.meraki_ha.core.utils.api_utils import handle_meraki_errors


@pytest.mark.asyncio
async def test_handle_meraki_errors_no_error():
    """Test that the handle_meraki_errors decorator doesn't break a normal call."""
    mock_api_call = AsyncMock(return_value="Success")
    decorated_func = handle_meraki_errors(mock_api_call)
    result = await decorated_func()
    assert result == "Success"
