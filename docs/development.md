# Development Guide

This document provides instructions for setting up a development environment for the Meraki Home Assistant integration.

## Frontend Development

The Meraki side panel is a modern web application built with React, Vite, and TypeScript.

### Frontend Code Location

The source code for the frontend panel is located in the `custom_components/meraki_ha/www/` directory.

### Installing Dependencies

To work with the frontend code, you must first install the necessary Node.js dependencies. Navigate to the frontend directory and run the following command:

```bash
cd custom_components/meraki_ha/www/
npm install
```

### Building the Frontend

After making changes to the frontend code, you must rebuild the panel to generate the final JavaScript and CSS files. To do this, run the following command from the `custom_components/meraki_ha/www/` directory:

```bash
npm run build
```

This will compile the frontend application and place the necessary `meraki-panel.js` and `style.css` files in the `custom_components/meraki_ha/www/` directory. These are the files that are served to Home Assistant.

### Development Server

For a more interactive development experience, you can run the Vite development server:

```bash
npm run dev
```

This will start a local server, typically on port 5173, that provides hot-reloading as you make changes to the code. Note that when running in this mode, the panel will not have access to the Home Assistant `hass` object and may not function completely, but it is useful for UI and styling work.