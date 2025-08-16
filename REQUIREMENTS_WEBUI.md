# Web UI Requirements for Home Assistant Integration

This document outlines the requirements for developing a self-hosted web interface for the Home Assistant integration. The target audience for this document is a development agent who will perform the implementation.

## 1. Web Interface Implementation Plan

The web interface will be a modern, single-page application (SPA) served by a lightweight Python web server that is started and managed by the Home Assistant integration itself.

### 1.1. Technology Stack

*   **Backend/Web Server**: `aiohttp`. This is the same asynchronous library used by Home Assistant, ensuring seamless integration and minimal dependency overhead. The server will be responsible for two things:
    1.  Serving the static frontend assets (HTML, CSS, JS).
    2.  Providing a simple REST API for the frontend to communicate with the Home Assistant integration hub.
*   **Frontend Framework**: **React** (using Vite for tooling). This allows for the creation of a dynamic, component-based, and modern UI.
*   **Styling**: **Tailwind CSS**. A utility-first CSS framework that enables rapid development of modern and responsive user interfaces.

### 1.2. Architecture

1.  When the Home Assistant integration hub starts, it will also start an `aiohttp` web server in the background on a user-configurable port.
2.  The web server will serve a pre-built React application from a dedicated `web_ui/dist` directory within the integration's folder.
3.  The React application will make API calls to the `aiohttp` server to fetch data and perform actions. The server will, in turn, get this data from the integration's data coordinator.

### 1.3. API Endpoints

The Python `aiohttp` server will expose the following endpoints, prefixed with `/api`:

*   `GET /api/config`: Returns basic configuration information, such as the organization name and other non-sensitive settings.
*   `GET /api/networks`: Returns a list of all WiFi networks (SSIDs) and their associated data (e.g., client count, status).
*   `GET /api/clients`: Returns a list of all connected clients, including their MAC, IP, connected SSID, and other relevant metadata.
*   `POST /api/networks/{ssid}/_enable`: A placeholder for a potential action to enable a specific network.
*   `POST /api/clients/{mac}/_block`: A placeholder for a potential action to block a specific client.

### 1.4. Project Structure

The integration's directory will be structured as follows:

```
custom_components/my_integration/
├── __init__.py
├── config_flow.py
├── const.py
├── coordinator.py
├── ... (other core integration files)
└── web_ui/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── dist/      <-- Pre-built static assets will be served from here
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── NetworkCard.jsx
        │   └── ClientCard.jsx
        └── ... (other React components)
```

## 2. Home Assistant Configuration

The integration's configuration flow (`config_flow.py`) in Home Assistant will be updated to include settings for the web interface.

### 2.1. Configuration Variables

The following options will be added to the integration's configuration schema:

*   `api_key`: (Type: `string`, Required: `True`). The API key for the service. This should be stored securely.
*   `organization_id`: (Type: `string`, Required: `True`). The target organization ID.
*   `enable_web_ui`: (Type: `boolean`, Default: `True`). A switch to allow the user to enable or disable the web interface entirely.
*   `web_ui_port`: (Type: `integer`, Default: `9988`). The port on which the self-hosted web interface will be accessible.

These will be managed via the "Configure" option on the integration's card in the Home Assistant dashboard.

## 3. Architecture: Single vs. Multi-Instance Web UI

**Recommendation: Each integration hub should have its own web instance.**

This model is recommended for the following reasons:

*   **Simplicity and Stability**: A 1:1 mapping between an integration instance (hub) and a web UI instance is vastly simpler to implement, test, and maintain. The web UI only needs to be aware of the single hub that launched it.
*   **Data Isolation**: This architecture ensures that the data for one hub is completely isolated from another. There is no risk of data leakage or incorrect actions being performed on the wrong hub.
*   **Resource Management**: It's easier for Home Assistant to manage the lifecycle of the web server when it's tied directly to the lifecycle of the integration hub. When the hub is unloaded, its associated web server is terminated.
*   **User Experience Clarity**: While a single "pane of glass" for multiple hubs is appealing, it introduces significant complexity (e.g., hub selection UI, aggregated views, routing commands to the correct hub). For a typical Home Assistant setup, users often manage distinct locations with separate hubs, and accessing them via different ports (e.g., `http://homeassistant.local:9988` for Hub 1, `http://homeassistant.local:9989` for Hub 2) is an acceptable and clear pattern.

## 4. General Integration Configuration Recommendations

To enhance the user experience and reduce noise, the following configuration values should be considered for the integration as a whole. These should be manageable via the integration's configuration options in the Home Assistant UI.

*   `scan_interval`: (Type: `integer`, Default: `60`). The interval in seconds for polling the API for new data.
*   `hide_unconfigured_ssids`: (Type: `boolean`, Default: `False`). If `True`, the web interface and Home Assistant entities will only show data for SSIDs that have been explicitly configured or enabled, hiding guest or neighboring networks.
*   `ignore_networks`: (Type: `list[string]`, Default: `[]`). A list of SSIDs that the integration should completely ignore. Data from these networks will not be fetched or displayed.
*   `track_devices_by_ssid`: (Type: `list[string]`, Default: `[]`). If this list is not empty, the integration will only create device tracker entities for clients connected to one of the specified SSIDs.

## 5. UI/UX Design

The web interface should be a modern, card-based web application.

*   **Layout**: A primary navigation sidebar on the left (for Dashboard, Networks, Clients, and Settings) and a main content area on the right.
*   **Dashboard**: The main landing page, showing high-level overview cards (e.g., "Total Clients", "Online Networks", "System Status").
*   **Networks Page**: A grid of "Network Cards". Each card represents an SSID and displays:
    *   The SSID name.
    *   An icon indicating its status (e.g., online, offline, warning).
    *   The number of connected clients.
    *   A "Details" button to navigate to a detailed view for that network.
*   **Clients Page**: A list or grid of "Client Cards". Each card represents a connected device and displays:
    *   Device hostname or user-defined alias.
    *   IP Address and MAC Address.
    *   The SSID it is connected to.
    *   Signal strength indicator.
*   **Responsiveness**: The design must be fully responsive, utilizing Tailwind CSS's responsive design utilities to ensure it is usable on both desktop and mobile devices.
*   **Real-time Updates**: The UI should periodically poll the backend API every 15-30 seconds to refresh data without requiring a full page load, providing a near real-time view of the network status.
