<<<<<<< HEAD

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

class MerakiPanel extends HTMLElement {
  connectedCallback() {
    const root = document.createElement('div');
    root.id = 'root';
    this.appendChild(root);

    const hass = (this as any).hass;
    const config_entry_id = (this as any).panel.config.config_entry_id;

    ReactDOM.createRoot(root).render(
      <React.StrictMode>
        <App hass={hass} config_entry_id={config_entry_id} />
      </React.StrictMode>
    );
  }
}

if (!customElements.get('meraki-panel')) {
  customElements.define('meraki-panel', MerakiPanel);
}
=======
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
