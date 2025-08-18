# Web UI End-to-End Testing Plan

This document outlines the end-to-end test cases for the self-hosted web interface. The tests are prioritized to ensure the most critical user journeys are validated first.

## P0: Critical Path Tests

These tests cover the most critical user journeys and must pass for the feature to be considered stable.

### Test Case: UI-P0-01 - View Dashboard with Data
*   **Priority:** P0
*   **Description:** Ensures a user can open the web UI and see the main dashboard populated with network and client data.
*   **Preconditions:**
    *   The Meraki integration is configured and running.
    *   The Web UI is enabled on the default port (9988).
    *   The backend coordinator has successfully fetched at least one network and one client.
*   **Steps:**
    1.  Navigate to the web UI URL (e.g., `http://<home-assistant-ip>:9988`).
    2.  Wait for the page to load.
    3.  Observe the "Networks" card.
    4.  Observe the "Clients" card.
*   **Expected Result:**
    *   The page loads without errors.
    *   The "Networks" card displays a list of networks, matching the data from the backend.
    *   The "Clients" card displays a list of clients, matching the data from the backend.

### Test Case: UI-P0-02 - Navigate to Network Detail View
*   **Priority:** P0
*   **Description:** Ensures a user can navigate from the dashboard to a network's detail page and see the correct data.
*   **Preconditions:**
    *   Test Case UI-P0-01 is passing.
*   **Steps:**
    1.  On the dashboard, click on the first network card in the "Networks" list.
    2.  Observe the new page that loads.
*   **Expected Result:**
    *   The URL changes to `/networks/<network-id>`.
    *   The network detail page loads.
    *   The page title or header contains the name of the clicked network.
    *   The details displayed on the page (ID, name, tags, etc.) match the data for that specific network.

### Test Case: UI-P0-03 - Navigate to Client Detail View
*   **Priority:** P0
*   **Description:** Ensures a user can navigate from the dashboard to a client's detail page and see the correct data.
*   **Preconditions:**
    *   Test Case UI-P0-01 is passing.
*   **Steps:**
    1.  On the dashboard, click on the first client card in the "Clients" list.
    2.  Observe the new page that loads.
*   **Expected Result:**
    *   The URL changes to `/clients/<client-mac>`.
    *   The client detail page loads.
    *   The page title or header contains the description or MAC address of the clicked client.
    *   The details displayed on the page (MAC, IP, description, etc.) match the data for that specific client.

## P1: High Priority Tests

These tests cover important configuration options and error handling cases.

### Test Case: UI-P1-01 - UI is disabled via configuration
*   **Priority:** P1
*   **Description:** Ensures that when the web UI is disabled in the Home Assistant options, it is not accessible.
*   **Preconditions:**
    *   The Meraki integration is configured and running.
*   **Steps:**
    1.  In Home Assistant, go to the Meraki integration's configuration.
    2.  Uncheck the "Enable Web UI" option and save.
    3.  Attempt to navigate to the web UI URL (e.g., `http://<home-assistant-ip>:9988`).
*   **Expected Result:**
    *   The connection is refused. The page does not load.

### Test Case: UI-P1-02 - Change UI Port
*   **Priority:** P1
*   **Description:** Ensures that changing the port in the configuration correctly moves the web UI.
*   **Preconditions:**
    *   The Meraki integration is configured and running.
*   **Steps:**
    1.  In Home Assistant, go to the Meraki integration's configuration.
    2.  Change the "Web UI Port" to a new value (e.g., 9989). Save the configuration.
    3.  Attempt to navigate to the old port (9988).
    4.  Navigate to the new port (9989).
*   **Expected Result:**
    *   The connection to the old port is refused.
    *   The new port successfully loads the web UI dashboard.

## P2: Medium Priority Tests

These tests cover edge cases and less critical functionality.

### Test Case: UI-P2-01 - Dashboard with no data
*   **Priority:** P2
*   **Description:** Ensures the UI loads gracefully if the backend returns no networks or clients.
*   **Preconditions:**
    *   The Meraki integration is configured and running.
    *   The Web UI is enabled.
    *   The backend coordinator returns empty lists for networks and clients.
*   **Steps:**
    1.  Navigate to the web UI URL.
*   **Expected Result:**
    *   The page loads without errors.
    *   The "Networks" card shows a count of 0 and an empty list.
    *   The "Clients" card shows a count of 0 and an empty list.
