# Meraki Home Assistant Integration Web UI Refactor

This document outlines the requirements for a comprehensive refactor of the Meraki Home Assistant integration's web UI. The goal is to transform the existing static view into a dynamic, informative, and user-friendly dashboard that provides a real-time overview of the Meraki network's status and health.

## Core Principles

1.  **Dashboard First:** The primary view will be a high-level dashboard that provides an at-a-glance summary of the entire Meraki organization.
2.  **Drill-Down Capability:** Users must be able to click on any summary metric or device to access a detailed view with all relevant information.
3.  **Proactive Communication:** The UI should display not just the status of devices but also the reasons for that status, using information logged in the backend.
4.  **Modern UI/UX:** The interface will be a modern, responsive web application that works on both mobile and desktop and adapts to the user's browser theme (light/dark mode).
5.  **State-Driven Interface:** The UI will be a passive consumer of a live data feed from the Home Assistant backend via WebSockets, ensuring a performant and efficient user experience.

## Architecture & Design

The new UI will be a single-page application (SPA) built with **React** and styled with **Tailwind CSS**.

- **Data Model:** A dedicated WebSocket API endpoint will serve a centralized data payload containing device counts, a list of all discovered entities with their properties, and a new `status_messages` field on each device for human-readable log information.
- **Component Hierarchy:**
  - `App.tsx`: The main component that manages application state, the WebSocket connection, and client-side routing.
  - `Dashboard.tsx`: Displays high-level metrics using `StatusCard` components and a summary table of devices.
  - `DeviceView.tsx`: Displays detailed information for a single device.
  - `StatusCard.tsx`: A reusable component for displaying a single metric.
  - `DeviceTable.tsx`: A searchable, sortable table of all discovered Meraki devices.
- **Styling:** Tailwind's `dark:` modifier will be used for dark mode. The font will be `Inter`.

## Implementation Plan

### Phase 1: Backend Data & API

1.  **Create WebSocket Endpoint:**
    - Define a WebSocket handler in `custom_components/meraki_ha/api/websocket.py`.
    - The handler will send a complete data snapshot on connection and push updates when the coordinator's data changes.
2.  **Enrich Data with Status Messages:**
    - Add a `status_messages` list to each device's data payload in the Meraki data coordinator.
    - Log significant events to this list for display in the UI.

### Phase 2: Frontend Foundation (React)

1.  **Set up the React App:**
    - Create a new React app in `custom_components/meraki_ha/www`.
2.  **Connect to Backend:**
    - Establish a WebSocket connection in `App.tsx` to receive data from the Home Assistant backend.
3.  **Implement Routing:**
    - Create a simple state-based routing system in `App.tsx`.

### Phase 3: Dashboard & Core Components

1.  **Build `StatusCard.tsx`:**
    - Create a reusable component for displaying metrics.
2.  **Build `Dashboard.tsx`:**
    - Create a responsive card layout for key metrics.
3.  **Build `DeviceTable.tsx`:**
    - Create a searchable, sortable table of devices.

### Phase 4: Device Details & Final Touches

1.  **Build `DeviceView.tsx`:**
    - Display detailed information for a single device, including `status_messages`.
2.  **Implement Dark Mode:**
    - Ensure all components support dark mode.
3.  **Add Final Polish:**
    - Implement smooth transitions, icons, and ensure proper spacing.
