"""Test static path registration."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.integration import DOMAIN


async def test_static_path_registration(
    hass: HomeAssistant, mock_http, mock_frontend
) -> None:
    """Test that static path registration uses the new async method."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"api_key": "fake_key", "organization_id": "fake_org"},
        entry_id="test_entry_id",
    )
    entry.add_to_hass(hass)

    # Ensure frontend is in components to trigger the registration block
    hass.config.components.add("frontend")

    # Action 1: Initialize the component
    await async_setup_component(hass, "http", {})

    mock_api_client = MagicMock()
    mock_api_client.async_setup = AsyncMock()
    mock_api_client.unregister_webhook = AsyncMock()
    mock_dfm = MagicMock()
    mock_dfm.async_initialize = AsyncMock()
    mock_dfm.get_all_data = AsyncMock(return_value={})
    mock_dfm.get_sensor_data = AsyncMock(return_value={})
    mock_dfm.get_device_data = AsyncMock(return_value={})

    # Action 1: Use patch.object to mock the method on the instance
    with (
        patch.object(hass.http, "async_register_static_paths") as mock_register,
        patch(
            "custom_components.meraki_ha.create_api_client",
            return_value=mock_api_client,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.base.DataFetchManager",
            return_value=mock_dfm,
        ),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        # Verify async_register_static_paths was called via the aliased mock
        mock_register.assert_called_once()
        args, _ = mock_register.call_args
        configs = args[0]
        assert len(configs) == 1
        config = configs[0]
        assert isinstance(config, StaticPathConfig)
        assert config.url_path == "/meraki_ha_static"
        assert config.path.endswith("custom_components/meraki_ha/www")
        assert config.cache_headers is False
