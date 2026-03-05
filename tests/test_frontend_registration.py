from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.frontend import (
    async_register_frontend,
    async_remove_frontend,
)


async def test_async_register_frontend(hass: HomeAssistant):
    """Test frontend registration."""
    entry = MagicMock()
    entry.domain = "meraki_ha"
    entry.title = "Meraki"
    entry.entry_id = "test_entry"

    # Mock async_get_loaded_integration
    integration = MagicMock()
    integration.version = "2.3.0-beta.120"

    with (
        patch(
            "custom_components.meraki_ha.frontend.async_get_loaded_integration",
            return_value=integration,
        ),
        patch(
            "homeassistant.components.frontend.async_register_built_in_panel"
        ) as mock_register,
    ):
        await async_register_frontend(hass, entry)

        mock_register.assert_called_once()
        args, kwargs = mock_register.call_args
        assert kwargs["frontend_url_path"] == "meraki"
        assert "v=2.3.0-beta.120" in kwargs["config"]["_panel_custom"]["module_url"]


async def test_async_remove_frontend(hass: HomeAssistant):
    """Test frontend removal."""
    with patch("homeassistant.components.frontend.async_remove_panel") as mock_remove:
        await async_remove_frontend(hass)
        mock_remove.assert_called_once_with(hass, "meraki")
