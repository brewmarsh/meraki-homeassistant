import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from meraki.exceptions import APIError

from custom_components.meraki_ha.core.utils.api.decorator import handle_meraki_errors


@handle_meraki_errors
async def dummy_call():
    metadata = {"tags": ["test"], "operation": "test"}
    response = MagicMock()
    response.status_code = 429
    response.reason = "Rate Limit"
    response.json.return_value = {"errors": ["rate limit"]}
    raise APIError(metadata, response)

async def test():
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        try:
            await dummy_call()
        except Exception:
            pass
        print(f"Sleep calls: {mock_sleep.call_args_list}")

if __name__ == "__main__":
    asyncio.run(test())
