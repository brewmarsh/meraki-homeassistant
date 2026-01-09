"""Test the button platform setup."""

from unittest.mock import MagicMock

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.button import async_setup_entry
from custom_components.meraki_ha.const import DOMAIN


async def test_async_setup_entry_adds_all_buttons(hass: HomeAssistant) -> None:
    """Test that all button entities are added at once."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    # Create mock entities
    # Mock isinstance to return True for ButtonEntity (simulated)
    # Since we can't easily mock isinstance(obj, Class), we will just use objects
    # that PASS the check in the real code.
    # In the real code:
    # button_entities = [e for e in discovered_entities if isinstance(e, ButtonEntity)]
    # So we need to pass actual ButtonEntity instances or mocks that inherit from it.

    class MockButton(ButtonEntity):
        pass

    entity1 = MockButton()
    entity2 = MockButton()
    entity3 = MockButton()

    entities = [entity1, entity2, entity3]

    hass.data[DOMAIN] = {
        "test_entry": {
            "entities": entities
        }
    }

    async_add_entities = MagicMock()

    await async_setup_entry(hass, config_entry, async_add_entities)

    # Verify async_add_entities was called once with all entities
    async_add_entities.assert_called_once_with(entities)


async def test_async_setup_entry_no_entities(hass: HomeAssistant) -> None:
    """Test setup when there are no button entities."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    hass.data[DOMAIN] = {
        "test_entry": {
            "entities": []
        }
    }

    async_add_entities = MagicMock()

    await async_setup_entry(hass, config_entry, async_add_entities)

    async_add_entities.assert_not_called()
