# Web UI V2 Requirements: Theming and Layout

This document outlines the requirements for a V2 update to the self-hosted web interface, focusing on visual theme, layout, and strategic intent.

## 1. Strategic Intent

The primary purpose of this web interface is to provide a user-friendly way to **view the status of and configure** the Meraki Home Assistant integration. It is not intended to replace the native Meraki Dashboard or the Home Assistant UI, but to supplement them with a dedicated control panel for this specific integration. Future development should prioritize adding controls for the integration's configuration options.

## 2. Layout

The application layout will be updated to a two-column design to improve navigation and scalability as more features are added.

*   **Left Column (Sidebar):**
    *   A fixed-width, persistent sidebar that is always visible.
    *   It will contain the main navigation links for the application.
    *   Initial navigation links will be:
        *   Dashboard (the current main view)
        *   Networks
        *   Clients
        *   Settings (for future configuration controls)
*   **Right Column (Main Content):**
    *   This area will take up the remaining page width.
    *   It will display the content for the currently selected page (e.g., the dashboard's cards, a list of networks, a settings form).

## 3. Theming and Color Scheme

The UI will be updated to use a professional color scheme inspired by Cisco's branding and will support both light and dark modes automatically.

*   **Color Palette:**
    *   **Primary/Accent Color:** A vibrant blue, similar to Cisco's branding (e.g., `#00bceb`). This will be used for links, active indicators, and primary buttons.
    *   **Light Mode Colors:**
        *   Background: White or a very light grey (e.g., `#f8f9fa`).
        *   Cards/Panels: White with subtle shadows.
        *   Text: Dark grey (e.g., `#212529`).
        *   Borders: Light grey (e.g., `#dee2e6`).
    *   **Dark Mode Colors:**
        *   Background: A very dark grey, near black (e.g., `#121212`).
        *   Cards/Panels: A slightly lighter dark grey (e.g., `#1e1e1e`).
        *   Text: A light, off-white grey (e.g., `#e8eaed`).
        *   Borders: A medium dark grey (e.g., `#3c4043`).

*   **Dark Mode Implementation:**
    *   The application must respect the user's OS-level or browser-level preference for dark mode.
    *   This will be implemented using the `prefers-color-scheme` CSS media query, which is supported out-of-the-box by Tailwind CSS's `dark:` variant.

## 4. Card Layout

The existing card-based layout will be maintained.

*   **Future Enhancement:** While not part of the immediate V2 implementation, the card design should be flexible enough to accommodate more information in the future. This could include adding small icons for status, secondary data points, or action buttons (e.g., "Block Client"). The initial redesign should focus on a clean presentation of the primary information.
