<<<<<<< HEAD
### **AI Agent Instructions**
=======
\***\*AI Agent Instructions**
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

**Persona:** A senior product manager with a deep understanding of user experience and system architecture.

**Objective:** The primary objective is to transform the integration's web UI from a simple static view into a dynamic, informative dashboard. The goal is to surface a complete, real-time overview of the Meraki network's status and health. The UI should preemptively answer a user's questions by displaying critical information—such as device discovery, entity status, and potential issues—that currently resides in backend logs.

**Core Principles to Guide Implementation:**

<<<<<<< HEAD
1.  **Dashboard First:** The initial view must be a high-level dashboard. It should provide a quick, at-a-glance summary of the entire organization, including key counts (e.g., number of wireless devices, switches, cameras) and any critical alerts.
2.  **Drill-Down Capability:** The user must be able to click on any summary metric or a specific device to access a detailed view. This detailed view will contain all relevant information for that specific device or entity, including its associated sensors, switches, and any logged status messages.
3.  **Proactive Communication:** The UI should move beyond showing what _is_ and begin explaining _why_. For example, instead of just showing that an RTSP stream is unavailable, it should display the specific reason logged in the backend. This is the core value-add for the user.
4.  **Modern UI/UX:** The interface must be a modern web application. It should be fully responsive, work seamlessly on both mobile and desktop, and automatically adapt to the user's browser theme (light/dark mode). All components should be reusable and adhere to a clean, consistent design language.
5.  **State-Driven Interface:** The UI should not poll the API directly. It must be a passive consumer of a live data feed from the Home Assistant backend. This will ensure a performant and efficient user experience.

---

### **Architecture & Design Instructions**
=======
1. **Dashboard First:** The initial view must be a high-level dashboard. It should provide a quick, at-a-glance summary of the entire organization, including key counts (e.g., number of wireless devices, switches, cameras) and any critical alerts.
2. **Drill-Down Capability:** The user must be able to click on any summary metric or a specific device to access a detailed view. This detailed view will contain all relevant information for that specific device or entity, including its associated sensors, switches, and any logged status messages.
3. **Proactive Communication:** The UI should move beyond showing what _is_ and begin explaining _why_. For example, instead of just showing that an RTSP stream is unavailable, it should display the specific reason logged in the backend. This is the core value-add for the user.
4. **Modern UI/UX:** The interface must be a modern web application. It should be fully responsive, work seamlessly on both mobile and desktop, and automatically adapt to the user's browser theme (light/dark mode). All components should be reusable and adhere to a clean, consistent design language.
5. **State-Driven Interface:** The UI should not poll the API directly. It must be a passive consumer of a live data feed from the Home Assistant backend. This will ensure a performant and efficient user experience.

---

\***\*Architecture & Design Instructions**
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

The UI will be a single-page application (SPA) built using **React** for its component-based architecture and state management capabilities, with **Tailwind CSS** for a utility-first approach to styling.

- **Data Model:** The Home Assistant integration will expose a dedicated WebSocket API endpoint that serves a centralized data payload. This payload will contain counts for all device types, a list of all discovered entities with their properties (device info, type, status), and a new field for `status_messages` on each device. This new field will hold the valuable, human-readable information from the logs.
- **Component Hierarchy:**
  - **`App.tsx` (Main Component):** Manages the primary application state (e.g., `loading`, `data`, `activeView`). It establishes the WebSocket connection and handles client-side routing.
  - **`Dashboard.tsx`:** Displays the high-level metrics using `StatusCard` components and a summary table of devices.
  - **`DeviceView.tsx`:** Displays detailed information for a single device, including its metadata and a list of all associated entities.
  - **`StatusCard.tsx`:** A reusable component to show a single metric with a title, a value, and an icon. This promotes a consistent look and feel across the dashboard.
  - **`DeviceTable.tsx`:** A searchable, sortable component to list all discovered Meraki devices.
- **Styling:** Tailwind's `dark:` modifier will be used exclusively for dark mode. All styling will be done with Tailwind classes to ensure full responsiveness and a clean, modern aesthetic. The font should be `Inter` for clarity and a modern feel.

---

<<<<<<< HEAD
### **Detailed Implementation Plan**
=======
\***\*Detailed Implementation Plan**
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

This plan is a step-by-step guide for an AI agent to build the new UI from scratch.

**Phase 1: Backend Data & API**

<<<<<<< HEAD
1.  **Create WebSocket Endpoint:**
    - Create a new file, `custom_components/meraki_ha/api/websocket.py`.
    - Define a WebSocket handler that, when a connection is established, immediately sends a complete snapshot of the integration's data from `hass.data[DOMAIN][config_entry.entry_id]`.
    - Implement a state change listener (e.g., using a Home Assistant `callback`) that pushes updates to all connected WebSocket clients whenever the coordinator's data changes. This ensures the UI is always in sync.

2.  **Enrich Data with Status Messages:**
    - Modify the Meraki data coordinator to store a new `status_messages` list for each device in its data payload.
    - Whenever an entity or handler logs a significant event (e.g., "Could not retrieve stream..."), instead of just logging a message, it should also add a formatted string to this new `status_messages` list for the relevant device.

**Phase 2: Frontend Foundation (React)**

1.  **Set up the React App:**
    - Create a React app in a new folder: `custom_components/meraki_ha/www`.
    - Remove all boilerplate code and create a single `App.tsx` component.
2.  **Connect to Backend:**
    - In `App.tsx`, use a `useState` hook for `data`, `loading`, and `error`.
    - In a `useEffect` hook, establish a WebSocket connection to the Home Assistant endpoint.
    - On a successful connection and a received message, update the `data` state. Implement a basic loading indicator (e.g., a spinner or text) while `loading` is true.
3.  **Implement Routing:**
    - Create a simple state-based routing system within `App.tsx` using a state variable like `activeView`.
    - The `App.tsx` component will conditionally render either the `Dashboard` component or the `DeviceView` component based on the `activeView` state.

**Phase 3: Dashboard & Core Components**

1.  **Build `StatusCard.tsx`:**
    - Create this reusable component. It will accept props like `title`, `value`, `icon`, and a `onClick` handler.
    - Apply Tailwind classes for styling, including responsive padding and margins. Use the `dark:` prefix for dark mode styles.
2.  **Build `Dashboard.tsx`:**
    - Use Tailwind's `grid-cols-1 md:grid-cols-2 lg:grid-cols-4` to create a responsive card layout.
    - Render an instance of `StatusCard` for each key metric: "Total Devices," "Wireless APs," "Switches," "Cameras," and "Virtual SSIDs." The values for these cards will come from the `data` received from the WebSocket.
3.  **Build `DeviceTable.tsx`:**
    - Create a component that renders a table with columns for **Device Name**, **Model**, and **Status**.
    - Add a search bar at the top to filter the table by device name or serial.
    - Add a `onClick` handler to each table row that sets the `activeView` state in the parent `App` component to show the device details.

**Phase 4: Device Details & Final Touches**

1.  **Build `DeviceView.tsx`:**
    - This component will receive the selected device's data as a prop.
    - Display key information like `name`, `model`, `serial`, and `firmware` in a prominent card at the top.
    - Display the new `status_messages` list from the device's data payload. Use a unique style (e.g., a red border for warnings) to make them stand out.
    - Create a list or table of all `entities` belonging to this device, clearly showing their name, type, and current state.
2.  **Implement Dark Mode:**
    - Review all React components and their styling.
    - For any color or background, ensure you have a `dark:` prefix class defined (e.g., `bg-white dark:bg-gray-800`). The browser will handle the rest.
3.  **Add Final Polish:**
    - Implement smooth transitions for component changes.
    - Add an icon for each card in the dashboard.
    - Ensure the overall layout is centered and has adequate spacing.
=======
1. **Create WebSocket Endpoint:**

   - Create a new file, `custom_components/meraki_ha/api/websocket.py`.
   - Define a WebSocket handler that, when a connection is established, immediately sends a complete snapshot of the integration's data from `hass.data[DOMAIN][config_entry.entry_id]`.
   - Implement a state change listener (e.g., using a Home Assistant `callback`) that pushes updates to all connected WebSocket clients whenever the coordinator's data changes. This ensures the UI is always in sync.

2. **Enrich Data with Status Messages:**
   - Modify the Meraki data coordinator to store a new `status_messages` list for each device in its data payload.
   - Whenever an entity or handler logs a significant event (e.g., "Could not retrieve stream..."), instead of just logging a message, it should also add a formatted string to this new `status_messages` list for the relevant device.

**Phase 2: Frontend Foundation (React)**

1. **Set up the React App:**
   - Create a React app in a new folder: `custom_components/meraki_ha/www`.
   - Remove all boilerplate code and create a single `App.tsx` component.
2. **Connect to Backend:**
   - In `App.tsx`, use a `useState` hook for `data`, `loading`, and `error`.
   - In a `useEffect` hook, establish a WebSocket connection to the Home Assistant endpoint.
   - On a successful connection and a received message, update the `data` state. Implement a basic loading indicator (e.g., a spinner or text) while `loading` is true.
3. **Implement Routing:**
   - Create a simple state-based routing system within `App.tsx` using a state variable like `activeView`.
   - The `App.tsx` component will conditionally render either the `Dashboard` component or the `DeviceView` component based on the `activeView` state.

**Phase 3: Dashboard & Core Components**

1. **Build `StatusCard.tsx`:**
   - Create this reusable component. It will accept props like `title`, `value`, `icon`, and a `onClick` handler.
   - Apply Tailwind classes for styling, including responsive padding and margins. Use the `dark:` prefix for dark mode styles.
2. **Build `Dashboard.tsx`:**
   - Use Tailwind's `grid-cols-1 md:grid-cols-2 lg:grid-cols-4` to create a responsive card layout.
   - Render an instance of `StatusCard` for each key metric: "Total Devices," "Wireless APs," "Switches," "Cameras," and "Virtual SSIDs." The values for these cards will come from the `data` received from the WebSocket.
3. **Build `DeviceTable.tsx`:**
   - Create a component that renders a table with columns for **Device Name**, **Model**, and **Status**.
   - Add a search bar at the top to filter the table by device name or serial.
   - Add a `onClick` handler to each table row that sets the `activeView` state in the parent `App` component to show the device details.

**Phase 4: Device Details & Final Touches**

1. **Build `DeviceView.tsx`:**
   - This component will receive the selected device's data as a prop.
   - Display key information like `name`, `model`, `serial`, and `firmware` in a prominent card at the top.
   - Display the new `status_messages` list from the device's data payload. Use a unique style (e.g., a red border for warnings) to make them stand out.
   - Create a list or table of all `entities` belonging to this device, clearly showing their name, type, and current state.
2. **Implement Dark Mode:**
   - Review all React components and their styling.
   - For any color or background, ensure you have a `dark:` prefix class defined (e.g., `bg-white dark:bg-gray-800`). The browser will handle the rest.
3. **Add Final Polish:**
   - Implement smooth transitions for component changes.
   - Add an icon for each card in the dashboard.
   - Ensure the overall layout is centered and has adequate spacing.
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

This implementation plan, guided by the product principles of being proactive and intuitive, will result in a significantly more useful and polished web UI for the Meraki Home Assistant integration.
