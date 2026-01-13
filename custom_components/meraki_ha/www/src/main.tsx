<<<<<<< HEAD

=======
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
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

<<<<<<< HEAD
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
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
