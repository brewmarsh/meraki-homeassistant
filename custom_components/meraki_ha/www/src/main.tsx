import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';

// Allow access to HA-provided properties on the window object
declare global {
  interface Window {
    hass: any;
    config_entry_id: string;
  }
}

const rootElement = document.getElementById('root');

const renderApp = () => {
  if (rootElement && window.hass) {
    ReactDOM.createRoot(rootElement).render(
      <React.StrictMode>
        <App hass={window.hass} config_entry_id={window.config_entry_id} />
      </React.StrictMode>,
    );
  } else if (rootElement) {
      const interval = setInterval(() => {
          if (window.hass) {
              clearInterval(interval);
              renderApp();
          }
      }, 100);
  } else {
    console.error('Root element not found');
  }
};

renderApp();
