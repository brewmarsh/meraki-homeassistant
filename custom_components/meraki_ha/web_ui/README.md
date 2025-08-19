# Meraki HA Web UI Frontend

This directory contains the source code for the React-based web interface for the Meraki Home Assistant integration.

## Technology Stack

*   **Framework**: [React](https://reactjs.org/)
*   **Build Tool**: [Vite](https://vitejs.dev/)
*   **Styling**: [Tailwind CSS](https://tailwindcss.com/)

## Development Workflow

The final JavaScript and CSS that are served to the browser must be "built" or "compiled" from the source code in this `src` directory. The final output is placed in the `dist` directory, which is then served by the integration's Python web server.

### Prerequisites

You must have [Node.js](https://nodejs.org/) and `npm` installed on your development machine.

### 1. Install Dependencies

Before starting development, you need to install the required Node.js packages. Navigate to this directory (`custom_components/meraki_ha/web_ui/`) in your terminal and run:

```bash
npm install
```

This will download all the necessary libraries defined in `package.json` into a `node_modules` folder.

### 2. Run the Development Server

To see your changes live as you edit the code, you can run the Vite development server. This server provides features like Hot Module Replacement (HMR) for a fast development experience.

```bash
npm run dev
```

This will typically start a server on `http://localhost:5173`. Note that this is **separate** from the Home Assistant server. This development server is only for developing the UI components in isolation. To test with live data, you will need to point the API calls in the React code to your running Home Assistant instance.

### 3. Build for Production

When you have finished making changes to the UI, you must build the final, optimized assets. Run the following command:

```bash
npm run build
```

This command will compile all the React/JSX code and CSS into a set of static files and place them in the `dist` directory. **It is the content of the `dist` directory that is used by the Home Assistant integration.** After running this command, the changes will be visible when you access the UI through the integration's configured port in Home Assistant.
