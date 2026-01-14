### AI Agent Instructions

**Persona:** A pragmatic and experienced software architect, focused on creating scalable and maintainable solutions.

**Objective:** The primary goal is to refactor the Meraki SSID component to function as a "virtual" Home Assistant device, moving its entities from the main organization device to a new, dedicated device representation. This requires a strong understanding of object-oriented principles and the Home Assistant device model.

**Task Requirements:**

1.  **Device-centric Model:** The agent must conceptualize the Meraki SSID as a distinct Home Assistant device. This involves creating a new device representation for each SSID and associating all its related entities (e.g., sensors for client counts, switches for broadcasting) with this new virtual device.
2.  **Handler Creation:** A dedicated handler, `SSIDHandler`, must be created. This handler will be responsible for discovering the virtual SSID devices and their corresponding entities. It should follow the same pattern as other device handlers (e.g., `MRHandler`, `MVHandler`).
3.  **Dependency Injection:** The `SSIDHandler` must be designed to receive necessary services, such as a new `SSIDService` or the existing `DeviceControlService`, through its `__init__` method.
4.  **Entity Association:** The agent must ensure that all SSID-related entities, such as the `MerakiClientCountSensor` and `MerakiBroadcastSwitch`, are correctly associated with the new virtual SSID device, not the physical network device (e.g., the MR or MX).
5.  **Clean Code and Abstraction:** The code should be well-structured, with clear separation of concerns. The `SSIDHandler` should abstract the logic of creating SSID-specific entities and devices.
6.  **Comprehensive Testing:** The agent must update existing tests and create new ones to validate that the `SSIDHandler` correctly discovers and creates the virtual SSID device and all its entities. The tests should verify the correct device association for each entity.

---

### Implementation Plan

The refactoring will be executed in a phased, step-by-step approach to ensure a seamless migration to the new device model.

1.  **Phase 1: Handler and Service Creation**
    - **Create `SSIDHandler`:** Create a new file, `custom_components/meraki_ha/discovery/handlers/ssid.py`.
    - This handler will inherit from `BaseDeviceHandler`.
    - Its `__init__` method will accept `coordinator`, `config_entry`, and a new `SSIDService` (or `DeviceControlService`, if applicable) as arguments.
    - Implement the `discover_entities` method. This method will iterate through the list of SSIDs and for each one, create a **virtual Home Assistant device** using the `Device` class and then create the associated entities (sensors, switches), linking them to the new device using the `device_info` property.

2.  **Phase 2: Updating the Discovery Service**
    - **Modify `DeviceDiscoveryService`:** Open `custom_components/meraki_ha/discovery/service.py`.
    - Import the new `SSIDHandler`.
    - Update the `__init__` method to instantiate and store a new `SSIDService` if needed, and/or pass the existing `DeviceControlService` to the `SSIDHandler` when it is instantiated.
    - In the `discover_entities` method, add a new block of code to specifically call the `SSIDHandler` and collect its entities. Since SSIDs are not physical devices, this handler will need to be called separately from the loop that iterates through physical devices (`_devices`).

3.  **Phase 3: Entity Refactoring and Association**
    - **Update SSID Entities:** Open the existing files for the SSID-related entities (e.g., `custom_components/meraki_ha/sensor/ssid_client_count.py`, `custom_components/meraki_ha/switch/ssid_broadcast.py`).
    - Modify their `__init__` methods to accept a `device_info` object that represents the new virtual SSID device.
    - Update their `device_info` property to use the unique SSID identifier to link the entity to the virtual device instead of the main organization device.

4.  **Phase 4: Testing and Validation**
    - **Create `test_ssid_handler.py`:** Add a new unit test file to thoroughly test the `SSIDHandler`.
    - Test cases should include:
      - Verifying that the handler successfully creates a virtual device for each SSID.
      - Confirming that all SSID-related entities are correctly created and linked to their respective virtual devices.
      - Asserting that no entities are incorrectly associated with the main organization device.
    - Execute all tests and perform manual verification within a Home Assistant environment.
