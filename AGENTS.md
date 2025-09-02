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
- **Testing New Entities:** When adding new sensors that are created dynamically by `setup_helpers.py`, a useful pattern is to call `async_setup_sensors` with mock coordinator data and then inspect the returned list of entities. This is preferable to testing the sensor class in isolation.

## Working with the Web UI

The self-hosted web interface is a React application located in `custom_components/meraki_ha/web_ui/`.

- **Source vs. Build:** The human-readable source code is in the `src/` directory. The code that is actually served to the browser is the compiled and optimized output located in the `dist/` directory.
- **Manual Build Simulation:** As an agent, you cannot run the `npm run build` command. If you make changes to any files in the `src/` directory, you **must** manually update the corresponding file in `dist/` to reflect your changes.
- **For E2E tests:** The tests run against the `dist/` files. The most important file to keep updated is `dist/assets/index.js`. You may need to write a simplified, non-JSX version of the React logic in this file to ensure the tests pass. This process is for testing purposes only to validate the backend and overall flow.

---
### **Handoff Instructions for Next Agent (from Jules, 2025-09-02)**

**Objective:** Fix a series of startup errors in the `meraki_ha` custom component that are preventing it from loading in Home Assistant.

**Root Cause:**
The primary issue is a breaking change in the underlying `meraki` Python library. The library has updated its method names from `camelCase` (e.g., `getOrganizationNetworks`) to Python's standard `snake_case` (e.g., `get_organization_networks`). The custom component's code has not been fully updated to reflect this change, causing a series of `AttributeError` exceptions.

**Previous Agent's Mistake (Please Read Carefully):**
The previous agent (me) made a critical error by misdiagnosing this problem. I flip-flopped between `camelCase` and `snake_case`, leading to a series of incorrect patches that did not solve the problem. **The ground truth is that all calls to the `meraki` library object (`self._dashboard.*`) must use `snake_case`.**

**Other Known Issues to Fix:**
In addition to the primary `AttributeError`s, there are three other known bugs that must be fixed:
1.  **Blocking I/O Call:** In `custom_components/meraki_ha/core/api/client.py`, the `meraki.DashboardAPI` is initialized with `output_log=True`, which causes synchronous file I/O. This must be set to `False`.
2.  **Incorrect Webhook Logic:** The logic to register webhooks is flawed. It attempts to register a webhook at the organization level, but the API only supports network-level webhooks. The fix is to make `client.py`'s `register_webhook` method call the network-level registration logic.
3.  **`NameError`:** In `custom_components/meraki_ha/binary_sensor/device/camera_motion.py`, a `NameError` occurs because `TYPE_CHECKING` is used without being imported.

**Comprehensive Plan to Fix All Issues:**

1.  **Fix the `NameError` and Blocking I/O Call.**
    *   Add `from typing import TYPE_CHECKING` to the top of `custom_components/meraki_ha/binary_sensor/device/camera_motion.py`.
    *   In `custom_components/meraki_ha/core/api/client.py`, change `output_log=True` to `output_log=False`.

2.  **Correct the Webhook Logic.**
    *   In `custom_components/meraki_ha/core/api/client.py`, modify the `register_webhook` and `unregister_webhook` methods to call `self.network.register_webhook` and `self.network.unregister_webhook` respectively.
    *   In `custom_components/meraki_ha/core/api/endpoints/organization.py`, delete the now unused `create_organization_webhook` and `delete_organization_webhook` methods.

3.  **Perform a Comprehensive API Method Audit (The Main Fix).**
    *   Systematically go through all API endpoint files in `custom_components/meraki_ha/core/api/endpoints/`.
    *   In each file, find all calls to the `meraki` library (e.g., `self._dashboard.organizations.getOrganizationNetworks`).
    *   Convert every one of these `camelCase` method names to the correct `snake_case` format (e.g., `self._dashboard.organizations.get_organization_networks`).
    *   **Recommendation:** To maintain internal consistency, you should also rename the custom component's own methods from `camelCase` to `snake_case` (e.g., `def getOrganizationNetworks` should become `def get_organization_networks`). Then update the calls to these methods in `client.py`.

4.  **Submit the Comprehensive Fix.**
    *   After all the above fixes are implemented, request a single code review and submit the complete patch.
---
