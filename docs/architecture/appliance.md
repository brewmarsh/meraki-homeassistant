### AI Agent Instructions

Your task is to refactor the `meraki_ha` integration to correctly retrieve and represent a device's on/off state and other controls for Meraki MX and GX appliances. The current methods are likely out of sync with the new architecture. Follow the updated design plan to ensure the refactored code is modular, testable, and robust.

1.  **Identify and use correct API endpoints**: The Meraki API has specific endpoints for controlling device state. You need to identify the correct API calls for toggling a device on/off, as well as checking its status.
2.  **Integrate with the `MerakiRepository`**: All API calls must go through the repository, which handles caching, rate-limiting, and state management. You must not call the API client directly.
3.  **Create a dedicated control service**: To avoid deep nesting and large files, create a new service specifically for handling device control logic. This service will contain methods like `async_reboot_device` or `async_set_power_state`.
4.  **Update `DeviceHandlers`**: The handlers for MX and GX devices must be refactored to use the new service for any actions (e.g., reboot). They will be responsible for creating the corresponding Home Assistant switch or button entities.
5.  **Write thorough tests**: For each new method and class, write unit tests that mock the repository and confirm the logic functions as expected. This will prevent regressions.

---

### Refactor Plan for MX/GX Device Controls

This plan focuses on making device controls stateless and declarative by centralizing the action logic in a dedicated service that the device handlers can call.

#### Phase 1: API and Repository Updates

1.  **Add `rebootDevice` to `MerakiApiClient`**:
    * Add a new asynchronous method, `async_reboot_device(serial)`, that calls the Meraki API's `rebootDevice` endpoint. This method will send the command to the Meraki cloud.

2.  **Add `reboot_device` to `MerakiRepository`**:
    * Create a new method, `async_reboot_device(serial)`, in the `MerakiRepository`.
    * This method will accept the device serial and call the `MerakiApiClient`. It will handle any errors, logging them but not raising exceptions that would crash the integration.
    * Because this is a write action, it should not be cached.

#### Phase 2: Create a Dedicated Control Service

1.  **Develop `DeviceControlService` (`meraki_ha/services/device_control_service.py`)**:
    * Create a new class, `DeviceControlService`, that is injected with the `MerakiRepository`.
    * This service will contain methods for device actions, such as:
        * `async_reboot(serial)`: A method that calls the repository's `async_reboot_device` method.
    * The separation of this logic into a service keeps the `DeviceHandlers` thin and focused on entity creation.

#### Phase 3: Update Device Handlers and Entities

1.  **Refactor `MXHandler` and `GXHandler`**:
    * Update the handlers to accept the `DeviceControlService` via **Dependency Injection**.
    * Within the handler's entity creation logic, create new `homeassistant.components.button.ButtonEntity` or `switch` entities as appropriate.
    * The `async_press` method of the button entity or the `async_turn_on`/`async_turn_off` methods of the switch entity must call the corresponding method on the **injected `DeviceControlService`**. For example, the button's `async_press` will call `await self._control_service.async_reboot(self.device_serial)`.

#### Phase 4: Testing and Cleanup

1.  **Write Focused Unit Tests**:
    * Test the `DeviceControlService` by injecting a mock `MerakiRepository` and asserting that the `async_reboot` method is called correctly.
    * Test the `MXHandler` and `GXHandler` to ensure they correctly create the button or switch entities. Use a mock control service and verify that the entity's action method calls the service as expected.
2.  **Remove Old Code**:
    * Delete any old, direct API calls for device control that may still exist in the `NetworkHub` or `DeviceHandlers`. Ensure all control actions are routed through the new service.
