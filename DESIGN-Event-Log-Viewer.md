# Design Proposal: Event / Alert Log Viewer

This document outlines the design for the "Event / Alert Log Viewer" feature for the Meraki Home Assistant integration's web UI.

## 1. Feature Goal

To provide a clear, filterable, and searchable view of network events and alerts from the Meraki dashboard directly within the Home Assistant web UI. This will allow for quick diagnostics and monitoring without needing to leave the Home Assistant environment.

## 2. UI Design

A new page in the web UI called **"Event Log"** will be created, accessible from the main sidebar.

### Main View

The page will feature a table displaying the event logs. Each row will represent a single event with the following columns:

*   **Timestamp:** When the event occurred.
*   **Event Type:** A short, descriptive category for the event (e.g., "Client Connected", "Device Disconnected", "Firewall Rule Blocked").
*   **Description:** A detailed message about the event.
*   **Severity:** A color-coded indicator (e.g., "Info", "Warning", "Alert") to quickly identify important events.

### Controls

Above the table, there will be several controls to help users find the information they need:

*   **Time Range Filter:** A dropdown to select common time ranges (e.g., "Last Hour," "Last 24 Hours") and a custom date/time picker.
*   **Event Type Filter:** A multi-select dropdown to show or hide specific categories of events.
*   **Search Bar:** A text input to search for keywords within the event descriptions.

### UI Sketch

```
---------------------------------------------------------------------
| Event Log                                                         |
---------------------------------------------------------------------
|                                                                   |
|  Time Range: [ Last 24 Hours ▼ ]  Filter: [ All Types ▼ ]  [ Search... ] |
|                                                                   |
|  -----------------------------------------------------------------  |
|  | Timestamp           | Type                  | Description      |
|  -----------------------------------------------------------------  |
|  | 2025-08-20 19:00:00 | Client Connected      | John's iPad...   |
|  | 2025-08-20 18:55:12 | Device Disconnected   | Living Room AP...|
|  | 2025-08-20 18:52:03 | Content Blocked       | Gaming site...   |
|                                                                   |
---------------------------------------------------------------------
```

---

## 3. Implementation Plan & Instructions for a Continuing Agent

This section provides a detailed plan for an agent to implement this feature.

### Goal

Implement the "Event / Alert Log Viewer" as described in the design proposal.

### Prerequisites

*   Familiarity with React (functional components, hooks like `useState` and `useEffect`).
*   Understanding of how to make API calls in JavaScript using `fetch`.
*   Basic knowledge of the existing web UI structure (`App.jsx`, `Sidebar.jsx`, and the `pages` directory).

### Step-by-Step Implementation Plan

#### 1. Backend: Create the API Endpoint

*   **File to Modify:** `custom_components/meraki_ha/web_server.py`
*   **Tasks:**
    1.  Add a new route, `/api/events`, to the `_setup_routes` method.
    2.  Create a new handler function, `handle_api_events`, for this route.
    3.  This handler should accept query parameters for filtering (e.g., `startTime`, `endTime`, `eventType`).
    4.  Inside the handler, use the `self.coordinator.api_client` to call the Meraki Dashboard API endpoint to fetch the events. The primary endpoint to investigate is `GET /networks/{networkId}/events`. You may need to fetch events for all networks and combine them, or use an organization-level endpoint if available.
    5.  Process the data from the Meraki API into a clean JSON format suitable for the frontend and return it.

#### 2. Frontend: Build the UI

*   **Task 1: Create the Event Log Page**
    *   Create a new file: `custom_components/meraki_ha/web_ui/src/pages/EventLogPage.jsx`.
    *   In this file, create a new React component named `EventLogPage`.
    *   Use `useState` to manage the state for the event logs, loading status, errors, and filter values.
    *   Use `useEffect` to make an initial `fetch` call to your new `/api/events` endpoint when the component mounts.
    *   Render the UI as described in the design proposal (the filter controls and the table).

*   **Task 2: Add Navigation**
    *   **File to Modify:** `custom_components/meraki_ha/web_ui/src/components/Sidebar.jsx`
    *   **Task:** Add a new `NavLink` to the sidebar for the "Event Log" page, pointing to the `/events` route. Choose a suitable icon.

*   **Task 3: Add the Route**
    *   **File to Modify:** `custom_components/meraki_ha/web_ui/src/App.jsx`
    *   **Task:** Add a new `<Route>` for the `/events` path that renders your new `EventLogPage` component.

#### 3. Build and Verify

*   **Task 1: Build the Frontend**
    *   Navigate to the `custom_components/meraki_ha/web_ui/` directory.
    *   Run the command `npm run build` to compile the new frontend code.
*   **Task 2: Verify with a Test Script**
    *   Create a new Playwright script (e.g., `jules-scratch/verification/verify_event_log.py`).
    *   The script should:
        1.  Start a local web server for the `dist` directory.
        2.  Navigate to the web UI.
        3.  Click the "Event Log" link in the sidebar.
        4.  Verify that the "Event Log" page loads correctly and that the event table is visible.
        5.  Take a screenshot of the page.
