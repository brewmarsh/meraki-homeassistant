# Meraki MR/GR Wireless Architecture

## Integration Plan

The refactoring and **integration** will be executed in a phased, step-by-step approach to minimize disruption and ensure a smooth transition to the new architecture.

1. **Define a Base Handler Class:** Create a new file for a `BaseDeviceHandler` class. This class will provide a common blueprint for all device handlers and will contain shared properties and methods, such as the `coordinator` and `config_entry`.
2. **Refactor the `MRHandler` and `GRHandler`:**
   - Modify both `MRHandler` and `GRHandler` classes to inherit from the newly created `BaseDeviceHandler`.
   - Update the `__init__` method in both classes to accept an instance of the `DeviceControlService` as a dependency. The new `__init__` will call `super().__init__()` and store the `DeviceControlService` instance for later use.
   - Refactor the `discover_entities` methods within both handlers to use the injected `DeviceControlService` for any control-related tasks.
3. **Update the `DeviceDiscoveryService`:**
   - Add the `GRHandler` to the `HANDLER_MAPPING` dictionary in the `DeviceDiscoveryService` to ensure GR devices are handled correctly.
   - Modify the `discover_entities` method to pass the `DeviceControlService` instance to the constructors of both the `MRHandler` and `GRHandler` when they are instantiated.
4. **Modify the Platform Setup (`__init__.py`):**
   - Update the `async_setup_entry` function in the respective platform files (`binary_sensor/__init__.py`, `sensor/__init__.py`, etc.) to create an instance of the `DeviceControlService`.
   - Pass this new service instance to the `DeviceDiscoveryService` when it is initialized, so it can be distributed to the appropriate handlers.
5. **Validation and Finalization:**
   - Execute all unit tests to confirm the refactoring has not introduced any errors. Address any failures immediately.
   - Run the Home Assistant integration with the new code to verify that both **MR** and **GR** devices are discovered correctly and all entities function as expected.
   - Remove any legacy code and imports that are no longer needed, ensuring a clean and efficient final codebase.
