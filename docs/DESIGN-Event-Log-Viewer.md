### **Updated Design and Implementation Plan: Event / Alert Log Viewer**

### **1. Product Vision & Scope**

The goal is to provide a performant, scalable, and user-friendly interface for viewing Meraki events and alerts. This feature will focus on providing a quick, at-a-glance view of the most important events while ensuring the ability to dig deeper when needed, all without overwhelming the user or the Home Assistant instance. We'll leverage pagination and intelligent filtering to achieve this.

The scope of this feature remains a centralized log viewer with robust filtering capabilities.

---

### **2. Core Features & User Stories**

* **User Story: High-Level Monitoring**
    * **As a user,** I want to see a concise summary of recent network events and alerts at a glance, so I can quickly confirm that my network is operating as expected.
    * **Implementation:** The main table view with columns for **Timestamp**, **Event Type**, **Description**, and **Severity**.

* **User Story: Focused Troubleshooting**
    * **As a user,** I want to filter and search through events to pinpoint the cause of a problem, like why a specific device can't connect.
    * **Implementation:** Add **Time Range**, **Event Type**, and **Search** filters.

* **User Story: Performance Management (NEW)**
    * **As a user,** I want the log viewer to load quickly and not slow down my Home Assistant instance.
    * **Implementation:** The backend will use Meraki's API pagination features and the frontend will implement infinite scrolling or paginated loading to handle large datasets efficiently.

---

### **3. Technical Design**

#### **3.1. Meraki API Interaction (Crucial Updates)**

The `GET /networks/{networkId}/events` endpoint is a good starting point, but it's limited to a single network. A more scalable solution for users with multiple networks would be to use an organization-level endpoint, if one exists, to avoid multiple API calls. A quick look at the Meraki API documentation shows a number of endpoints for getting events at the network level and for specific event types at the organization level, but not a single organization-wide event feed.

Therefore, the best approach is to query each configured network for its events and then combine them on the backend.

* **Backend (`web_server.py`):**
    * The `handle_api_events` function will need to iterate through **all networks** configured in the integration.
    * For each network, it will call `GET /networks/{networkId}/events`.
    * It must handle the API's pagination by making multiple requests (using the `perPage` and `startingAfter`/`endingBefore` parameters) to retrieve a full set of events for the requested time range.
    * The backend should apply the time range and search/type filters **before** returning the data to the frontend, minimizing the amount of data transferred. The Meraki API supports filtering by `includedEventTypes` and `excludedEventTypes`, which should be leveraged to reduce the initial payload size.

#### **3.2. Frontend: UI & Performance**

* **Frontend (`EventLogPage.jsx`):**
    * The UI design is solid, but the implementation should prioritize performance.
    * Instead of loading all events at once, the `useEffect` hook should initiate a request for the first page of results (e.g., 50-100 events).
    * Implement **paginated loading** or **infinite scrolling**. When the user scrolls to the bottom of the table, the frontend should trigger another API call to fetch the next page of results using the Meraki `startingAfter` token.
    * The search and filter controls should trigger a new API call with the relevant parameters, not just filter the data on the client side. This is vital for performance on large datasets.

#### **3.3. New Complementary Features**

1.  **Event Type Icons & Colors:**
    * **Concept:** Use icons and colors to provide an immediate visual cue for event types and severity.
    * **Implementation:** Create a mapping in the frontend that assigns an icon (e.g., a "check-circle" for connected, a "warning-triangle" for warnings) and a color to each `eventType` returned by the Meraki API. This makes the log much easier to scan.

2.  **Configurable Push Notifications:**
    * **Concept:** Allow users to receive Home Assistant push notifications for specific, high-severity Meraki events without needing to have the log viewer page open.
    * **Implementation:** This would be an additional feature, likely configured on a separate settings page. The integration could expose a Home Assistant **sensor entity** or **binary sensor** that triggers an event when a new alert (e.g., a **Firewall Rule Blocked** alert) appears in the Meraki event log. Users could then use Home Assistant automations to send a notification to their phone.
    * **Value:** Transforms the passive log viewer into an active alerting tool, which is a key value proposition for Home Assistant users.

3.  **Detailed Event Modal:**
    * **Concept:** Provide a way to view a single event in greater detail.
    * **Implementation:** When a user clicks a row in the table, a pop-up modal should appear showing all of the available data for that event from the Meraki API response. This often includes granular details like client IP, device MAC, and more, which are too verbose for the main table but crucial for advanced troubleshooting.
