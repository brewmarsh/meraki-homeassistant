# AI Agent Instructions

This file contains instructions for AI agents working with this codebase.

## Best Practices

- When writing tests, ensure that all mocks are as accurate as possible to the real APIs they are replacing. This will help to prevent bugs from being introduced into the codebase.

## Testing

This project uses `pytest` to run tests. A helper script is provided to simplify the process.

### Setup

1.  **Install Dependencies:** All development and testing dependencies are listed in `requirements_dev.txt`. Install them with the following command:

    ```bash
    pip install -r requirements_dev.txt
    ```

### Running Tests

1.  **Use the Helper Script:** The easiest way to run the full test suite is to use the provided helper script:

    ```bash
    ./scripts/run-tests.sh
    ```

    This script will ensure all dependencies are installed and then run `pytest` with the correct configuration.

2.  **Running Tests Manually (Optional):** You can also run `pytest` directly. Make sure you have installed the dependencies first.

    ```bash
    pytest --cov=custom_components.meraki_ha tests/
    ```
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

## Architectural Pattern for Configuration Entities

**Author:** Jules, 2025-09-14

**Problem:** The Meraki Cloud API has a significant **provisioning delay**. When a configuration change is sent (e.g., disabling an SSID), the API acknowledges the change immediately with a `200 OK` response. However, the change can take several minutes to be fully provisioned on the backend. During this time, `GET` requests to the same API endpoint will return the *old* (stale) data.

**Consequences:** This delay caused a persistent bug where Home Assistant's UI would not correctly reflect the state of a switch. The flow was:
1. User toggles a switch.
2. The UI updates optimistically.
3. A `PUT` request is sent to Meraki.
4. The next scheduled data refresh in Home Assistant makes a `GET` request.
5. The `GET` request receives stale data from the Meraki API.
6. The Home Assistant coordinator updates the entity with this stale data, overwriting the correct optimistic state and making the UI revert to its previous, incorrect state.

**Solution: Optimistic UI with Cooldown**

To solve this, a specific architectural pattern **must** be used for all entities that modify configuration in Meraki (e.g., switches, text inputs, selects).

The required logic is as follows:

1.  **Optimistic State Update:** The entity's action method (e.g., `async_turn_on`, `async_set_value`) **must** immediately update its own state and tell Home Assistant to write this state to the UI.
    ```python
    # Example from a switch
    self._attr_is_on = True
    self.async_write_ha_state()
    ```

2.  **Fire-and-Forget API Call:** The method should then make the API call to Meraki without waiting for a response to be confirmed by a refresh.

3.  **Register a Cooldown:** After making the API call, the entity **must** register a "pending update" with the central `MerakiDataCoordinator`. This acts as a cooldown period.
    ```python
    # Example
    self.coordinator.register_pending_update(self.unique_id)
    ```
    The default cooldown is 150 seconds, which has been proven to be effective.

4.  **Ignore Coordinator Updates During Cooldown:** The entity's state update method (`_update_internal_state`), which is called by the coordinator, **must** check if it is in a cooldown period before processing new data. If it is, it should do nothing.
    ```python
    # Example
    def _update_internal_state(self) -> None:
        if self.coordinator.is_pending(self.unique_id):
            return # Ignore update
        # ... rest of the update logic
    ```

This pattern ensures a responsive UI that is resilient to the backend API's provisioning delay. **Do not attempt to "fix" this by forcing an immediate refresh after an action.** This will not work and will re-introduce the original bug.
