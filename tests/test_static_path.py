"""Test static path registration."""

from unittest.mock import patch

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.integration import DOMAIN


async def test_static_path_registration(hass: HomeAssistant) -> None:
    """Test that static path registration uses the new async method."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"api_key": "fake_key", "organization_id": "fake_org"},
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)

    # Ensure frontend is in components to trigger the registration block
    hass.config.components.add("frontend")

    with (
        patch("custom_components.meraki_ha.create_api_client"),
        patch("custom_components.meraki_ha.coordinators.base.DataFetchManager"),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # Verify async_register_static_paths was called
    hass.http.async_register_static_paths.assert_called_once()
    args, _ = hass.http.async_register_static_paths.call_args
    configs = args[0]
    assert len(configs) == 1
    config = configs[0]
    assert isinstance(config, StaticPathConfig)
    assert config.url_path == "/meraki_ha_static"
    assert config.path.endswith("custom_components/meraki_ha/www")
    assert config.cache_headers is False
