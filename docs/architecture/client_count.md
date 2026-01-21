<<<<<<< HEAD
### AI Agent Instructions
=======
\*\*AI Agent Instructions
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

The connected client counts are incorrect because the existing implementation likely uses a simple API endpoint that provides a snapshot of connected clients at a single point in time, which can quickly become outdated. It may also not correctly aggregate data from multiple devices or networks. The fix involves using a different set of Meraki API endpoints that are designed for monitoring client data.

Your task is to refactor how client counts are retrieved, ensuring the data is correct and properly aggregated for all relevant device types.

<<<<<<< HEAD
1.  **Strictly use a more reliable API endpoint**: The API provides specific endpoints for retrieving client count history and details. The most reliable way to get an accurate count is to use the `getNetworkWirelessClientCountHistory` endpoint or similar ones that provide aggregated data. Avoid using endpoints that simply list clients, as they often don't provide a real-time total.
2.  **Modularize the count logic**: Create a dedicated service or module specifically for handling client count logic. This will prevent the `NetworkHub` from becoming too complex.
3.  **Aggregate data correctly**: The logic must correctly handle data from different sources (MX, MR, VLANs, SSIDs) and sum them up to get a correct total.

---

### Implementation Plan

This plan builds on the existing modular architecture, adding a new service layer dedicated to client count collection and aggregation.

#### Phase 1: API Client and Repository Updates

1.  **Add new endpoints to `MerakiApiClient`**:
    - Add a new method, `get_network_wireless_client_count_history(network_id, **kwargs)`, that calls the Meraki API's `/networks/{networkId}/wireless/clientCountHistory` endpoint. This endpoint can filter by device serial, SSID, or other parameters.
    - Add other relevant endpoints for getting client lists or stats from specific devices (e.g., `get_device_clients` for individual devices) if needed for more granular data.

2.  **Add new methods to `MerakiRepository`**:
    - Create a `get_client_counts_for_network(network_id)` method in the repository.
    - This method will use the newly added API client method to fetch client count data. It should handle the API call, parse the response, and cache the result according to a short-term TTL (e.g., 5-10 minutes) since client counts are dynamic.
    - Add a similar method for getting device-specific client counts, if required.

#### Phase 2: Create a Client Count Service

1.  **Develop `ClientCountService` (`meraki_ha/services/client_count_service.py`)**:
    - Create a new class that is injected with the `MerakiRepository`.
    - This service will have a primary method, `get_aggregated_counts(network_id)`.
    - This method will call the repository to get the latest client count data.
    - It will then **aggregate** this data. The aggregation logic will vary based on the desired sensor type:
      - **Network-wide count:** Simply sum up the total clients from the API response for the entire network.
      - **Per-device count (e.g., for an MR or MX):** The service will need to filter the API response by device serial number or use a separate API endpoint to get a device-specific client list.
      - **Per-VLAN/SSID count:** The service must use the correct API parameters to filter the client count data by SSID number or VLAN and return that specific count.

#### Phase 3: Integration and Entity Refinement

1.  **Update `NetworkHub`**:
    - **Inject the `ClientCountService`**: The `NetworkHub` should be updated to accept an instance of the `ClientCountService` in its constructor.
    - **Call the service in `_async_update_data`**: During the data update, the hub will call the `get_aggregated_counts` method from the injected service.

2.  **Update `DeviceHandlers`**:
    - **Refactor count sensor creation**: Within the `MRHandler` and `MXHandler` classes, update the logic for creating the client count sensors.
    - The sensor's value should now come from the data returned by the `ClientCountService`, ensuring it is the correct, aggregated value.

#### Phase 4: Testing and Cleanup

1.  **Create new unit tests**:
    - Write new tests for the `MerakiRepository` methods that fetch client counts, ensuring they correctly handle API responses.
    - Write unit tests for the `ClientCountService` to verify that it correctly aggregates data from various mock API responses.
    - Test the `NetworkHub` to ensure it correctly calls the `ClientCountService` and updates the entities.

2.  **Remove old logic**:
    - Delete any old, incorrect logic for counting clients from the `NetworkHub` or `DeviceHandlers`.
    - Ensure no part of the code relies on endpoints that don't provide accurate or real-time counts.
=======
1. **Strictly use a more reliable API endpoint**: The API provides specific endpoints for retrieving client count history and details. The most reliable way to get an accurate count is to use the `getNetworkWirelessClientCountHistory` endpoint or similar ones that provide aggregated data. Avoid using endpoints that simply list clients, as they often don't provide a real-time total.
2. **Modularize the count logic**: Create a dedicated service or module specifically for handling client count logic. This will prevent the `NetworkHub` from becoming too complex.
3. **Aggregate data correctly**: The logic must correctly handle data from different sources (MX, MR, VLANs, SSIDs) and sum them up to get a correct total.

---

\*\*Implementation Plan

This plan builds on the existing modular architecture, adding a new service layer dedicated to client count collection and aggregation.

#\*\*Phase 1: API Client and Repository Updates

1. **Add new endpoints to `MerakiApiClient`**:

   - Add a new method, `get_network_wireless_client_count_history(network_id, **kwargs)`, that calls the Meraki API's `/networks/{networkId}/wireless/clientCountHistory` endpoint. This endpoint can filter by device serial, SSID, or other parameters.
   - Add other relevant endpoints for getting client lists or stats from specific devices (e.g., `get_device_clients` for individual devices) if needed for more granular data.

2. **Add new methods to `MerakiRepository`**:
   - Create a `get_client_counts_for_network(network_id)` method in the repository.
   - This method will use the newly added API client method to fetch client count data. It should handle the API call, parse the response, and cache the result according to a short-term TTL (e.g., 5-10 minutes) since client counts are dynamic.
   - Add a similar method for getting device-specific client counts, if required.

#\*\*Phase 2: Create a Client Count Service

1. **Develop `ClientCountService` (`meraki_ha/services/client_count_service.py`)**:
   - Create a new class that is injected with the `MerakiRepository`.
   - This service will have a primary method, `get_aggregated_counts(network_id)`.
   - This method will call the repository to get the latest client count data.
   - It will then **aggregate** this data. The aggregation logic will vary based on the desired sensor type:
     - **Network-wide count:** Simply sum up the total clients from the API response for the entire network.
     - **Per-device count (e.g., for an MR or MX):** The service will need to filter the API response by device serial number or use a separate API endpoint to get a device-specific client list.
     - **Per-VLAN/SSID count:** The service must use the correct API parameters to filter the client count data by SSID number or VLAN and return that specific count.

#\*\*Phase 3: Integration and Entity Refinement

1. **Update `NetworkHub`**:

   - **Inject the `ClientCountService`**: The `NetworkHub` should be updated to accept an instance of the `ClientCountService` in its constructor.
   - **Call the service in `_async_update_data`**: During the data update, the hub will call the `get_aggregated_counts` method from the injected service.

2. **Update `DeviceHandlers`**:
   - **Refactor count sensor creation**: Within the `MRHandler` and `MXHandler` classes, update the logic for creating the client count sensors.
   - The sensor's value should now come from the data returned by the `ClientCountService`, ensuring it is the correct, aggregated value.

#\*\*Phase 4: Testing and Cleanup

1. **Create new unit tests**:

   - Write new tests for the `MerakiRepository` methods that fetch client counts, ensuring they correctly handle API responses.
   - Write unit tests for the `ClientCountService` to verify that it correctly aggregates data from various mock API responses.
   - Test the `NetworkHub` to ensure it correctly calls the `ClientCountService` and updates the entities.

2. **Remove old logic**:
   - Delete any old, incorrect logic for counting clients from the `NetworkHub` or `DeviceHandlers`.
   - Ensure no part of the code relies on endpoints that don't provide accurate or real-time counts.
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
