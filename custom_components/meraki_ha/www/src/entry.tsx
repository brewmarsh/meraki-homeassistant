import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

class MerakiPanel extends HTMLElement {
  connectedCallback() {
    const shadow = this.attachShadow({ mode: 'open' });

    // Inject styles into Shadow DOM
    // Since Vite builds style.css alongside meraki-panel.js, we can link to it.
    // We assume style.css is in the same directory as the script/page.
    const styleLink = document.createElement('link');
    styleLink.setAttribute('rel', 'stylesheet');
    styleLink.setAttribute('href', 'style.css');
    shadow.appendChild(styleLink);

    const mountPoint = document.createElement('div');
    mountPoint.id = 'root';
    shadow.appendChild(mountPoint);

    const hass = (this as any).hass;
    const panel = (this as any).panel;
    const config_entry_id = panel?.config?.config_entry_id;

    const root = ReactDOM.createRoot(mountPoint);
    root.render(
      <React.StrictMode>
        <App hass={hass} config_entry_id={config_entry_id} />
      </React.StrictMode>
    );
  }
}

if (!customElements.get('meraki-panel')) {
  customElements.define('meraki-panel', MerakiPanel);
}
