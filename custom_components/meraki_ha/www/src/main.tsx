import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';

class MerakiHaPanel extends HTMLElement {
  _hass: any;
  _config_entry_id: string | null = null;
  root: ReactDOM.Root | null = null;

  set hass(hass: any) {
    console.log('Hass property set');
    this._hass = hass;
    this._render();
  }

  connectedCallback() {
    console.log('Connected callback called');
    this._config_entry_id = this.getAttribute('config_entry_id');
    console.log('config_entry_id:', this._config_entry_id);
    this.attachShadow({ mode: 'open' });
    const rootDiv = document.createElement('div');
    rootDiv.id = 'root';
    this.shadowRoot!.appendChild(rootDiv);
    this.root = ReactDOM.createRoot(rootDiv);
    console.log('Root created');
    this._render();
  }

  private _render() {
    console.log('Render called');
    if (this.root && this._hass && this._config_entry_id) {
      console.log('Rendering app');
      this.root.render(
        <React.StrictMode>
          <App hass={this._hass} config_entry_id={this._config_entry_id} />
        </React.StrictMode>
      );
    } else {
        console.log('Not rendering app, missing data:', {
            root: !!this.root,
            hass: !!this._hass,
            config_entry_id: !!this._config_entry_id,
        });
    }
  }
}

customElements.define('meraki-ha-panel', MerakiHaPanel);
