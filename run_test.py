import asyncio
from unittest.mock import MagicMock, patch


async def main():
    hass = MagicMock()
    config_entry = MagicMock()
    config_entry.entry_id = "test"
    config_entry.unique_id = "test"
    config_entry.options = {}
    hass.data = {
        "meraki_ha": {
            "test": {
                "client": MagicMock(),
                "coordinators": {"meraki_ha_ssids_test": MagicMock()},
            }
        }
    }

    with patch("homeassistant.helpers.device_registry.async_get", MagicMock()):
        from custom_components.meraki_ha import async_setup_entry
        from custom_components.meraki_ha.sensor import (
            async_setup_entry as sensor_async_setup_entry,
        )

        # Mock the coordinator data
        coordinator = MagicMock()
        coordinator.data = {
            "devices": [
                {
                    "serial": "Q2KX-ACU9-ZAVN",
                    "name": "switch_garage_gs120_8p",
                    "productType": "switch",
                }
            ],
            "networks": [{"id": "L_3695766444210918206", "name": "Marshmallow Home"}],
            "ssids": [],
            "clients": [],
        }
        coordinator.org_id = "1254890"
        coordinator.org_name = "My Org"
        coordinator.formatted_org_display_name = "My Org"
        hass.data["meraki_ha"]["test"]["meraki_ha_coordinator"] = coordinator
        hass.data["meraki_ha"]["test"]["coordinators"] = {
            "meraki_ha_ssids_test": MagicMock(data={})
        }

        await async_setup_entry(hass, config_entry)
        await sensor_async_setup_entry(hass, config_entry, MagicMock())


if __name__ == "__main__":
    asyncio.run(main())
