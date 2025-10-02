import sys
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

async def main():
    """Patched environment to test setup."""
    hass = AsyncMock()
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"
    config_entry.data = {}  # Set data to avoid None errors
    config_entry.options = {}

    # Mock the coordinator and API client
    with patch('custom_components.meraki_ha.MerakiDataUpdateCoordinator') as MockCoordinator, \
         patch('custom_components.meraki_ha.async_setup_entry') as mock_async_setup_entry:

        # Instantiate the coordinator mock
        mock_coordinator_instance = MockCoordinator.return_value
        mock_coordinator_instance.async_config_entry_first_refresh = AsyncMock()

        # Mock hass.data
        hass.data = {
            'meraki_ha': {
                'test_entry': {
                    'coordinator': mock_coordinator_instance
                }
            }
        }

        from custom_components.meraki_ha import async_setup_entry

        # Call the setup function
        result = await async_setup_entry(hass, config_entry)

        # Verify that the setup function was called
        mock_async_setup_entry.assert_called_once()
        print("Test run successful: async_setup_entry was called.")

if __name__ == "__main__":
    asyncio.run(main())