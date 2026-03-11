"""Test migration for Meraki."""
from homeassistant.core import HomeAssistant
from custom_components.meraki_ha import async_migrate_entry
from pytest_homeassistant_custom_component.common import MockConfigEntry

async def test_migration_v1_to_v2(hass: HomeAssistant):
    """Test migrating a config entry from version 1 to 2."""
    entry = MockConfigEntry(
        domain="meraki_ha",
        version=1,
        data={
            "meraki_api_key": "test-key",
            "organization_id": "123456",
        },
    )
    entry.add_to_hass(hass)

    assert await async_migrate_entry(hass, entry)

    assert entry.version == 2
    assert entry.data["api_key"] == "test-key"
    assert "meraki_api_key" not in entry.data
