import React from 'react';
import ReactDOM from 'react-dom/client';
// import App from './App.tsx';
import './index.css';

class MerakiHaPanel extends HTMLElement {
  _hass: any;
  _config_entry_id: string | null = null;
  root: ReactDOM.Root | null = null;

  set hass(hass: any) {
    this._hass = hass;
    this._render();
  }

  connectedCallback() {
    this._config_entry_id = this.getAttribute('config_entry_id');
    this.attachShadow({ mode: 'open' });
    const rootDiv = document.createElement('div');
    rootDiv.id = 'root';
    this.shadowRoot!.appendChild(rootDiv);
    this.root = ReactDOM.createRoot(rootDiv);
    this._render();
  }

  private _render() {
    if (this.root && this._hass && this._config_entry_id) {
      this.root.render(
        <React.StrictMode>
          <h1>Testing render</h1>
          {/* <App hass={this._hass} config_entry_id={this._config_entry_id} /> */}
        </React.StrictMode>
      );
    }
  }
}

customElements.define('meraki-ha-panel', MerakiHaPanel);
