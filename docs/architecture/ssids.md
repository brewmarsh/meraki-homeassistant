# Meraki SSID Architecture

## Implementation Plan

The refactoring will be executed in a phased, step-by-step approach to ensure a seamless migration to the new device model.

1. **Phase 1: Handler and Service Creation**

   - **Create `SSIDHandler`:** Create a new file, `custom_components/meraki_ha/discovery/handlers/ssid.py`.
   - This handler will inherit from `BaseDeviceHandler`.
   - Its `__init__` method will accept `coordinator`, `config_entry`, and a new `SSIDService` (or `DeviceControlService`, if applicable) as arguments.
   - Implement the `discover_entities` method. This method will iterate through the list of SSIDs and for each one, create a **virtual Home Assistant device** using the `Device` class and then create the associated entities (sensors, switches), linking them to the new device using the `device_info` property.

2. **Phase 2: Updating the Discovery Service**

   - **Modify `DeviceDiscoveryService`:** Open `custom_components/meraki_ha/discovery/service.py`.
   - Import the new `SSIDHandler`.
   - Update the `__init__` method to instantiate and store a new `SSIDService` if needed, and/or pass the existing `DeviceControlService` to the `SSIDHandler` when it is instantiated.
   - In the `discover_entities` method, add a new block of code to specifically call the `SSIDHandler` and collect its entities. Since SSIDs are not physical devices, this handler will need to be called separately from the loop that iterates through physical devices (`_devices`).

3. **Phase 3: Entity Refactoring and Association**

   - **Update SSID Entities:** Open the existing files for the SSID-related entities (e.g., `custom_components/meraki_ha/sensor/ssid_client_count.py`, `custom_components/meraki_ha/switch/ssid_broadcast.py`).
   - Modify their `__init__` methods to accept a `device_info` object that represents the new virtual SSID device.
   - Update their `device_info` property to use the unique SSID identifier to link the entity to the virtual device instead of the main organization device.

4. **Phase 4: Testing and Validation**
   - **Create `test_ssid_handler.py`:** Add a new unit test file to thoroughly test the `SSIDHandler`.
   - Test cases should include:
     - Verifying that the handler successfully creates a virtual device for each SSID.
     - Confirming that all SSID-related entities are correctly created and linked to their respective virtual devices.
     - Asserting that no entities are incorrectly associated with the main organization device.
   - Execute all tests and perform manual verification within a Home Assistant environment.
