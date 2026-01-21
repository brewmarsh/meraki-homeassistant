# Web UI Requirements for Home Assistant Integration

This document outlines the requirements for developing a self-hosted web interface for the Home Assistant integration.

## 1. Strategic Intent

The primary purpose of this web interface is to provide a user-friendly way to **view the status of and configure** the Meraki Home Assistant integration. It is not intended to replace the native Meraki Dashboard or the Home Assistant UI, but to supplement them with a dedicated control panel for this specific integration. Future development should prioritize adding controls for the integration's configuration options.

## 2. Web Interface Implementation Plan

The web interface will be a modern, single-page application (SPA) served by a lightweight Python web server that is started and managed by the Home Assistant integration itself.

<<<<<<< HEAD
### 2.1. Technology Stack
=======
\*\*2.1. Technology Stack
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

- **Backend/Web Server**: `aiohttp`.
- **Frontend Framework**: **React** (using Vite for tooling).
- **Styling**: **Tailwind CSS**.

<<<<<<< HEAD
### 2.2. Architecture
=======
\*\*2.2. Architecture
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

1. The integration will start an `aiohttp` web server on a user-configurable port.
2. The server will serve a pre-built React application from `web_ui/dist`.
3. The React app will consume REST API endpoints from the server to get data from the integration's coordinator.

<<<<<<< HEAD
### 2.3. API Endpoints
=======
\*\*2.3. API Endpoints
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

- `GET /api/config`: General configuration.
- `GET /api/networks`: List of all networks.
- `GET /api/clients`: List of all clients.
- `GET /api/networks/{id}`: Detailed information for a single network.
- `GET /api/clients/{mac}`: Detailed information for a single client.

## 3. UI/UX Design (V2)

The application layout will be updated to a two-column design with a new color scheme.

<<<<<<< HEAD
### 3.1. Layout
=======
\*\*3.1. Layout
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

- **Left Column (Sidebar):**
  - A fixed-width, persistent sidebar for navigation.
  - Links: Dashboard, Networks, Clients, Settings.
- **Right Column (Main Content):**
  - Displays the content for the selected page.

<<<<<<< HEAD
### 3.2. Theming and Color Scheme
=======
\*\*3.2. Theming and Color Scheme
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

- **Color Palette:**
  - **Primary/Accent:** Cisco Blue (e.g., `#00bceb`).
  - **Light Mode:** Light grey background, white cards, dark grey text.
  - **Dark Mode:** Very dark grey background, lighter dark grey cards, off-white text.
- **Dark Mode Implementation:**
  - Must support automatic dark mode based on `prefers-color-scheme`.
  - To be implemented using Tailwind CSS's `dark:` variant.

<<<<<<< HEAD
### 3.3. Card Layout
=======
\*\*3.3. Card Layout
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

- The existing card-based layout will be maintained and enhanced.
- Cards should be designed to be flexible for future additions (more data, action buttons).

## 4. Home Assistant Configuration

The following options will be managed via the integration's "Configure" panel.

- `enable_web_ui`: (boolean, Default: `True`)
- `web_ui_port`: (integer, Default: `9988`)
- `hide_unconfigured_ssids`: (boolean, Default: `False`)
- `ignored_networks`: (string, comma-separated list)

## 5. Architecture: Single vs. Multi-Instance Web UI

**Recommendation: Each integration hub should have its own web instance.** This is for simplicity, stability, and data isolation.
