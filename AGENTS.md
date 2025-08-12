# AI Agent Instructions

This file contains instructions for AI agents working with this codebase.

## Best Practices

- When writing tests, ensure that all mocks are as accurate as possible to the real APIs they are replacing. This will help to prevent bugs from being introduced into the codebase.
- Remove all debugging code, such as `_LOGGER.debug` statements, once feature development is complete.
- Follow the coding style of the project. This will help to ensure that the codebase is consistent and easy to read.
- Write clear and concise commit messages. This will help other developers to understand the changes that have been made.
- Update the documentation when making changes. This will help to ensure that the documentation is accurate and up-to-date.
- Run all tests before submitting changes. This will help to ensure that the changes have not introduced any new bugs.
- When using the Meraki API, please double-check against the Meraki API documentation at <https://developer.cisco.com/meraki/api-v1/>
- When using the Home Assistant API, double-check against the Home Assistant API documentation at <https://developers.home-assistant.io/docs/api/rest/>
- Prioritize local control, use established libraries, manage dependencies, and be mindful of performance impacts. Specifically, always prefer interacting with devices through established Python libraries rather than directly within the integration.
- **Centralized Device Creation:** To ensure device information is consistent, always use the `resolve_device_info` helper in `custom_components/meraki_ha/helpers/device_info_helpers.py` when creating a `DeviceInfo` object for an entity. Do not create `DeviceInfo` objects manually in entity classes.
- **Device vs. Entity Naming:** Use the `format_device_name` utility for the `name` field within `DeviceInfo`. For the name of an entity itself (`_attr_name`), use the `format_entity_name` helper.
- **Handling Disabled Features:** When an API call fails because a feature (like Traffic Analysis or VLANs) is disabled in the Meraki Dashboard, the corresponding sensor should reflect this. Instead of becoming `unknown`, its state should be set to `Disabled`, and an attribute should be added to explain the reason.
- **Testing New Entities:** When adding new sensors that are created dynamically by `setup_helpers.py`, the most effective tests call `async_setup_sensors` with mock coordinator data and then inspect the returned list of entities. This is preferable to testing the sensor class in isolation.
