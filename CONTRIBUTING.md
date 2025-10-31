# Contributing to Meraki Home Assistant

Thank you for your interest in contributing to this integration!

This document provides project-specific rules, architectural patterns, and guidelines that are essential for successful development. **Please read this file *after* reading the main `AGENTS.md` file** in this repository.

## 1. Core Architectural Principles

These are the most important patterns to understand before writing any code. Failure to follow them will re-introduce known, high-impact bugs.

### Pattern 1: The "Optimistic UI with Cooldown" (for Configuration Entities)

This is the **most critical pattern** in this codebase for all entities that modify configuration (e.g., `switch`, `select`, `text`).

* **Problem:** The Meraki Cloud API has a significant **provisioning delay**. When you send a `PUT` request (e.g., to disable an SSID), the API returns a `200 OK` immediately. However, the change can take several minutes to actually apply. During this time, any `GET` request will return the *old, stale data*.
* **Bug:** This delay causes the Home Assistant UI to "flicker." The user toggles a switch, the UI updates, the integration refreshes, the API returns the *old* state, and the UI toggle reverts to its original, incorrect position.
* **Solution:** We **must** use an optimistic state with a timed cooldown.

The required logic is as follows:

1.  **Optimistic State Update:** The entity's action method (e.g., `async_turn_on`) **must** immediately update its own state and tell Home Assistant to write this state to the UI.
    ```python
    # Example from a switch
    self._attr_is_on = True
    self.async_write_ha_state()
    ```

2.  **Fire-and-Forget API Call:** The method should then make the API call to Meraki without waiting for a response to be confirmed by a refresh.

3.  **Register a Cooldown:** After making the API call, the entity **must** register a "pending update" with the central `MerakiDataCoordinator`. This acts as a cooldown period (default 150 seconds).
    ```python
    # Example
    self.coordinator.register_pending_update(self.unique_id)
    ```

4.  **Ignore Coordinator Updates:** The entity's state update method (`_update_internal_state`) **must** check if it is in a cooldown period before processing new data. If it is, it must `return` and do nothing.
    ```python
    # Example
    def _update_internal_state(self) -> None:
        if self.coordinator.is_pending(self.unique_id):
            return  # Ignore update, optimistic state is in control
        
        # ... rest of the update logic ...
    ```

**Do not attempt to "fix" this by forcing an immediate refresh after an action.** This will not work and will re-introduce the original bug.

### Pattern 2: API Client Conventions (`meraki` Library)

* **Historical Context:** The underlying `meraki` Python library had a breaking change, moving all its methods from `camelCase` (e.g., `getOrganizationNetworks`) to Python's standard `snake_case` (e.g., `get_organization_networks`).
* **Rule:** All calls to the `meraki` library object (e.g., `self._dashboard.*`) **must** use `snake_case` methods.
* **Internal Convention:** To maintain consistency, this project's *own* client wrapper methods (in `custom_components/meraki_ha/core/api/endpoints/`) also use `snake_case`. Please follow this pattern.

---

## 2. Home Assistant Integration Best Practices

Follow these rules to ensure consistency with Home Assistant's design patterns and this integration's helpers.

* **Device & Entity Helpers:**
    * **Device Info:** **Do not** create `DeviceInfo` objects manually. Always use the `resolve_device_info` helper in `custom_components/meraki_ha/helpers/device_info_helpers.py`.
    * **Device Name:** Use the `format_device_name` utility for the `name` field within `DeviceInfo`.
    * **Entity Name:** Use the `format_entity_name` helper for the entity's own name (`_attr_name`).

* **Handling Disabled Features:**
    * When an API call fails because a feature (like Traffic Analysis or VLANs) is disabled in the Meraki Dashboard, the corresponding entity should not become `unknown`.
    * Instead, its state **must** be set to `Disabled`, and an attribute should be added to explain the reason.

* **Testing New Entities:**
    * A useful pattern for testing new, dynamically created sensors is to call `async_setup_sensors` (or the equivalent setup helper) with mock coordinator data.
    * You can then inspect the list of entities returned by the helper to validate their properties. This is often more effective than testing the sensor class in isolation.

* **Constants:**
    * All constants (domain names, default values, keys) **must** be defined in `custom_components/meraki_ha/const.py`. Do not use magic strings in entity or coordinator code.

* **Configuration Validation:**
    * All configuration data (from `configuration.yaml` or UI config flows) **must** be validated using `voluptuous` schemas.

* **API Documentation:**
    * When working with a Meraki endpoint, double-check your implementation against the [Meraki API documentation](https://developer.cisco.com/meraki/api-v1/).
    * When interacting with Home Assistant, double-check against the [Home Assistant API documentation](https://developers.home-assistant.io/docs/api/rest/).

---

## 3. Working with the Web UI (React)

The self-hosted web interface is a React application located in `custom_components/meraki_ha/web_ui/`.

* **Source vs. Build:**
    * The human-readable source code is in the `src/` directory.
    * The code actually served to the browser is the compiled/optimized output in the
