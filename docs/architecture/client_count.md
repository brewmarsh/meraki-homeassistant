\*\*AI Agent Instructions

The connected client counts are incorrect because the existing implementation likely uses a simple API endpoint that provides a snapshot of connected clients at a single point in time, which can quickly become outdated. It may also not correctly aggregate data from multiple devices or networks. The fix involves using a different set of Meraki API endpoints that are designed for monitoring client data.

Your task is to refactor how client counts are retrieved, ensuring the data is correct and properly aggregated for all relevant device types.

1.  **Develop `ClientCountService` (`meraki_ha/services/client_count_service.py`)**: - Create a new class that is injected with the `MerakiRepository`. - This service will have a primary method, `get_aggregated_counts(network_id)`. - This method will call the repository to get the latest client count data. - It will then **aggregate** this data. The aggregation logic will vary based on the desired sensor type: - **Network-wide count:** Simply sum up the total clients from the API response for the entire network. - **Per-device count (e.g., for an MR or MX):** The service will need to filter the API response by device serial number or use a separate API endpoint to get a device-specific client list. - **Per-VLAN/SSID count:** The service must use the correct API parameters to filter the client count data by SSID number or VLAN and return that specific count.

    > > > > > > > fix/camera-prefix-inference-8324397860843535137

1.  **Develop `ClientCountService` (`meraki_ha/services/client_count_service.py`)**:
    - Create a new class that is injected with the `MerakiRepository`.
    - This service will have a primary method, `get_aggregated_counts(network_id)`.
    - This method will call the repository to get the latest client count data.
    - It will then **aggregate** this data. The aggregation logic will vary based on the desired sensor type:
      - **Network-wide count:** Simply sum up the total clients from the API response for the entire network.
      - **Per-device count (e.g., for an MR or MX):** The service will need to filter the API response by device serial number or use a separate API endpoint to get a device-specific client list.
      - **Per-VLAN/SSID count:** The service must use the correct API parameters to filter the client count data by SSID number or VLAN and return that specific count.

<<<<<<< HEAD
#\*\*Phase 3: Integration and Entity Refinement

1. # **Update `NetworkHub`**:
1. **Update `NetworkHub`**:

   - **Inject the `ClientCountService`**: The `NetworkHub` should be updated to accept an instance of the `ClientCountService` in its constructor.
   - **Call the service in `_async_update_data`**: During the data update, the hub will call the `get_aggregated_counts` method from the injected service.

1. **Update `DeviceHandlers`**: - **Refactor count sensor creation**: Within the `MRHandler` and `MXHandler` classes, update the logic for creating the client count sensors. - The sensor's value should now come from the data returned by the `ClientCountService`, ensuring it is the correct, aggregated value.
   > > > > > > > fix/camera-prefix-inference-8324397860843535137

- **Inject the `ClientCountService`**: The `NetworkHub` should be updated to accept an instance of the `ClientCountService` in its constructor.
- **Call the service in `_async_update_data`**: During the data update, the hub will call the `get_aggregated_counts` method from the injected service.

<<<<<<< HEAD 2. **Update `DeviceHandlers`**:

- **Refactor count sensor creation**: Within the `MRHandler` and `MXHandler` classes, update the logic for creating the client count sensors.
- The sensor's value should now come from the data returned by the `ClientCountService`, ensuring it is the correct, aggregated value.

#\*\*Phase 4: Testing and Cleanup

1. **Create new unit tests**:

   - Write new tests for the `MerakiRepository` methods that fetch client counts, ensuring they correctly handle API responses.
   - Write unit tests for the `ClientCountService` to verify that it correctly aggregates data from various mock API responses.
   - Test the `NetworkHub` to ensure it correctly calls the `ClientCountService` and updates the entities.

2. **Remove old logic**:
   - Delete any old, incorrect logic for counting clients from the `NetworkHub` or `DeviceHandlers`.
   - # Ensure no part of the code relies on endpoints that don't provide accurate or real-time counts.
3. **Create new unit tests**:

   - Write new tests for the `MerakiRepository` methods that fetch client counts, ensuring they correctly handle API responses.
   - Write unit tests for the `ClientCountService` to verify that it correctly aggregates data from various mock API responses.
   - Test the `NetworkHub` to ensure it correctly calls the `ClientCountService` and updates the entities.

4. **Remove old logic**: - Delete any old, incorrect logic for counting clients from the `NetworkHub` or `DeviceHandlers`. - Ensure no part of the code relies on endpoints that don't provide accurate or real-time counts.
   > > > > > > > fix/camera-prefix-inference-8324397860843535137
