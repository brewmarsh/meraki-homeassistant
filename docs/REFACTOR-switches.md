### AI Agent Instructions

Your task is to refactor the `meraki_ha` integration to properly represent Meraki MS/GS switch ports as Home Assistant entities. This includes creating a **visual status indicator** that changes based on whether a port is connected or disconnected. The refactor must be modular and testable, adhering to all previous instructions regarding file size and code structure.

1.  **Use the correct API endpoint:** The Meraki API has a dedicated endpoint to get the status for all ports of a switch: `/devices/{serial}/switch/ports/statuses`. You must use this endpoint to retrieve the port status, speed, duplex, and other relevant information.
2.  **Modularize port logic**: Create a dedicated service for handling switch port data. This will include methods for retrieving a specific port's status and for parsing the raw data.
3.  **Implement the visual indicator**: You must create a Home Assistant entity that automatically changes its icon to reflect the port's status. For a **connected** port, use a green icon, and for a **disconnected** port, use a red icon. You can use standard Home Assistant icons like `mdi:lan-connect` and `mdi:lan-disconnect` and leverage the `state_color` property to make the icon green or red based on the entity's state.

***

### Refactor Plan for Meraki MS/GS Switches

This plan will integrate switch port monitoring into the existing architecture by adding a new service layer and updating the `MSHandler` to dynamically create a binary sensor for each port.

#### Phase 1: API and Repository Updates

1.  **Add `getDeviceSwitchPortsStatuses` to `MerakiApiClient`**:
    * Add a new asynchronous method, `async_get_switch_port_statuses(serial)`, that calls the Meraki API's `/devices/{serial}/switch/ports/statuses` endpoint. This will return a list of all ports and their current status.

2.  **Add `get_switch_port_statuses` to `MerakiRepository`**:
    * Create a new method, `async_get_switch_port_statuses(serial)`, in the repository.
    * This method will accept the switch's serial number and call the API client. The repository will handle caching the results with a short TTL (e.g., 60 seconds) since port status can change frequently.

---

#### Phase 2: Create a Dedicated Switch Port Service

1.  **Develop `SwitchPortService` (`meraki_ha/services/switch_port_service.py`)**:
    * Create a new class, `SwitchPortService`, that is injected with the `MerakiRepository`.
    * This service will contain methods for handling switch port data, such as:
        * `async_get_port_status(serial, port_id)`: A method that queries the repository and returns the status (`Connected` or `Disconnected`) for a specific port.
        * `async_get_port_speed(serial, port_id)`: A similar method to get the port's current speed.

2.  **Update `MSHandler`**:
    * The `MSHandler` needs to be updated to accept the `SwitchPortService` via **Dependency Injection**.

---

#### Phase 3: Dynamic Entity Creation and Visual Indicators

1.  **Refactor `MSHandler`**:
    * During device discovery, after identifying a Meraki MS switch, the handler must iterate through all of its ports.
    * For each port, the handler will create a new **binary sensor** Home Assistant entity. A binary sensor is ideal for representing a simple "on/off" or "connected/disconnected" state.
    * The sensor's state will be set to `on` if the port status is 'Connected' and `off` if it's 'Disconnected'.
    * **Implement the visual indicator**: When creating the binary sensor entity, use the `device_class` property with `connectivity`. This tells Home Assistant to use a specific icon set for connected devices. For a more direct visual, you can also set the `icon` attribute and the `state_color` attribute to `True` on the entity. Home Assistant will then automatically color the icon based on the state. For example, the icon will be green when the state is `on` and gray when the state is `off`. 

---

#### Phase 4: Testing and Cleanup

1.  **Write New Unit Tests**:
    * Write tests for the `SwitchPortService` to ensure it correctly parses data from mock API responses.
    * Create tests for the `MSHandler` that verify it correctly creates a binary sensor for each port on a mock switch and sets the `device_class` and other properties correctly.
2.  **Remove Old Code**:
    * Remove any old or incorrect methods for retrieving switch port status. All status checks must now be routed through the new `SwitchPortService`.
