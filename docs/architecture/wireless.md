### Agent Instructions
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======

>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
The agent's primary objective is to refactor the **Meraki MR** and **GR** components to align with the new, service-based architecture of the Home Assistant integration. The agent must adhere to the following instructions:

1.  **Objective:** The core task is to create a unified and scalable architecture for Meraki devices by refactoring the **MR** and **GR** components.
2.  **Service-Oriented Design:** The agent must exclusively use the **`DeviceControlService`** for all device management functions, such as rebooting or upgrading firmware. This service will be injected into the component handlers during discovery.
3.  **Handler Consolidation:** The agent should ensure the new **MR** and **GR** handlers inherit from a common base class, such as `BaseDeviceHandler`, to reduce redundant code and standardize the interface for device discovery.
4.  **Preservation of Functionality:** The refactor must not introduce any regressions. Existing functionalities, such as sensor discovery for MR devices, must continue to work as intended.
5.  **Code Quality:** The code produced must be clean, well-commented, and conform to the PEP 8 Python style guide. All new functions and classes should have clear docstrings.
6.  **Testing Protocol:** After the refactor, the agent must ensure that all existing unit tests for the **MR** and **GR** components pass. Additionally, new tests must be created to cover the new dependency injection pattern and the use of the `DeviceControlService`.

<<<<<<< HEAD
<<<<<<< HEAD
***

### Integration Plan
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
---

### Integration Plan

<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
The refactoring and **integration** will be executed in a phased, step-by-step approach to minimize disruption and ensure a smooth transition to the new architecture.

1.  **Define a Base Handler Class:** Create a new file for a `BaseDeviceHandler` class. This class will provide a common blueprint for all device handlers and will contain shared properties and methods, such as the `coordinator` and `config_entry`.
2.  **Refactor the `MRHandler` and `GRHandler`:**
<<<<<<< HEAD
<<<<<<< HEAD
    * Modify both `MRHandler` and `GRHandler` classes to inherit from the newly created `BaseDeviceHandler`.
    * Update the `__init__` method in both classes to accept an instance of the `DeviceControlService` as a dependency. The new `__init__` will call `super().__init__()` and store the `DeviceControlService` instance for later use.
    * Refactor the `discover_entities` methods within both handlers to use the injected `DeviceControlService` for any control-related tasks.
3.  **Update the `DeviceDiscoveryService`:**
    * Add the `GRHandler` to the `HANDLER_MAPPING` dictionary in the `DeviceDiscoveryService` to ensure GR devices are handled correctly.
    * Modify the `discover_entities` method to pass the `DeviceControlService` instance to the constructors of both the `MRHandler` and `GRHandler` when they are instantiated.
4.  **Modify the Platform Setup (`__init__.py`):**
    * Update the `async_setup_entry` function in the respective platform files (`binary_sensor/__init__.py`, `sensor/__init__.py`, etc.) to create an instance of the `DeviceControlService`.
    * Pass this new service instance to the `DeviceDiscoveryService` when it is initialized, so it can be distributed to the appropriate handlers.
5.  **Validation and Finalization:**
    * Execute all unit tests to confirm the refactoring has not introduced any errors. Address any failures immediately.
    * Run the Home Assistant integration with the new code to verify that both **MR** and **GR** devices are discovered correctly and all entities function as expected.
    * Remove any legacy code and imports that are no longer needed, ensuring a clean and efficient final codebase.
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    - Modify both `MRHandler` and `GRHandler` classes to inherit from the newly created `BaseDeviceHandler`.
    - Update the `__init__` method in both classes to accept an instance of the `DeviceControlService` as a dependency. The new `__init__` will call `super().__init__()` and store the `DeviceControlService` instance for later use.
    - Refactor the `discover_entities` methods within both handlers to use the injected `DeviceControlService` for any control-related tasks.
3.  **Update the `DeviceDiscoveryService`:**
    - Add the `GRHandler` to the `HANDLER_MAPPING` dictionary in the `DeviceDiscoveryService` to ensure GR devices are handled correctly.
    - Modify the `discover_entities` method to pass the `DeviceControlService` instance to the constructors of both the `MRHandler` and `GRHandler` when they are instantiated.
4.  **Modify the Platform Setup (`__init__.py`):**
    - Update the `async_setup_entry` function in the respective platform files (`binary_sensor/__init__.py`, `sensor/__init__.py`, etc.) to create an instance of the `DeviceControlService`.
    - Pass this new service instance to the `DeviceDiscoveryService` when it is initialized, so it can be distributed to the appropriate handlers.
5.  **Validation and Finalization:**
    - Execute all unit tests to confirm the refactoring has not introduced any errors. Address any failures immediately.
    - Run the Home Assistant integration with the new code to verify that both **MR** and **GR** devices are discovered correctly and all entities function as expected.
    - Remove any legacy code and imports that are no longer needed, ensuring a clean and efficient final codebase.
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
